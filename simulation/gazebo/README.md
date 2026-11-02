# L12 native macOS Gazebo baseline

[Observed evidence](../../docs/evidence/l12-instrumented-scene/README.md) · [Deployment diagram](../../docs/assets/learning/l12-simulator-deployment.svg) · [Core architecture](../../docs/architecture/README.md)

This is a headless local physics/IMU integration, qualified with one stock GUIDED flight, a fresh disarmed connection and a basic-SITL rollback. It adds no flight firmware, AI, ROS, obstacle sensing/avoidance or product UI. The native L11 executable remains preserved; its behavior on this changed X-frame plant is not inferred from this stock flight.

The qualified tuple is macOS15.7.7 arm64, Gazebo Sim8.10.0, gz-physics7.5.0/DART6.19.5, official ArduPilot plugin commit `f116b03552d05c8d0b0bed5ed67033a1183121d1`, AppleClang17 and the exact retained stock Copter-4.7.2 executable. [Source lock](source-lock.json) and [269-package native lock](conda-osx-arm64.lock.txt) record the actual selection. The complete package/build identities are in the evidence directory.

## Setup and build entry point

The environment lives in ignored `.local/l12/gazebo-env`, with a project-local micromamba2.10.0 executable/cache. No shell startup file is changed. The original Homebrew tap route had no bottle metadata in the examined gz-sim8 formula and required trust; no formula or trust was installed. The temporary tap was removed. Native conda-forge binaries supplied the actual working tuple instead.

For a fresh setup, obtain micromamba as described in its [official manual installation](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), verify the retained binary/archive identity, and place it at `.local/l12/micromamba/bin/micromamba`. From the project root:

```sh
export MAMBA_ROOT_PREFIX="$PWD/.local/l12/mamba-root"
.local/l12/micromamba/bin/micromamba --no-rc create \
  -p "$PWD/.local/l12/gazebo-env" \
  -f simulation/gazebo/conda-osx-arm64.lock.txt -y
```

The plugin checkout must be at `.local/l12/src/ardupilot_gazebo`, from the official repository and at the exact pinned revision. `CMakeLists.txt` builds its unmodified `ArduPilotPlugin.cc`, `SocketUDP.cc` and `Util.cc` only. Camera/streaming/parachute targets are outside L12; Gazebo packages still include their own transitive libraries. With that checkout present:

```sh
.local/l12/micromamba/bin/micromamba --no-rc run \
  -p "$PWD/.local/l12/gazebo-env" cmake \
  -S simulation/gazebo -B .local/l12/plugin-build \
  -DARDUPILOT_GAZEBO_SOURCE="$PWD/.local/l12/src/ardupilot_gazebo" \
  -DCMAKE_PREFIX_PATH="$PWD/.local/l12/gazebo-env" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_POLICY_VERSION_MINIMUM=3.5
.local/l12/micromamba/bin/micromamba --no-rc run \
  -p "$PWD/.local/l12/gazebo-env" cmake --build .local/l12/plugin-build -j4
```

## Launch and operate

Use one fresh run directory; do not overwrite retained session evidence. Run these in separate terminals, from the project root:

```sh
simulation/gazebo/run-gazebo.sh "$PWD/.local/l12/new-session"
simulation/gazebo/run-sitl.sh "$PWD/.local/l12/new-session"
```

`run-gazebo.sh` scopes the partition, loopback transport, plugin/resource paths and recording directory to this process. The world uses1ms steps, gravity, a ground plane, the official Iris and IMU system. `run-sitl.sh` selects the existing JSON model and official gazebo-iris defaults with a fresh EEPROM, then starts MAVProxy on TCP5760 and forwards MAVLink to UDP14550. The local profile retains QUAD/X, disables unqualified precision landing/rangefinder and requests WP_SPD1m/s. This differs from the basic QUAD/PLUS profile.

Wait for actual home/navigation validity and healthy disarmed state before normal operator commands. The recorded sequence was GUIDED, arm, takeoff3m, measured hover, `guided -35.3632172 149.1652374 3`, measured arrival/hold, explicit LAND and automatic disarm. These scripts launch processes; they do not issue flight commands or own a flight state machine.

After fresh on-ground/disarmed evidence, stop the owned SITL and launcher, passive recorders and then Gazebo. The last session was cleanly stopped. Rollback uses the exact stock executable with basic `quad`/`+` defaults in a fresh directory, with Gazebo absent; the observed rollback restored FRAME_TYPE0 and WP_SPD10.

## Qualification boundary

DART did not instantiate the official Iris mesh `base_collision`; primitive leg/rotor collisions are present and a level ground landing was observed. Body/obstacle collision behavior is unqualified. GUI, rendering, cameras, sensor-only autonomy, native L11 transfer, fault/reliability campaigns and hardware were not exercised. Gazebo model poses are privileged simulation evaluation data. A package install or successful build alone is not this qualification.

## L13 front-observation scene

The separate [L13 record](../../docs/evidence/l13-obstacle-observation/README.md) adds one front GPU lidar/static box and an observation-only adapter. It remains disarmed, with avoidance disabled; it adds no flight firmware. Use a fresh directory and pass `l13` as the second launcher argument in each terminal:

```sh
simulation/gazebo/run-gazebo.sh "$PWD/.local/l13/new-session" l13
simulation/gazebo/run-sitl.sh "$PWD/.local/l13/new-session" l13
.local/l02/venv/bin/python simulation/gazebo/range_observer.py \
  --record .local/l13/new-session/observer.jsonl
```

The adapter connects to existing TCP5762 and sends only DISTANCE_SENSOR. It reads real LaserScan samples, never model poses. The world/profile retain the L12 plant/JSON setup and explicitly add21 front rays across10deg in one plane over0.2–8m. Samples/no-return/stale state are written to a new exclusive JSONL file. Source and receive clocks are separate; capture latency is unqualified.

No-return is not clearance: a box below the0.2m minimum produced the same all-infinity output as one beyond8m. The801cm MAVLink value is an out-of-range sentinel, not a measured obstacle. Read the coverage/consumer limitations before any later control integration. Stop the observer after inspection; after fresh disarmed/on-ground evidence stop the owned SITL/recorder/server. Rollback is the default L12 world/profile in another fresh directory, without the observer or `l13` argument. The actual rollback confirmed RNGFND1_TYPE0 and no front_scan topic. L14 avoidance is not implemented by these launchers.

## L14 stock stopping and recorded 3D playback

[L14 evidence](../../docs/evidence/l14-stock-obstacle-stop/README.md) qualifies one head-on stock LOITER/Stop case, with a clear comparison. Use the same launchers with a fresh directory and second argument `l14`; start the observer with `--phase l14`. The profile enables rangefinder-based proximity and stock Stop, limits LOITER speed to 0.5 m/s and pilot lean to 1.5 degrees. Initial speed/timing failures are retained separately. This is operator-controlled stopping, not autonomous detouring or native ModeFeatherLane avoidance.

To watch the actual retained flights without running SITL, use separate terminals on macOS:

```sh
simulation/gazebo/replay-l14.sh server blocked
simulation/gazebo/replay-l14.sh gui blocked
```

Playback starts paused. In a third terminal, `simulation/gazebo/replay-l14.sh cue` seeks to 55 s, just before the recorded forward approach; `simulation/gazebo/replay-l14.sh play` starts playback and `simulation/gazebo/replay-l14.sh pause` pauses it. The GUI also has playback controls. The drone approaches the box, holds before it, then later lands because that operator command is in the recording. For the clear case, stop both owned playback terminals and start them with `clear` instead of `blocked`. The shared camera shows the starting area and box. Stop both terminals with Ctrl-C when finished.

These commands replay recorded entity states, not a new live flight or new evidence of control. The large state logs remain ignored under `.local/l14/{clear,blocked}-final/gazebo-record/`; they must exist locally. The recorder hashes and source identity are retained in L14 evidence. Current desktop observation is unavailable; GUI-visible flight is only claimed if the human confirms it.
