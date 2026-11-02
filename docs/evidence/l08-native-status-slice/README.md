# L08 — native status observer

**Retention update — 2026-11-02:** generated CSV/TXT exports were removed at the user’s request. References below describe the original export provenance; retained summaries/figures and source/recording identities remain. See the [retention note](../README.md).

Status: custom build, manual disarmed observation and stock rollback check passed. Guided learning checkpoint complete. AI-assisted C++ and documentation; no flight claim.

## Concept and prediction recorded before the run

A class is a small C++ component that holds state and exposes methods. Our `FL_Status` receives a copy of the active stock mode and arming state. ArduPilot’s existing scheduler calls the Copter wrapper at a nominal 1 Hz. Every five invocations (and on the first invocation), the wrapper asks the existing MAVLink stack to send `STATUSTEXT`.

Prediction: MAVProxy displays `FL L08 tick=... mode=0 armed=0` in disarmed STABILIZE. After a manual stock GUIDED selection, later reports display `mode=4 armed=0`. Counter increments represent callback invocations, not an independent uptime clock. This demonstrates code linkage, scheduling and observed state; stock modes/controllers still own movement.

This is a SITL-only observer. It has no task admission, target setter, controller/motor reference, custom flight mode or perception. L09/L10 remain separate work.

## Files and entry point

| Firmware file | Role |
| --- | --- |
| `libraries/FL_Status/FL_Status.h` | Snapshot/counter state and read-only accessors. |
| `libraries/FL_Status/FL_Status.cpp` | Bounded update and report countdown; no dynamic allocation or I/O. |
| `ArduCopter/wscript` | Includes the new library for the `sitl` board only. |
| `ArduCopter/Copter.h` | Includes/owns the component and declares its callback under a SITL guard. |
| `ArduCopter/Copter.cpp` | Registers the 1 Hz low-priority callback, reads actual stock mode/arming and uses `GCS_SEND_TEXT`. |

The native entry is `Copter::scheduler_tasks[]` → `Copter::update_featherlane_status()` → `FL_Status::update()`. The return flag gates status publication. The MAVLink transport and MAVProxy display remain upstream facilities.

## Baseline and scope

Pinned upstream: Copter-4.7.2, `fb773567896014da007bca58358704d4a0d8516f`; 21 pinned recursive submodules. Custom work is on local `codex/l08-native-status-slice` branches in the parent and firmware repositories. Parent branch inherits L07 evidence/docs. After the guided checkpoint, the user explicitly authorized publishing completed L07/L08 on feature branches before L09. Main is unchanged.

The original executable remains at `ardupilot/build/sitl/bin/arducopter`; an exact retained copy is `.local/l08/stock-arducopter`. The custom build uses `.local/l08/build/sitl/bin/arducopter`. Build output is separate; the Waf configuration lock now points to the custom output directory, so always specify `--out` when rebuilding either tree.

No new automated tests, snapshots or test scaffolding were created. Manual SITL evidence and existing build/check facilities are used.

## Build commands

Run from `ardupilot/` (substitute the absolute workspace root for `$PROJECT_ROOT`):

```sh
../.local/l02/venv/bin/python waf configure --board sitl --no-submodule-update --out="$PROJECT_ROOT/.local/l08/build"
../.local/l02/venv/bin/python waf copter -j4 --out="$PROJECT_ROOT/.local/l08/build"
```

Scheduling: requested 1 Hz, priority 171, declared 100 µs allowance. That allowance is configuration, not a measured worst-case bound. Status uses the existing GCS queue; reception timing can differ from callback timing. Hardware performance and end-to-end mission latency are unqualified.

## Observation, resource notes and rollback

The isolated build completed successfully in 1m8.500s. The full build output (generated export removed) and configuration output (generated export removed) are retained. Copied build/configuration/console transcripts have trailing spaces removed for publication; original byte-for-byte logs remain under `.local/l08/`. The applicable patch preserves Git context-line prefixes, including blank context lines. There were 223 compiler warning records in upstream paths, including macro redefinitions and existing conversion/move warnings; no warning names an added FL_Status source. This is a successful build with warnings, not a warning-free claim.

The custom manual run retained 13 `FL L08` messages, tick 1 through 61, always stepping by five. Reception intervals were 4.996–5.005 s. Stock heartbeat observations covered 66.04 s and modes 0/4; all 71 vehicle heartbeat samples were disarmed. All received extended states were on-ground. Each custom report matched the nearest stock heartbeat’s mode/arming state (at most 0.409 s apart). STABILIZE → GUIDED → STABILIZE was requested manually; no arm, takeoff or destination request was sent.

```text
FL L08 tick=41 mode=0 armed=0
FL L08 tick=46 mode=4 armed=0
FL L08 tick=61 mode=0 armed=0
```

The upstream `@SYS/tasks.txt` interface was read via MAVProxy’s existing FTP module. The first read enabled task statistics in RAM; the second produced task details (generated export removed), including the new scheduled callback with zero reported time/overruns/slips. **Zero is not a host CPU measurement:** `AP_Scheduler` uses `AP_HAL::micros()`, and SITL’s stopped simulation clock is returned by `AP_HAL_SITL/system.cpp` while callbacks run. All task rows reported zero. No measured 100 µs worst-case bound, hardware qualification or mission-latency improvement is claimed. The custom update contains fixed state copies/counter/countdown operations and calls the existing bounded status queue at the report cadence. Further profiling belongs to a separately scoped measurement.

The custom executable file is 4,818,072 bytes versus 4,817,736 bytes for the retained stock binary (+336 bytes). File size includes build metadata/alignment and is not a runtime RAM measurement; Mach-O segment sizes round to the same values. SHA-256 identities are retained in [binaries.json](binaries.json).

Return to the retained stock executable with explicit `sim_vehicle.py --vehicle-binary ... -N`; this selects the baseline binary even while the working source contains the custom diff. Reverting the source is a separate action. The preserved stock executable produced 81 disarmed STABILIZE heartbeats over 78.04 s and zero `FL L08` messages. All received extended states were on-ground. Its source-original and retained-copy hashes match the recorded baseline. Both owned sessions were deliberately stopped only after fresh disarmed/on-ground telemetry; [cleanup evidence](cleanup.json) records no owned SITL processes or selected TCP/UDP sockets remaining. The scoped custom patch is retained for review.


## Exact manual entry points

The retained [custom launch command](custom-run-launch.zsh) selects the new binary explicitly. The [stock launch command](stock-run-launch.zsh) selects the exact retained original. Both launch upstream `sim_vehicle.py`, which starts the selected ArduCopter executable and MAVProxy. Commands below are typed into MAVProxy, not the C++ component:

```text
module load ftp
long SET_MESSAGE_INTERVAL 245 500000
ftp get @SYS/tasks.txt <local tasks-start.txt path>
mode GUIDED
ftp get @SYS/tasks.txt <local tasks-end.txt path>
mode STABILIZE
```

The first `long` requests on-ground state telemetry. The FTP commands read diagnostics. `mode` asks stock ArduPilot to switch its mode; `FL_Status` observes the result. Full typed paths and responses are retained in the custom console record. No firmware parameter-set commands were issued; reading task diagnostics enables the stock performance option in RAM only.

## Evidence and limits

- [Scoped five-file patch](native-status.patch) and [baseline/submodule manifest](source-manifest.json). The executable was built from the stock base plus the retained patch. The subsequently created firmware commit `3f467d90be284654c5721ac3d94c26863f771275` identifies exactly those five-file changes; the source manifest keeps both identities. Branch publication is not a qualified release.
- Custom console (generated export removed), [execution summary](execution-summary.json), [raw artifact paths/hashes](raw-artifacts.json), task statistics initialization (generated export removed) and task statistics (generated export removed). Stock console (generated export removed) is retained too. Raw passive MAVLink JSONL, tlog and session files remain under ignored `.local/l08/`.
- Observations are sampled telemetry and source/build evidence from one custom disarmed session; they do not qualify armed flight, hardware, another vehicle, failure behavior or a native mission contract. Simulator truth messages may exist in the raw stock stream; this status component consumes only the stock mode/arming values, not truth position.
- Startup connection refusal before the executable opened its TCP port and reconnect refusal after deliberate shutdown are recorded lifecycle events, not proof of fault recovery. No failed/rejected-connection campaign was performed; P01/P03 broader gates remain open.

Guided checkpoint completed after the learner’s follow-up explanation: removing `FL_Status` would retain movement/remote control and remove only its reports. The learner identified the addition as an observer/logger. Clarification distinguished the native C++ component from `GCS_SEND_TEXT`, which transports status through MAVLink; the component is not itself a GCS command. Stock flight modes choose movement behavior/targets, controllers calculate thrust/rotation demand, and `AP_Motors` mixes that demand into individual motor outputs. The initial answer remembered the mode update but needed this chain explained. This records guided understanding, not independent examination. L09 implementation has not started. The user subsequently authorized L07/L08 feature-branch publication; this does not authorize L09 publication.
