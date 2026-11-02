"""Offline analysis of the manually moved obstacle and recorded observation path."""
from pathlib import Path
import collections
import hashlib
import json
import statistics
from pymavlink import mavutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / '.local/l13/session'
OUT = ROOT / 'docs/evidence/l13-obstacle-observation'
OUT.mkdir(exist_ok=True)
def load_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]
def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

observer = load_lines(RUN / 'observer2.jsonl')
samples = [row for row in observer if row['event'] == 'sample']
cases = load_lines(RUN / 'cases.jsonl')
vehicle = [row for row in load_lines(RUN / 'sitl/observations.jsonl')
           if (row['source_system'], row['source_component']) == (1, 1)]
summary_cases = []
for index, case in enumerate(cases):
    end = cases[index + 1]['wall_time'] if index + 1 < len(cases) else samples[-1]['wall_time']
    # Exclude a declared 350ms settling window after each manual scene move.
    selected = [row for row in samples if case['wall_time'] + 0.35 <= row['wall_time'] < end]
    finite = [row['distance_m'] for row in selected if row['distance_m'] is not None]
    summary_cases.append({**case, 'analysis_settling_window_s': 0.35,
        'samples': len(selected), 'statuses': dict(collections.Counter(row['observation_status'] for row in selected)),
        'all_sent': all(row['sent'] for row in selected),
        'distance_min_m': min(finite) if finite else None,
        'distance_max_m': max(finite) if finite else None,
        'maximum_error_m': max(abs(value - case['expected_distance_m']) for value in finite)
                           if finite and case['expected_distance_m'] is not None else None})
rfnd=[]; modes=[]
log=mavutil.mavlink_connection(str(RUN / 'sitl/logs/00000001.BIN'))
while True:
    message=log.recv_match(type=['RFND','MODE'])
    if message is None:break
    (rfnd if message.get_type()=='RFND' else modes).append(message.to_dict())
transitions=[]
for row in rfnd:
    if not transitions or row['Stat'] != transitions[-1]['Stat']:
        transitions.append(row)
heartbeats=[row for row in vehicle if row['message']['mavpackettype']=='HEARTBEAT']
positions=[row for row in vehicle if row['message']['mavpackettype']=='GLOBAL_POSITION_INT']
distance=[row for row in vehicle if row['message']['mavpackettype']=='DISTANCE_SENSOR']
process_events=load_lines(RUN / 'process-events.jsonl')
pause, resume = [row['wall_time'] for row in process_events]
last_before = max((row for row in samples if row['wall_time'] < pause), key=lambda row:row['wall_time'])
stale = next(row for row in observer if row['event']=='stale' and pause < row['wall_time'] < resume)
first_after = next(row for row in samples if row['wall_time'] > resume)
summary={'phase':'L13','case_results':summary_cases,
    'source_samples':len(samples),'source_simulator_span_s':samples[-1]['source_stamp_s']-samples[0]['source_stamp_s'],
    'sample_receive_span_s':samples[-1]['wall_time']-samples[0]['wall_time'],
    'source_stamp_increasing':all(b['source_stamp_s']>a['source_stamp_s'] for a,b in zip(samples,samples[1:])),
    'observer_events':dict(collections.Counter(row['event'] for row in observer)),
    'dropout':{'process_events':process_events,'last_sample_before_pause':last_before['wall_time'],
        'stale_event':stale,'stale_after_last_sample_s':stale['wall_time']-last_before['wall_time'],
        'first_sample_after_resume':{key:first_after[key] for key in ['wall_time','source_stamp_s','distance_m','sent']},
        'clock_limit':'Receive freshness only. Simulator/host/AP clocks are not synchronized; no end-to-end capture-age or latency bound.'},
    'consumer':{'RFND_samples':len(rfnd),'status_counts':dict(collections.Counter(row['Stat'] for row in rfnd)),
        'status_legend':{'1':'NoData','3':'OutOfRangeHigh','4':'Good'},'status_transitions':transitions,
        'MAVLink_distance_packets':len(distance),'telemetry_distances_cm':sorted(set(row['message']['current_distance'] for row in distance)),
        'metadata_limit':'AP output omits original FOV/quality metadata; id changes to backend instance0. Backend accepts by orientation, not sensor id.'},
    'vehicle':{'heartbeat_samples':len(heartbeats),'all_disarmed':all(not row['message']['base_mode']&128 for row in heartbeats),
        'modes':modes,'maximum_absolute_relative_alt_m':max(abs(row['message']['relative_alt'])/1000 for row in positions)},
    'limits':['Initial front_3m marker overlapped the subsequent manual move before its completion marker: mixed3m/5m samples retained, not used as a stable3m qualification. Use restored_3m instead.',
        'One static/disarmed simulation; no flight or obstacle control.',
        'All-infinity includes under-range blind spot: no_return is not proof of free space.',
        '10deg horizontal, one vertical plane; no rear/side/up/down or swept-body clearance.',
        'Malformed-input checks source-reviewed, not injected; no automated tests added.',
        'Initial source/observer1 differs from final observer2; both retained locally with separate hashes.',
        'Renderer warnings and missing DART mesh collision retained; no collision/hardware or reliability claim.']}
save('observation-summary.json',summary)
save('case-markers.json',cases)
save('example-scans.json',{status:next(row for row in samples if row['observation_status']==status) for status in ['return','no_return']})
start=cases[0]['wall_time']
fig,axes=plt.subplots(2,1,figsize=(11,6),sharex=False)
selected=[row for row in samples if row['wall_time']>=start]
plot_time=[];plot_distance=[]
for index,row in enumerate(selected):
    if index and row['wall_time']-selected[index-1]['wall_time']>0.35:
        plot_time.append(row['wall_time']-start);plot_distance.append(float('nan'))
    plot_time.append(row['wall_time']-start);plot_distance.append(row['distance_m'])
axes[0].plot(plot_time,plot_distance,color='#177968',label='Gazebo front fan nearest return')
no_return=[row for row in selected if row['observation_status']=='no_return']
axes[0].scatter([row['wall_time']-start for row in no_return],[8.5]*len(no_return),s=4,color='#a45b2c',label='No return (display marker, not distance)')
for case in cases:
    axes[0].axvline(case['wall_time']-start,color='gray',alpha=.3)
    if case['name']!='front_3m':
        axes[0].text(case['wall_time']-start,8.9,case['name'],fontsize=7,rotation=90,ha='left',va='bottom')
axes[0].axvspan(pause-start,resume-start,color='#bd4747',alpha=.15,label='Reader paused')
axes[0].set_ylim(0,12.5);axes[0].set_ylabel('Range (m) / no-return marker');axes[0].set_xlabel('Host receive seconds since first manual marker')
axes[0].legend(fontsize=8,loc='lower left');axes[0].grid(alpha=.2)
axes[1].step([row['TimeUS']/1e6 for row in rfnd],[row['Stat'] for row in rfnd],where='post',color='#3061a4')
axes[1].set_yticks([1,3,4],['NoData','OutOfRangeHigh','Good']);axes[1].set_ylabel('Onboard RFND status')
axes[1].set_xlabel('Autopilot boot seconds (separate clock)');axes[1].grid(alpha=.2)
fig.suptitle('L13 — actual front lidar observations and stock autopilot validity\nDisarmed, avoidance disabled; no-return does not establish clearance')
fig.tight_layout();fig.savefig(OUT/'obstacle-observations.png',dpi=160);plt.close(fig)
print(json.dumps({'cases':summary_cases,'dropout_stale_s':summary['dropout']['stale_after_last_sample_s'],'status_counts':summary['consumer']['status_counts'],'disarmed':summary['vehicle']},indent=2))
