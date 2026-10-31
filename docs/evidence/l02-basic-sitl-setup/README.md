# L02 — Native macOS build and disarmed SITL

[Project](../../../README.md) · [Learning card](../../phases/learning/l02-basic-sitl-setup.md) · [L01 source](../l01-source-and-orientation/README.md)

Executed locally on 2026-10-31 after the user requested: “Okay, let's start L02. Walk me through building and running the simulator step by step, and explain what we're doing as we go.” Scope: local dependencies, unchanged Copter build, one disarmed instance at a time, state observation, stop and repeat. No firmware edits, arming, takeoff, new automated tests, product UI, remote publication or physical operation.

## Concept and prediction

Source is the recipe. Waf compiles it into the native `ardupilot/build/sitl/bin/arducopter` executable. The stock `sim_vehicle.py` launcher starts that executable and MAVProxy, the text ground console. The Copter executable runs both ArduPilot and the built-in multicopter simulation. Predicted result: one standard quad starts disarmed, sends heartbeats and simulated sensor/estimator state, then stops and starts again without changing flight source.

The `quad` profile resolves to the `+` physics model and stock `Tools/autotest/default_params/copter.parm` (see pinned `Tools/autotest/pysim/vehicleinfo.py`). GPS, IMU, compass, pressure and other sensor observations originate in the built-in SITL simulation. The estimator's fused position and simulator `SIMSTATE` truth are distinct messages. No external sensor-only autonomy is demonstrated; truth is present for observation/evaluation and no new autonomy consumer exists.

## Observed result

L02 execution and the learner explanation checkpoint are complete. Both launches used fresh run directories and the same unchanged binary/profile. Both reported mode `STABILIZE`, GPS fix type 6 / 10 simulated satellites, EKF3 GPS use on both IMUs and a healthy pre-arm status bit before shutdown.

| Run | Vehicle heartbeats (`1:1`) | Armed vehicle heartbeats | Shutdown/cleanup |
| --- | ---: | ---: | --- |
| 1 | 65 | 0 | Owned simulator terminated; launcher/console stopped; no session processes or SITL sockets remained |
| 2 | 83 | 0 | Same result after a fresh launch |

Ground-console heartbeats (`255:230`) are counted separately in the result JSON; they are not vehicle state. “Disarmed throughout” refers to all recorded vehicle heartbeats, not a continuous independently instrumented guarantee. No flight occurred.

## Exact environment and dependencies

[Environment/source manifest](environment.json) records the unchanged `Copter-4.7.2` commit `fb773567896014da007bca58358704d4a0d8516f`, branch `featherlane/dev`, all 21 recursive submodule pins, binary hash, compiler and SDK. This native disarmed qualification applies to macOS 15.7.7 (24G720), arm64, Apple Clang 17.0.0, uv 0.12.1 and uv-managed Python 3.12.12. It is not a qualification of hardware firmware or other macOS/simulator versions.

The local environment is `.local/l02/venv`. [requirements.lock.txt](requirements.lock.txt) freezes all 29 installed Python packages, including MAVProxy 1.8.75, pymavlink 2.4.50, empy 3.3.4 and gnureadline. Some large packages (including VTK and OpenCV) are transitive MAVProxy requirements; installation does not establish a perception capability. No Homebrew packages, hardware cross compiler, shell profile or system Python changes were made. uv's user-managed interpreter/cache remain outside the repository.

The official [macOS setup guide](https://ardupilot.org/dev/docs/building-setup-mac.html), pinned `Tools/environment_install/install-prereqs-mac.sh`, `BUILD.md`, `sim_vehicle.py` and terminal helper were inspected. The broad installer was not run: it also updates Homebrew, changes Python links/shell profiles and offers a hardware toolchain. `docs/CODEX-NAVIGATION-GUIDE.md` was checked and is absent.

## Reproduce the setup and build

From the project root, only when creating a new environment (do not recreate an environment being used by a running build/session):

```sh
uv venv --python 3.12.12 .local/l02/venv
uv pip install --python .local/l02/venv/bin/python \
  -r docs/evidence/l02-basic-sitl-setup/requirements.lock.txt
```

Use the existing pinned checkout; do not update upstream or submodule revisions. Configure/build:

```sh
cd ardupilot
../.local/l02/venv/bin/python waf configure --board sitl --no-submodule-update
../.local/l02/venv/bin/python waf copter -j4
cd ..
file ardupilot/build/sitl/bin/arducopter
```

Configuration and build both exited 0. [Build summary](build-summary.txt) records the actual final output. Full configure/build logs remain in ignored `.local/l02/`. The linker warned that `-ld_classic` is deprecated; build still succeeded. Waf generated `ardupilot/build/sitl/libraries/GCS_MAVLink/include/mavlink/v2.0/all/version.h`. Editor include-path configuration was not changed or qualified.

## Reproduce a disarmed launch

From the project root, choose a new run directory, with no other controller/instance using the endpoints below:

```sh
l02_root="$PWD"
l02_run_dir="$l02_root/.local/l02/manual-01"
mkdir -p "$l02_run_dir"
env -u DISPLAY SITL_RITW_TERMINAL=bash TMPDIR="$l02_run_dir/" \
  PATH="$l02_root/.local/l02/venv/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
  /usr/bin/script -q "$l02_run_dir/console.log" \
  "$l02_root/.local/l02/venv/bin/python" \
  "$l02_root/ardupilot/Tools/autotest/sim_vehicle.py" \
  -v ArduCopter -f quad -N --use-dir "$l02_run_dir" \
  --no-extra-ports --out 127.0.0.1:14550 \
  --mavproxy-args=--default-modules=log,param,mode,arm,rc,cmdlong,output
```

`-N` skips rebuilding; each new directory starts with stock parameters and independent EEPROM/log state. `DISPLAY` is unset to select the inspected terminal helper's bash path; helper scripts stay inside that run directory. `script` captures the interactive terminal. The explicit console module list avoids GUI/terrain-download modules. Inspect local MAVProxy startup scripts before reproducing with a different account: `~/.mavinit.scr` and `~/.mavproxy/mavinit.scr` were absent in this execution; no private startup file was read or edited. No GUI map or application UI is needed.

In the MAVProxy prompt, use observation commands:

```text
status HEARTBEAT
status GPS_RAW_INT
status SYS_STATUS
status EKF_STATUS_REPORT
status GLOBAL_POSITION_INT
arm list
```

`arm list` only lists the configured arming checks; it does not arm or bypass checks. Never enter `arm throttle` during L02. Initially sensors/estimator are still settling; wait for actual EKF/GPS evidence. A simulated GPS fix alone is not a position-flight qualification. A temporary `set streamrate 4` in run 1 requested telemetry at the existing default rate; it did not alter flight parameters.

Endpoints observed: MAVProxy connects to TCP `127.0.0.1:5760`; simulated RC uses UDP `127.0.0.1:5501`; telemetry is forwarded to UDP `127.0.0.1:14550`. Stock SITL actually binds TCP `*:5760`, `*:5762`, `*:5763` and UDP `*:5501`; `--sim-address=127.0.0.1` does not restrict these listener binds. This is not a localhost-only network-isolation claim. No firewall or remote service was changed. The advertised Irlock port 9005 does not prove a qualified target sensor.

## Stop only this session

In another terminal, identify the executable PID and verify its full command belongs to this run (the actual execution additionally matched `SIM_VEHICLE_SESSION` against captured process evidence):

```sh
ps -axo pid,ppid,command | rg 'arducopter|sim_vehicle.py|mavproxy.py'
# Substitute only the verified PID of this run's arducopter:
kill -TERM <owned-arducopter-pid>
```

Then press Ctrl-C in the launch terminal to close MAVProxy/the launcher. The stock launcher's final cleanup uses session-scoped psutil because psutil is installed and `DISPLAY` is unset. Stopping the binary first avoids that cleanup force-killing the active simulator. Do not use broad `pkill` commands. Termination is process cleanup, not a landing command or a claim of application-level log flush.

Check that this session has no remaining processes and no SITL listener remains:

```sh
lsof -nP -iTCP:5760 -iTCP:5762 -iTCP:5763 -iUDP:5501
```

No output with exit 1 means lsof found no matching sockets. Preserve another task's processes if any are found. Repeat with another empty directory such as `manual-02`.

## Evidence and limitations

The detailed actual run results and heartbeat counts are recorded in [run-results.json](run-results.json). Captured [run 1 console](run1-console.txt) and [run 2 console](run2-console.txt) retain startup, state queries and shutdown, with terminal escapes removed and whitespace/line endings normalized. Raw `.tlog`, `.tlog.raw`, parameter/EEPROM files, passive JSONL observations, process/session IDs, endpoints and cleanup records remain under ignored `.local/l02/run1/` and `.local/l02/run2/`. Passive observation used pymavlink on the forwarded UDP stream; it sent no commands. These are manual experiment artifacts, not new automated tests or test scaffolding.

Initial launch failed on missing `gnureadline`; the failure and scoped install are retained in `.local/l02/startup-attempt01/console.log` and `gnureadline-install.log`. The failed instance was stopped by stock session cleanup before retrying. An unexplained local venv reset removed packages during compilation; the recorded lock restored all packages, imports were verified and subsequent successful sessions used the frozen environment. Cause was not established. Raw dependency install/restore logs are retained.

MAVProxy reported four MAV parsing errors during startup in each successful run; these must not be described as a zero-error link. They did not prevent continuing heartbeat/state reception. Exact cause remains uninvestigated; vehicle `SYS_STATUS` communication/error counters were zero in the observed samples. Terrain data was not downloaded/qualified (`TERRAIN_REPORT` had pending requests and zero loaded); no terrain-navigation claim is made. `EXTENDED_SYS_STATE` was not observed by the chosen default stream, so no touchdown claim is inferred. Disarmed logging is disabled in the stock profile; retained MAVLink telemetry/console logs are the evidence here.

Observed health/pre-arm flags apply to the disarmed stock state at that moment. No arm command, actual arming acceptance, takeoff, hold, landing, navigation-performance measurement, custom firmware behavior or independent external verification occurred. P01's flight gate remains open. L03 is next, subject to its own selected scope; it was not started.

## Documentation checks

[Execution summary](execution-summary.json) records verification and limits. The canonical registry, generated L02 card/master plan, roadmap, direction and repository status were updated consistently. The existing learning workflow was regenerated through the installed Archify skill: validation, delivery, strict artifact and browser gates passed with fresh ignored receipts under `.archify/l02-learning-progress/`. Desktop HTML and final static SVG captures were inspected; the durable SVG remains in `docs/assets/learning/` with editable JSON in `docs/phases/`. No new architecture or approval was introduced. `git diff --check` passed; firmware source stayed clean at the original pin.

## Saving the phase record

On 2026-10-31, after reviewing which files belong in Git, the user said “And let's do that and then kick off the CO3 in new track,” referring to committing/pushing L02 and starting L03 in a new chat. The scoped publication branch is `codex/l02-sitl-setup`. It contains maintained documents, the learning diagram/source and selected build/run evidence; the firmware gitlink stays unchanged. Local dependencies, executable, raw telemetry and temporary browser evidence remain ignored. The pre-commit audit of the frozen Python dependencies found no known vulnerabilities; its raw output is retained under `.local/l02/`. Publication is separate from flight qualification and does not approve UI/architecture or start L03 here.

## Rollback and learning checkpoint

Stop the owned session as above. Keep the source/submodule pin unchanged. The local Python environment, run directories and generated `ardupilot/build/` can be removed or Waf-cleaned later when unused; they are ignored and reproducible. Preserve evidence before removal. This phase did not edit user profiles, credentials, other checkouts or firmware source. The simulator execution itself made no commit or push. After the learning discussion, the user authorized saving and publishing these project records on a dedicated branch before starting L03 in a new chat.

Checkpoint completed through follow-up discussion in this chat on 2026-10-31. The learner described C++ compilation, Software in the Loop, simulated sensor feedback and the ground console. Follow-up explanations clarified that `arducopter` runs ArduPilot with simulated physics/sensors, `sim_vehicle.py` launches the session, MAVProxy observes/sends commands, and a successful launch establishes a running communicating program without proving flight. The learner then restated SITL as the setup and successful launch as starting the software. This is a guided understanding checkpoint, not an independent examination.
