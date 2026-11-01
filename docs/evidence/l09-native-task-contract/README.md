# L09 — admit one typed coordinate task

Status: native builds, final-source manual admission and retained-L08 rollback verified; guided checkpoint complete. L09 remains local/uncommitted and unpublished. AI-assisted C++ and documentation. No flight execution or publication authorized in L09.

## Concept and prediction before the run

A typed task is data with an explicit meaning for every field: coordinate reference, units, version, ID and limits. Acceptance means the native component retained one validated request; it does not mean navigation began. A correctly formatted number may still use the wrong reference, exceed limits, lack navigation prerequisites or come from an unaccepted source.

Prediction: the existing MAVProxy `command_int` sends our `USER_1` request into the SITL-only receiver. A valid nearby 3 m-above-home task reports `accepted kept=1`; invalid examples report specific reasons and keep the retained ID unchanged. An identical repeat reports `duplicate`. The vehicle stays disarmed and no goal is installed into GUIDED or a controller.

## Contract and entry point

[Exact admission contract](admission-contract.json). This is a project-local experimental meaning for the already defined user command `MAV_CMD_USER_1` (31010), not a supported stock mission command or a new MAVLink dialect. COMMAND_INT is mandatory; the LAT/LON_INT frame is 6. Latitude/longitude are degrees × 1e7, while altitude is metres above the admission-time home.

```text
command_int GLOBAL_RELATIVE_ALT_INT USER_1 0 0 1 1 1 1 -353632172 1491652374 3
```

The four parameters are version, task ID, speed limit (m/s) and arrival radius (m). The next fields are latitude, longitude and height above home. Limits for this teaching slice: horizontal distance <=20 m from estimated home, height [0.01,10] m, speed (0,2] m/s and radius [0.5,2] m.

Path: MAVProxy → COMMAND_INT → stock GCS dispatch → Copter `handle_featherlane_admission()` → `FL_TaskAdmission::admit()` → RAM task + stock COMMAND_ACK/STATUSTEXT. `FL_Status` retains its L08 observation role.

The native component has Request, Context and accepted Task types. Request version/ID remain wire floats until validation, preventing unsafe conversion of nonfinite/out-of-range values. The stored Task has a bounded uint16 ID, centimetre-resolution above-home Location, requested speed/radius and a copy of home. Invalid requests do not overwrite it. One task slot remains occupied until process restart; no generalized mission queue or execution state machine is added.

## Necessary source slice

| File | Role |
| --- | --- |
| `libraries/FL_TaskAdmission/FL_TaskAdmission.h` | Typed request/context/task, results and one RAM slot. |
| `libraries/FL_TaskAdmission/FL_TaskAdmission.cpp` | Bounded validation, idempotency/conflict/busy handling and explicit reason names. |
| `ArduCopter/Copter.h` | Owns one admission component in SITL only. |
| `ArduCopter/wscript` | Links its library only for board sitl. |
| `ArduCopter/GCS_MAVLink_Copter.h` | Declares the scoped receiver. |
| `ArduCopter/GCS_MAVLink_Copter.cpp` | Routes USER_1, supplies actual source/vehicle/home/EKF context and maps results to upstream ACKs. |

No controller, arming, set-mode or target-setting call is present in this path. Source system-ID filtering is a configured identity check; signing/authentication and adversarial qualification are not established here. The accepted goal is not execution authorization. Future L10 must revalidate home/reference changes, estimator resets, state and bounds before movement; restart clears admission state.

## Baseline, publication and rollback

L07/L08 were published with explicit user approval: project `09c3229e3ed4cb7d9a8998b1f85ec16def0448a8`, firmware `3f467d90be284654c5721ac3d94c26863f771275`. Remote branch SHAs matched and main stayed `c45c9e19ae279011d5779fa2669df3fac0f21a29`. L09 is isolated on local `codex/l09-native-task-contract` branches. Upstream remains Copter-4.7.2 `fb773567896014da007bca58358704d4a0d8516f`, with the same 21 recursive submodules; no upstream adoption.

The unchanged L08 executable is retained at `.local/l09/l08-arducopter`. L09 uses a separate `.local/l09/build/` output. Rollback selects the exact retained L08 executable with `sim_vehicle.py -N --vehicle-binary ...`; the source diff remains for review. Baseline USER_1 should be unsupported while the existing L08 status remains available.

No automated tests, snapshots or test scaffolding are created. Evidence uses actual manual submissions, passive telemetry recording, native build/checks and retained outputs. Build performance and hardware timing remain unqualified.

## Actual observations

The initial full build succeeded in 1m5.538s. It retained 223 warnings in unchanged upstream paths. The focused rebuilds succeeded; their remaining warning is the macOS linker’s `-ld_classic` deprecation. These are successful builds with retained warnings, not warning-free or performance qualification claims.

The initial and corrected sessions manually exercised normal admission, duplicate/conflicting/busy requests, version/ID/frame/coordinate/height/speed/radius/range checks, missing home/navigation, wrong stock mode, wrong source and transport. The source/binary identities and timeline keep each run separate. The final-run results below take precedence for the final source.

Wrong-source and nonzero-current submissions use a one-shot local pymavlink sender on TCP5762, because MAVProxy’s existing `command_int` handler hardcodes current/autocontinue to zero. It sends a single manually selected request and records its response; it is not a flight mission state machine or test suite. MAVProxy remains the producer for the normal examples. Its source is ignored locally under `.local/l09/submit-once.py`.

One nonzero-current request in run2 arrived while the operator had selected GUIDED. It correctly returned `vehicle` before reaching the flags check. That output is retained as `flags-while-guided.json`; a subsequent request in STABILIZE returned `flags`. This is validation-order evidence, not a missing-response success.

The exact retained L08 binary was selected for rollback. It continued producing L08 status and returned standard ACK `UNSUPPORTED` (3) for USER_1, with no L09 text. The rollback process was disarmed/on-ground, then deliberately stopped. Its launcher also logged an already-exited PID during cleanup; process/socket inventory is the separate cleanup evidence.

Guided learner checkpoint complete: learner identified request validation/rejection and the receive/return flow without movement. Clarification distinguished task ID from coordinates, payload validity from home/navigation/vehicle readiness, and the already-wired/observed RAM admission from an unused function. Accepted data is stored; the switch maps its result to a MAVLink acknowledgment. This records guided understanding, not independent examination.


## Storage-resolution correction

The initial run used a strictly positive height check. Source review found that sub-centimetre values could round to zero in the stored Location. Before the final run, the lower bound was made 0.01 m (one centimetre). The final incremental build and a fresh disarmed run exercise the corrected bound, repeat admission/rejection examples and confirm that rejected requests preserve the stored task. Initial source/binary hashes and outcomes are retained separately; the initial run is not represented as the final executable.


The final source also uses exact equality for the wire version field. Upstream `is_equal()` permits an epsilon tolerance appropriate to measurements; protocol version 1 instead requires exactly representable `1.0f`. Run3 checks the fractional value `0.99999994`, the sub-centimetre height and the normal admission/rejection cases against these final bytes. Run2 remains evidence of the height correction before this exact-version change.


## Result mapping and evidence

| Native result | Standard COMMAND_ACK |
| --- | --- |
| accepted, duplicate | ACCEPTED (0) |
| version, frame, flags | UNSUPPORTED (3) |
| vehicle, home, navigation, busy | TEMPORARILY_REJECTED (1) |
| source, ID, coordinate, height, speed, radius, range, ID conflict | DENIED (2) |
| COMMAND_LONG used instead of COMMAND_INT | COMMAND_INT_ONLY (8) |

[Source manifest](source-manifest.json) · [Scoped patch](task-admission.patch) · [Executable hashes](binaries.json) · [Initial build](build.txt) · [Final build](build-final.txt) · [Configuration](configure.txt) · [Execution summary](execution-summary.json) · [Admission timeline](admission-timeline.csv) · [Raw manifest](raw-artifacts.json) · [Selected parameters](selected-parameters.txt) · [Cleanup](cleanup.json).

The run console/launch pairs and direct-submission JSON records accompany the summary. Original logs, telemetry and helpers remain ignored in `.local/l09/`; copied transcripts have trailing spaces removed, while applicable patch context is preserved.

Scope limits: this establishes selected manual admission outcomes while disarmed in local native macOS SITL. Armed-state rejection is source-inspected but not exercised by arming a vehicle. There is no signing/authentication, general command replay/mission queue, task persistence, reset-safe execution, hardware/timing bound, target motion, perception or combined-failure qualification. The simulated telemetry stream may contain truth messages; admission reads only stock home/EKF/mode/arming context, and the displacement summary uses estimated GLOBAL_POSITION_INT. P01/P03 broader gates remain open; L10 has not started and L09 is not published.


## Run3 observations before style cleanup

Final source produced 22 admission reports: one acceptance, two duplicate acknowledgments and 19 rejections across the manually chosen examples. Every report after the initial acceptance retained task 1. The fractional version `0.99999994` was rejected; the early otherwise-valid request was rejected for unavailable navigation. Sub-centimetre height was rejected both before and after acceptance. The normal 3 m task was accepted after EKF/GPS readiness. The two TCP5762 submissions separately returned `source` and `flags`; the remaining commands were typed into MAVProxy. [Final console](run3-console.txt) and [launch command](run3-launch.zsh) retain the actual inputs and responses.

All 93 observed vehicle heartbeats over 88.04s were disarmed; all received extended states were on-ground. Estimated horizontal position varied at most 0.0144m from the first valid estimate, maximum reported horizontal speed was 0.0283m/s, and relative altitude ranged from -0.002 to 0.006m. These small on-ground estimate variations are distinct from executing the accepted 3m-height goal. This is sampled evidence plus source inspection, not an armed flight qualification.

The rollback run retained 40 disarmed STABILIZE heartbeats across 37.04s, seven L08 status reports, zero L09 reports and one USER_1 ACK UNSUPPORTED. Its byte hash matched the retained L08 original. All four owned sessions (three development observations and one rollback) were stopped using fresh disarmed/on-ground telemetry; final cleanup inventory is retained. No broad performance/reliability or failure-campaign claim follows from these disarmed runs.


## Repository-style follow-up

The user requested following the repository’s coding conventions when reviewing `Context`. The Copter handler now zero-initializes `Request`/`Context` and assigns named fields individually, following the existing MAVLink message-building pattern and GNU C++11 baseline. Each original field binding and condition is preserved. This also wraps the status call and aligns its function continuation; no admission contract/policy was changed.

The incremental native build and whitespace check passed. Manual SITL scenarios were not rerun for this style-only adjustment. [Observed patch](observed-task-admission.patch) identifies the bytes exercised by run3; [current patch](task-admission.patch), [style receipt](style-followup.json), [build output](build-style-followup.txt) and updated source/binary manifests distinguish the subsequent build. Both binaries are retained locally; L09 remains unpublished and its learning checkpoint is complete.

The user subsequently clarified visual spacing in the result switch. Blank lines now separate the logging, type alias and switch, and separate groups that return different MAV_RESULT values. Case-label alignment follows the existing Linux-style formatter settings. This last edit was verified to change whitespace only; no rebuild or simulator rerun was needed for added blank lines. The current patch/hash includes it.

At the user’s request, short repository-style comments now explain the admission guard groups, wire units and bounds, home/navigation prerequisites, duplicate/conflict handling and retained home reference. Blank lines separate checks. This follow-up was verified to change only comments and whitespace; executable code and prior behavior are unchanged. No build or simulator rerun was needed for comments/spacing only.

The checkpoint clarification follows the learner’s explanation of payload checking and the receive/return flow. L09 is already integrated and manually observed in SITL. Admission stores `_task` and sets `_has_task`; result mapping reports the outcome. No movement execution was added. L09 is complete locally; L10 remains unstarted, and no L09 publication is authorized.

The build-file style follow-up moves the two FeatherLane entries into a normal one-entry-per-line `sitl_libraries` list under an explicit `BOARD == sitl` condition. Library selection and ordering are preserved. The [incremental native build](build-libraries-followup.txt) and scoped whitespace check passed; current source/binary identities are updated. No simulator rerun or publication was performed for this build-list cleanup.

The requested readability refactor renames `r`/`c` to `request`/`context` and names the version/ID/height/speed/radius/home-distance bounds using file-scope `static constexpr` values and units. Values and validation behavior are preserved. The named version constant triggered the compiler’s float-equality rule, so its exact finite check now uses equivalent lower/upper comparisons. The [build](build-readability-followup.txt), source-equivalence review and whitespace check passed; [receipt](readability-followup.json) distinguishes this build from earlier manual observations. No manual SITL rerun or publication was performed for the refactor.


## Publication after the guided checkpoint

The user explicitly requested adding the repository-style convention to AGENTS.md, publishing L09 and continuing with L10. Firmware commit `39cf614d1aae2ee4acb93f9294ebf66178967acb` on `codex/l09-native-task-contract` identifies the six-file admission implementation and requested readability changes. Its remote branch SHA was verified before the parent gitlink publication. This is feature-branch publication, not a merge, release, upstream adoption or authorization to publish L10. Earlier local/unpublished statements above describe the observation/preparation stage.
