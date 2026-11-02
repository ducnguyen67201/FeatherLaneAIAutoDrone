"""Analyze retained L14 manual flights offline; never connects to a vehicle."""
from pathlib import Path
import collections
import csv
import json
import math
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pymavlink import mavutil

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = PROJECT_ROOT / '.local/l14'
OUTPUT_ROOT = PROJECT_ROOT / 'docs/evidence/l14-stock-obstacle-stop'
HOME_LAT_DEG = -35.3632621
HOME_LON_DEG = 149.1652374
EARTH_RADIUS_M = 6378137
WALL_FACE_NORTH_M = 6.3
BODY_ENVELOPE_RADIUS_M = 0.7


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def write_json(name, value):
    (OUTPUT_ROOT / name).write_text(json.dumps(value, indent=2) + '\n')


def write_csv(name, rows):
    if not rows:
        return
    with (OUTPUT_ROOT / name).open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def analyze_case(case):
    run = RUN_ROOT / f'{case}-final'
    rows = [row for row in read_rows(run / 'sitl/observations.jsonl')
            if (row['source_system'], row['source_component']) == (1, 1)]
    intervals = []
    active = None
    for row in rows:
        message = row['message']
        if message['mavpackettype'] != 'RC_CHANNELS':
            continue
        if active is None or message['chan2_raw'] != active['RC2']:
            if active is not None:
                active.update(end=row['wall_time'], end_boot_ms=message['time_boot_ms'])
                intervals.append(active)
            active = {'RC2': message['chan2_raw'], 'start': row['wall_time'],
                      'start_boot_ms': message['time_boot_ms']}
    pulse = [interval for interval in intervals if interval['RC2'] == 1000][-1]
    start_ms = pulse['start_boot_ms']
    end_ms = pulse['end_boot_ms']
    latest = {}
    trajectory = []
    for row in rows:
        message = row['message']
        latest[message['mavpackettype']] = row
        if message['mavpackettype'] != 'GLOBAL_POSITION_INT':
            continue
        if not start_ms <= message['time_boot_ms'] <= end_ms + 4000:
            continue
        heartbeat = latest.get('HEARTBEAT')
        rc_input = latest.get('RC_CHANNELS')
        gps = latest.get('GPS_RAW_INT')
        ekf = latest.get('EKF_STATUS_REPORT')
        landed = latest.get('EXTENDED_SYS_STATE')
        fresh = all(item is not None and 0 <= row['wall_time'] - item['wall_time'] <= 2.5
                    for item in [heartbeat, rc_input, gps, ekf, landed])
        trajectory.append({
            'wall_time': row['wall_time'],
            'boot_ms': message['time_boot_ms'],
            'elapsed_s': (message['time_boot_ms'] - start_ms) / 1000,
            'north_m': math.radians(message['lat'] / 1e7 - HOME_LAT_DEG) * EARTH_RADIUS_M,
            'east_m': math.radians(message['lon'] / 1e7 - HOME_LON_DEG) * EARTH_RADIUS_M * math.cos(math.radians(HOME_LAT_DEG)),
            'height_m': message['relative_alt'] / 1000,
            'horizontal_speed_mps': math.hypot(message['vx'], message['vy']) / 100,
            'vertical_speed_down_mps': message['vz'] / 100,
            'armed': bool(heartbeat and heartbeat['message']['base_mode'] & 128),
            'mode': heartbeat['message']['custom_mode'] if heartbeat else None,
            'rc2': rc_input['message']['chan2_raw'] if rc_input else None,
            'fresh_navigation': bool(fresh and gps['message']['fix_type'] >= 3 and ekf['message']['flags'] & 16),
            'input_interval': message['time_boot_ms'] < end_ms,
        })
    commanded = [row for row in trajectory if row['input_interval']]
    first = None
    completed = None
    previous = None
    for sample in commanded:
        # Require substantial approach progress: initial stationary hover is not a stop.
        bounded = (sample['north_m'] >= 3 and sample['horizontal_speed_mps'] <= 0.15
                   and abs(sample['height_m'] - 3) <= 0.4 and sample['fresh_navigation']
                   and sample['armed'] and sample['mode'] == 5 and sample['rc2'] == 1000)
        gap = previous is not None and (sample['wall_time'] - previous['wall_time'] > 0.75
                                       or sample['boot_ms'] - previous['boot_ms'] > 750)
        if not bounded or gap:
            first = None
        if bounded:
            if first is None:
                first = sample
            duration = min(sample['elapsed_s'] - first['elapsed_s'], sample['wall_time'] - first['wall_time'])
            if duration >= 2 and completed is None:
                completed = {'first': first, 'completed': sample, 'dwell_s': duration}
        previous = sample
    onboard = []
    log = mavutil.mavlink_connection(str(run / 'sitl/logs/00000001.BIN'))
    while True:
        message = log.recv_match(type=['RFND', 'PRX', 'SA', 'MODE'])
        if message is None:
            break
        onboard.append(message.to_dict())
    avoidance = [row for row in onboard if row['mavpackettype'] == 'SA'
                 and start_ms <= row['TimeUS'] / 1000 < end_ms]
    pose_samples = []
    box_center = [5, 6.55] if case == 'clear' else [0, 6.55]
    for row in read_rows(run / 'poses.jsonl'):
        pose = next(item for item in row['pose'] if item['name'] == 'iris_l14')
        position = pose['position']
        east = position.get('x', 0)
        north = position.get('y', 0)
        # Conservative horizontal disc versus the known static rectangular box.
        # All session poses are used; no cross-clock alignment is assumed.
        box_distance = math.hypot(max(abs(east - box_center[0]) - 1, 0),
                                  max(abs(north - box_center[1]) - 0.25, 0))
        pose_samples.append({'gazebo_time_s': float(row['header']['stamp'].get('sec', 0)) + row['header']['stamp'].get('nsec', 0) / 1e9,
                             'east_m': east, 'north_m': north, 'world_z_m': position.get('z', 0),
                             'center_to_box_xy_m': box_distance,
                             'declared_envelope_gap_m': box_distance - BODY_ENVELOPE_RADIUS_M})
    observer = read_rows(run / 'observer.jsonl')
    samples = [row for row in observer if row['event'] == 'sample' and pulse['start'] <= row['wall_time'] < pulse['end']]
    summary = {
        'selected_pulse': pulse,
        'input_boot_span_s': (end_ms - start_ms) / 1000,
        'input_receive_span_s': pulse['end'] - pulse['start'],
        'peak_horizontal_speed_mps': max(row['horizontal_speed_mps'] for row in commanded),
        'maximum_north_m': max(row['north_m'] for row in commanded),
        'maximum_north_through_neutral_hold_m': max(row['north_m'] for row in trajectory),
        'maximum_lateral_magnitude_m': max(abs(row['east_m']) for row in commanded),
        'maximum_height_error_m': max(abs(row['height_m'] - 3) for row in commanded),
        'all_input_samples_armed_LOITER_fresh': all(row['armed'] and row['mode'] == 5 and row['fresh_navigation'] for row in commanded),
        'stopped_while_forward_held': completed,
        'minimum_center_to_wall_face_m': WALL_FACE_NORTH_M - max(row['north_m'] for row in commanded) if case == 'blocked' else None,
        'sensor_observation_counts_during_pulse': dict(collections.Counter(row['observation_status'] for row in samples)),
        'all_sensor_samples_sent': all(row['sent'] for row in samples),
        'minimum_sensor_return_m': min((row['distance_m'] for row in samples if row['distance_m'] is not None), default=None),
        'native_avoidance_records_during_pulse': len(avoidance),
        'native_avoidance_records_without_backup': all(row['Back'] == 0 for row in avoidance),
        'all_session_gazebo_evaluation': {
            'pose_samples': len(pose_samples),
            'minimum_center_to_box_xy_m': min(row['center_to_box_xy_m'] for row in pose_samples),
            'body_envelope_radius_m': BODY_ENVELOPE_RADIUS_M,
            'minimum_declared_envelope_gap_m': min(row['declared_envelope_gap_m'] for row in pose_samples),
            'scope': 'Known box geometry/poses are evaluation only; planar envelope bound is not mesh/contact or physical qualification.'},
        'onboard_counts': dict(collections.Counter(row['mavpackettype'] for row in onboard)),
        'observer_events': dict(collections.Counter(row['event'] for row in observer)),
        'all_RC_intervals': intervals,
        'operator_events': read_rows(run / 'operator-events.jsonl'),
        'shutdown': json.loads((run / 'sitl/shutdown.json').read_text()),
    }
    write_json(f'{case}-summary.json', summary)
    write_csv(f'{case}-trajectory.csv', trajectory)
    write_csv(f'{case}-avoidance.csv', avoidance)
    write_csv(f'{case}-gazebo-poses.csv', pose_samples)
    write_csv(f'{case}-rangefinder.csv', [row for row in onboard if row['mavpackettype'] == 'RFND'])
    for source, name in [(run / 'sitl/console.log', f'{case}-console.txt'),
                         (RUN_ROOT / f'{case}-final-gazebo.log', f'{case}-gazebo-console.txt')]:
        text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', source.read_text(errors='replace')).replace('\r', '')
        (OUTPUT_ROOT / name).write_text('\n'.join(line.rstrip() for line in text.splitlines()) + '\n')
    return summary, trajectory, avoidance, pose_samples


OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
results = {case: analyze_case(case) for case in ['clear', 'blocked']}
figure, axes = plt.subplots(2, 2, figsize=(12, 8))
colors = {'clear': '#167b6d', 'blocked': '#a85732'}
for case, (summary, trajectory, _, poses) in results.items():
    time_axis = [row['elapsed_s'] for row in trajectory]
    axes[0, 0].plot(time_axis, [row['north_m'] for row in trajectory], color=colors[case], label=case)
    axes[0, 1].plot(time_axis, [row['horizontal_speed_mps'] for row in trajectory], color=colors[case], label=case)
    for axis in axes[0]:
        axis.axvline(summary['input_boot_span_s'], color=colors[case], linestyle=':', linewidth=1)
    axes[1, 1].plot([row['east_m'] for row in poses], [row['north_m'] for row in poses], color=colors[case], label=case)
axes[0, 0].set_ylabel('North from starting home (m)')
axes[0, 1].set_ylabel('Actual horizontal speed (m/s)')
axes[0, 1].axhline(0.15, color='gray', linestyle='--', linewidth=0.8)
for axis in axes[0]:
    axis.set_xlabel('Autopilot seconds since observed full forward input')
    axis.legend(fontsize=8)
blocked_summary, _, avoidance, _ = results['blocked']
start_s = blocked_summary['selected_pulse']['start_boot_ms'] / 1000
axes[1, 0].plot([row['TimeUS'] / 1e6 - start_s for row in avoidance], [math.hypot(row['DVelX'], row['DVelY']) for row in avoidance], label='Desired before avoidance')
axes[1, 0].plot([row['TimeUS'] / 1e6 - start_s for row in avoidance], [math.hypot(row['MVelX'], row['MVelY']) for row in avoidance], label='Modified by stock avoidance')
axes[1, 0].set_xlabel('Autopilot seconds since forward input (blocked)')
axes[1, 0].set_ylabel('Onboard SA horizontal velocity (m/s)')
axes[1, 0].legend(fontsize=8)
for east, color, label in [(5, colors['clear'], 'Box aside'), (0, colors['blocked'], 'Box ahead')]:
    axes[1, 1].add_patch(Rectangle((east - 1, 6.3), 2, 0.5, fill=False, edgecolor=color))
    axes[1, 1].text(east, 6.95, label, ha='center', fontsize=8)
axes[1, 1].set_xlabel('Gazebo east (m)')
axes[1, 1].set_ylabel('Gazebo north (m)')
axes[1, 1].set_xlim(-1.5, 6.5)
axes[1, 1].set_ylim(-0.5, 7.6)
axes[1, 1].set_aspect('equal', adjustable='box')
axes[1, 1].legend(fontsize=8, loc='lower right')
for axis in axes.flat:
    axis.grid(alpha=0.2)
figure.suptitle('L14 — stock LOITER/Stop: clear advance versus blocked stop\nDotted lines: input returned to neutral; plan view uses separately recorded Gazebo poses')
figure.tight_layout()
figure.savefig(OUTPUT_ROOT / 'stock-stop-comparison.png', dpi=160)
plt.close(figure)
print(json.dumps({case: {key: summary[key] for key in ['input_boot_span_s', 'input_receive_span_s', 'peak_horizontal_speed_mps', 'maximum_north_m', 'minimum_sensor_return_m', 'native_avoidance_records_during_pulse', 'all_session_gazebo_evaluation']} for case, (summary, _, _, _) in results.items()}, indent=2))
