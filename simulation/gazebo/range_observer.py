"""Forward one fresh front LaserScan to a stock MAVLink rangefinder; no flight commands."""
from pathlib import Path
import argparse
import json
import math
import os
import selectors
import signal
import subprocess
import time

# Enable DISTANCE_SENSOR's FOV/quality extensions in this process only.
os.environ['MAVLINK20'] = '1'
from pymavlink import mavutil

MIN_RANGE_M = 0.2
MAX_RANGE_M = 8.0
HALF_ANGLE_RAD = math.radians(5)
MAX_RECEIVE_GAP_S = 0.35
MAX_HEARTBEAT_AGE_S = 2.5
MAX_BUFFER_BYTES = 65536
EXPECTED_RAYS = 21
EXPECTED_FRAME = 'iris_l13::front_lidar_link::front_range'
TOPIC = '/l13/front_scan'


def decode_scan(message, previous_stamp_s, expected_frame=EXPECTED_FRAME):
    """Validate the declared sensor geometry and classify its actual range returns."""
    stamp = message['header']['stamp']
    seconds = float(stamp.get('sec', 0))
    nanoseconds = int(stamp.get('nsec', 0))
    if not 0 <= nanoseconds < 1_000_000_000:
        raise ValueError('source_clock')
    stamp_s = seconds + nanoseconds / 1e9
    if not math.isfinite(stamp_s) or stamp_s < 0 or stamp_s <= previous_stamp_s:
        raise ValueError('source_clock')
    if message['frame'] != expected_frame:
        raise ValueError('frame')
    if message['count'] != EXPECTED_RAYS or message['verticalCount'] != 1:
        raise ValueError('coverage')
    for key, expected in [('rangeMin', MIN_RANGE_M), ('rangeMax', MAX_RANGE_M),
                          ('angleMin', -HALF_ANGLE_RAD), ('angleMax', HALF_ANGLE_RAD)]:
        if not math.isclose(float(message[key]), expected, abs_tol=0.0001):
            raise ValueError('geometry')
    ranges = [float(value) for value in message['ranges']]
    if len(ranges) != EXPECTED_RAYS or any(math.isnan(value) or value < 0 for value in ranges):
        raise ValueError('ranges')
    finite = [value for value in ranges if math.isfinite(value)]
    if any(value < MIN_RANGE_M - 0.0001 or value > MAX_RANGE_M + 0.0001 for value in finite):
        raise ValueError('range_bounds')
    # Positive infinity means no return within this narrow fan and configured range.
    if not finite:
        return stamp_s, 'no_return', None, int(MAX_RANGE_M * 100) + 1
    distance_m = min(MAX_RANGE_M, max(MIN_RANGE_M, min(finite)))
    return stamp_s, 'return', distance_m, int(round(distance_m * 100))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--endpoint', default='tcp:127.0.0.1:5762')
    parser.add_argument('--phase', choices=['l13', 'l14'], default='l13',
                        help='L13 is disarmed-only; L14 permits the scoped simulator flight')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    topic = f'/{args.phase}/front_scan'
    expected_frame = f'iris_{args.phase}::front_lidar_link::front_range'
    environment = dict(os.environ, GZ_PARTITION=f'featherlane_{args.phase}', GZ_IP='127.0.0.1',
                       MAMBA_ROOT_PREFIX=str(root / '.local/l12/mamba-root'))
    command = [str(root / '.local/l12/micromamba/bin/micromamba'), '--no-rc', 'run',
               '-p', str(root / '.local/l12/gazebo-env'), 'gz', 'topic', '-e',
               '-t', topic, '--json-output']
    args.record.parent.mkdir(parents=True, exist_ok=True)
    connection = mavutil.mavlink_connection(args.endpoint, source_system=255, source_component=191)
    scan_process = None
    selector = selectors.DefaultSelector()
    with args.record.open('x') as output:
        def record(**fields):
            output.write(json.dumps({'wall_time': time.time(), 'monotonic_s': time.monotonic(), **fields}) + '\n')
            output.flush()

        try:
            scan_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=False,
                                            env=environment, start_new_session=True)
            os.set_blocking(scan_process.stdout.fileno(), False)
            selector.register(scan_process.stdout, selectors.EVENT_READ)
            buffer = b''
            previous_stamp_s = -1.0
            last_source_received = None
            last_heartbeat = None
            armed = False
            last_status = None
            record(event='started', endpoint=args.endpoint, topic=topic, phase=args.phase,
                   max_receive_gap_s=MAX_RECEIVE_GAP_S, commands='DISTANCE_SENSOR only')
            while True:
                now = time.monotonic()
                for _ in range(50):
                    message = connection.recv_match(blocking=False)
                    if message is None:
                        break
                    if (message.get_type() == 'HEARTBEAT' and message.get_srcSystem() == 1
                            and message.get_srcComponent() == 1):
                        last_heartbeat = now
                        armed = bool(message.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                if armed and args.phase == 'l13':
                    raise RuntimeError('L13 observation qualification requires a disarmed vehicle')
                heartbeat_fresh = last_heartbeat is not None and now - last_heartbeat <= MAX_HEARTBEAT_AGE_S
                for key, _ in selector.select(timeout=0.05):
                    data = os.read(key.fd, MAX_BUFFER_BYTES)
                    if not data:
                        raise RuntimeError('LaserScan reader exited')
                    buffer += data
                    if len(buffer) > MAX_BUFFER_BYTES:
                        raise RuntimeError('LaserScan record exceeds buffer limit')
                    complete_records = buffer.split(b'\n')
                    buffer = complete_records.pop()
                    if len(complete_records) > 1:
                        record(event='discarded_queue', count=len(complete_records) - 1)
                    # Forward the newest complete observation, never replay a queued history.
                    for line in complete_records[-1:]:
                        if not line.strip():
                            continue
                        try:
                            scan = json.loads(line)
                            stamp_s, status, distance_m, distance_cm = decode_scan(scan, previous_stamp_s, expected_frame)
                        except (ValueError, TypeError, KeyError, OverflowError) as error:
                            last_source_received = None
                            record(event='invalid', reason=str(error))
                            continue
                        previous_stamp_s = stamp_s
                        last_source_received = time.monotonic()
                        sent = heartbeat_fresh
                        if sent:
                            # Source simulator clock is not the autopilot boot clock. The stock
                            # backend ages packets using its own receive time, not this field.
                            connection.mav.distance_sensor_send(
                                int(stamp_s * 1000) & 0xFFFFFFFF, int(MIN_RANGE_M * 100),
                                int(MAX_RANGE_M * 100), distance_cm,
                                mavutil.mavlink.MAV_DISTANCE_SENSOR_LASER, 1,
                                mavutil.mavlink.MAV_SENSOR_ROTATION_NONE, 255,
                                horizontal_fov=2 * HALF_ANGLE_RAD, vertical_fov=0,
                                signal_quality=0)
                        record(event='sample', source_stamp_s=stamp_s, observation_status=status,
                               distance_m=distance_m, sent=sent, wire_distance_cm=distance_cm,
                               scan=scan)
                        last_status = status if sent else 'vehicle_heartbeat_unavailable'
                # This bounds receive freshness; simulator and host clocks are not synchronized.
                stale = last_source_received is None or time.monotonic() - last_source_received > MAX_RECEIVE_GAP_S
                if stale and last_status != 'stale':
                    record(event='stale', action='stop forwarding; stock receive timeout owns NoData')
                    last_status = 'stale'
        except KeyboardInterrupt:
            record(event='stopped', reason='operator')
        except (RuntimeError, OSError) as error:
            record(event='stopped', reason=str(error))
            raise
        finally:
            selector.close()
            if scan_process is not None and scan_process.poll() is None:
                # This new process group belongs only to the observation reader we started.
                os.killpg(scan_process.pid, signal.SIGTERM)
                try:
                    scan_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(scan_process.pid, signal.SIGKILL)
                    scan_process.wait(timeout=3)
            connection.close()


if __name__ == '__main__':
    main()
