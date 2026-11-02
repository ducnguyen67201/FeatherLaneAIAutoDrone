"""Summarize recorded L15 simulator observations; never connect to a vehicle."""
from pathlib import Path
import json
import math
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'docs/evidence/l15-native-obstacle-stop'
GOAL_LATITUDE_E7 = -353632172
GOAL_LONGITUDE_E7 = 1491652374
HOME_LATITUDE_E7 = -353632621
METRES_PER_DEGREE = 6378137 * math.pi / 180
CASES = ['clear-final', 'blocked-final', 'observation-loss']
STATE_PATTERN = re.compile(r'FL L11 t=(\d+) s=(\w+) r=(\w+) ms=(\d+)')


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def position_error_m(message):
    north_m = (message['lat'] - GOAL_LATITUDE_E7) / 1e7 * METRES_PER_DEGREE
    east_m = ((message['lon'] - GOAL_LONGITUDE_E7) / 1e7 * METRES_PER_DEGREE
              * math.cos(math.radians(GOAL_LATITUDE_E7 / 1e7)))
    return math.hypot(north_m, east_m)


def summarize(case):
    run = ROOT / '.local/l15' / case
    rows = [row for row in read_rows(run / 'sitl/observations.jsonl')
            if (row['source_system'], row['source_component']) == (1, 1)]
    positions = [row for row in rows if row['message']['mavpackettype'] == 'GLOBAL_POSITION_INT']
    events = []
    for row in rows:
        message = row['message']
        if message['mavpackettype'] != 'STATUSTEXT':
            continue
        match = STATE_PATTERN.fullmatch(message['text'])
        if match:
            task_id, state, reason, boot_ms = match.groups()
            events.append({'task_id': int(task_id), 'state': state, 'reason': reason,
                           'boot_ms': int(boot_ms), 'received_wall_time': row['wall_time']})
    start = next(event for event in events if event['state'] == 'running' and event['reason'] == 'start')
    terminal = next(event for event in events if event['state'] in ['complete', 'blocked', 'failed'])
    land = next(row for row in rows if row['message']['mavpackettype'] == 'HEARTBEAT'
                and row['message']['custom_mode'] == 9 and row['wall_time'] > start['received_wall_time'])
    flight = [row for row in positions if start['boot_ms'] <= row['message']['time_boot_ms']
              and row['wall_time'] < land['wall_time']]
    times = [(row['message']['time_boot_ms'] - start['boot_ms']) / 1000 for row in flight]
    speeds = [math.hypot(row['message']['vx'], row['message']['vy']) / 100 for row in flight]
    north = [(row['message']['lat'] - HOME_LATITUDE_E7) / 1e7 * METRES_PER_DEGREE for row in flight]
    heights = [row['message']['relative_alt'] / 1000 for row in flight]
    summary = {
        'case': case, 'native_events': events,
        'native_terminal_seconds_after_start': (terminal['boot_ms'] - start['boot_ms']) / 1000,
        'peak_recorded_horizontal_speed_mps': max(speeds),
        'maximum_recorded_north_progress_m': max(north),
        'height_above_home_range_m': [min(heights), max(heights)],
        'maximum_position_sample_gap_s': max(second - first for first, second in zip(times, times[1:])),
        'flight_mode_sequence_after_start': [],
        'shutdown': json.loads((run / 'sitl/shutdown.json').read_text()),
    }
    for row in rows:
        message = row['message']
        if message['mavpackettype'] == 'HEARTBEAT' and row['wall_time'] >= start['received_wall_time']:
            mode = message['custom_mode']
            if not summary['flight_mode_sequence_after_start'] or summary['flight_mode_sequence_after_start'][-1] != mode:
                summary['flight_mode_sequence_after_start'].append(mode)
    if terminal['state'] == 'complete':
        dwell = next(event for event in events if event['state'] == 'dwelling')
        held = [row['message'] for row in flight if row['message']['time_boot_ms'] >= terminal['boot_ms']]
        summary['native_dwell_ms'] = terminal['boot_ms'] - dwell['boot_ms']
        summary['sampled_hold_after_complete_s'] = times[-1] - (terminal['boot_ms'] - start['boot_ms']) / 1000
        summary['maximum_goal_error_after_complete_m'] = max(position_error_m(message) for message in held)
    else:
        low_start_ms = None
        for row in flight:
            message = row['message']
            if message['time_boot_ms'] < terminal['boot_ms']:
                continue
            low_speed = math.hypot(message['vx'], message['vy']) / 100 <= 0.3
            if not low_speed:
                low_start_ms = None
            elif low_start_ms is None:
                low_start_ms = message['time_boot_ms']
            elif message['time_boot_ms'] - low_start_ms >= 2000:
                summary['sampled_two_second_stop_after_handoff_s'] = (message['time_boot_ms'] - terminal['boot_ms']) / 1000
                break
    if case.startswith('blocked'):
        truth_north = []
        for row in read_rows(run / 'poses.jsonl'):
            for pose in row.get('pose', []):
                if pose.get('name') == 'iris_l15':
                    truth_north.append(pose.get('position', {}).get('y', 0))
        summary['evaluation_truth_only'] = {
            'minimum_center_to_box_front_m': 6.3 - max(truth_north),
            'declared_body_disc_radius_m': 0.7,
            'minimum_declared_body_disc_gap_m': 6.3 - max(truth_north) - 0.7,
        }
    if case == 'observation-loss':
        observation_events = [row for row in rows if row['message']['mavpackettype'] == 'STATUSTEXT'
                              and row['message']['text'].startswith('FL L15 observation')]
        summary['observation_age_reports'] = [row['message']['text'] for row in observation_events]
        summary['injection'] = json.loads((run / 'injection.json').read_text())
    (OUTPUT / f'{case}-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary, times, north, heights, speeds


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True, constrained_layout=True)
    summaries = []
    for case, color in zip(CASES, ['#238443', '#d95f0e', '#756bb1']):
        summary, times, north, heights, speeds = summarize(case)
        summaries.append(summary)
        label = case.replace('-final', '').replace('-', ' ')
        for axis, values in zip(axes, [north, speeds, heights]):
            axis.plot(times, values, label=label, color=color)
            axis.axvline(summary['native_terminal_seconds_after_start'], color=color, linestyle=':', alpha=0.8)
    axes[0].axhline(5, color='gray', linestyle='--', linewidth=1, label='stored goal')
    axes[0].set_ylabel('North from home (m)')
    axes[0].legend(loc='upper left')
    axes[1].set_ylabel('Horizontal speed (m/s)')
    axes[2].set_ylabel('Height above home (m)')
    axes[2].set_ylim(2.6, 3.4)
    axes[2].set_xlabel('Seconds since native task start (autopilot boot clock)')
    axes[0].set_title('L15: native clear goal, obstacle veto, and observation-loss stop\nDotted lines mark native terminal reports; BRAKE stopping occurs afterward')
    for axis in axes:
        axis.grid(alpha=0.2)
    figure.savefig(OUTPUT / 'native-stop-comparison.png', dpi=170)
    plt.close(figure)
    print(json.dumps([{key: value for key, value in summary.items() if key != 'shutdown'} for summary in summaries], indent=2))


if __name__ == '__main__':
    main()
