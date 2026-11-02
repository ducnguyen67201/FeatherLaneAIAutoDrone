# Core ArduPilot architecture

[Open the core diagram](../assets/architecture/ardupilot-code-stack.svg) · [Editable diagram source](ardupilot-code-stack.json) · [Master learning plan](../MASTER-LEARNING-PLAN.md)

This is the single maintained architecture for FeatherLane. It shows the native mission stack we intend to build inside our maintained ArduPilot-derived codebase and the upstream flight capabilities we reuse. The external console and optional perception supply requests and observations. Native C++ owns in-flight task progression and policy.

**Status:** ArduPilot/macOS, native mission ownership, upstream maintenance and mission-selected optional perception are confirmed directions. L08’s SITL-only status observer and L09’s experimental version1 admission-only contract are implemented, manually observed and published. L10 now locally implements/observes one known-goal execution through SITL-only ModeFeatherLane (mode31). Its guided checkpoint is complete after clarification. Native arrival/typed abort (L11), broader coordination/ingress and resource budgets remain future work. Read the [phase registry](../phases/registry.json) for current acquisition/build progress; source acquisition is separate from a qualified executable, custom firmware or a successful simulation. Consolidating this page does not change implementation or UI/architecture approval flags.

## L08 current implementation slice

The user explicitly selected the small native status component on 2026-10-31. The L08 row was shown before implementation. `FL_Status` is a SITL-only observer: Copter supplies actual stock mode/arming state at a nominal 1 Hz; a first/every-five-update report goes through stock `GCS_SEND_TEXT`/MAVLink to MAVProxy. The callback has no target, controller or motor-write interface. L08 itself adds no mission coordinator or mode; later L09/L10 slices are recorded separately below.

The [L08 record](../evidence/l08-native-status-slice/README.md) carries build, manual observation, resource notes and stock-binary rollback evidence. Phase authorization is not an approval of the entire detailed architecture. No new hosting, process or deployment placement is introduced; this component is compiled into the existing local SITL executable.

## L09 current admission slice

The user authorized local L09 after the separately published L07/L08 records. The proposed L09 diagram scope was shown before implementation. `FL_TaskAdmission` receives the project-local `COMMAND_INT / MAV_CMD_USER_1` contract through a SITL-only Copter GCS handler. It checks the configured GCS system ID, disarmed/on-ground STABILIZE state, actual home/EKF prerequisites, version/frame/units and bounded fields; then retains one RAM task or reports a rejection. Native result text uses stock MAVLink status and acknowledgments.

The final source’s [manual record](../evidence/l09-native-task-contract/README.md) includes 22 reports, stored-task preservation, fractional-version/sub-centimetre corrections, 93 disarmed heartbeat samples, and a return to the exact L08 binary. It exposes no execution/arm/mode/target/motor interface. Existing `FL_Status` still reports stock mode/arming. L10 revalidates references and current authority before executing admitted data. Detailed diagram/UI approval flags are unchanged; no new process/hosting/deployment placement is introduced.

## L10 observed execution slice

The user authorized L10 after publishing L09. The maintained core diagram showed the proposed scope before implementation. The [L10 record](../evidence/l10-native-known-goal/README.md) retains its exact seven-file firmware patch against published L09, successful native build and actual final-mode flight. USER_2 explicitly starts the retained task; the native adapter installs its goal and runtime speed limit, then delegates to inherited Guided position control. Upstream position/attitude/rate controllers and AP_Motors produce movement and individual outputs. Only the selected native mode runs.

Entry requires a qualified airborne stock GUIDED hover and valid authority/navigation/reference state. Generic Guided setpoint ingress and stock speed setters are disabled in this mode. Operator LAND exits through the stock lifecycle; reference/navigation guard fallback is source-inspected but not fault-injected. Guided-specific failsafe classification does not automatically apply. The adapter preserves admission-time home when converting the above-home goal; broader failure qualification remains open.

Final mode31 flight peaked at0.99m/s, completed an offline measured two-second dwell at7.93s and held another50.27s before LAND/disarm. This is external arrival evidence, not an onboard completion transition; L11 remains unstarted. Exact-stock rollback rejected USER_2/mode31 and all owned sessions stopped disarmed/on-ground. L10 feature-branch publication is authorized. The initial29/client RATE_ACRO label conflict remains separate evidence; installed MAVProxy displays final31 as `Mode(31)`. There is no new process, hosting or deployment placement.

## Module ownership

The diagram is a selected module/responsibility view, not an exhaustive call graph. Layer groupings are explanatory; arrows do not imply that every module calls only the layer beneath it. ArduPilot paths below refer to the selected source checkout, and must be checked against its pinned revision.

| Ownership | Component | Responsibility |
| --- | --- | --- |
| BUILD L08 | `libraries/FL_Status/` plus Copter scheduling/status glue | SITL-only state observer; stock flight authority retained. See L08 evidence for actual execution status. |
| BUILD L09 | `libraries/FL_TaskAdmission/` plus scoped Copter GCS handler | Local experimental v1 coordinate-task admission and RAM retention only; no execution. |
| BUILD native | Candidate `FL_Mission`, proposed `libraries/FL_Mission/` | Bounded task state, required-input validity, motion limits, completion and abort/continue policy. |
| BUILD L10 | `ModeFeatherLane`, `ArduCopter/mode_featherlane.cpp` plus scoped Copter integration | Local SITL known-goal execution; explicit start, reference checks, inherited Guided controller reuse and normal mode exit. |
| BUILD integration | Scoped ingress and status/logging | Validate/version requests and observations; report actual native state, rejection and transition reasons. L09 USER_1 admission and L10 USER_2 start are experimental scoped mappings; broader ingress remains proposed. |
| REUSE | `GCS_MAVLink`, Copter handlers | Supported protocol requests, mission transfer and telemetry. Acceptance is separate from achieved behavior. |
| REUSE | `AP_Mission`, stock AUTO/GUIDED/other modes | Stored mission facilities and stock execution choices. Only the selected mode owns flight execution. |
| REUSE | `AC_WPNav` and qualified avoidance path | Navigation/reference generation; obstacle avoidance additionally needs usable sensing, configuration and mode integration. |
| REUSE | `AC_PosControl`, `AC_AttitudeControl` | Follow references using estimated state and produce control demand. |
| REUSE | `AP_AHRS`, configured EKF and sensors | Estimated attitude, position, velocity and validity. External navigation needs an actual qualified estimate producer. |
| REUSE | `AP_Motors`, `AP_HAL` and selected backend | Motor mixing and platform/simulator output. |
| REUSE authority | Arming checks, manual override and configured failsafes | Retain upstream authority; qualify interaction with our task policy. |
| BUILD/INTEGRATE externally | Python/uv session API, React/MUI console, optional compute and evidence | Prepare requests, launch/clean owned simulation processes, produce bounded observations and display/record firmware state. |

## Mission inputs and execution

A mission declares its steps, coordinate destination or target rule, frame/origin, motion/operating limits, required capabilities, input-validity requirements, completion conditions and failure/terminal policy. Vehicle state and required observations continue to arrive during execution; they are not frozen configuration data.

- A coordinate/route task can run without a target detector. Suitable stored routes may use existing AUTO/AP_Mission behavior.
- An object-dependent step requires qualified acquisition/identity and spatial localization. Helicopter is one example target; arbitrary object recognition is not assumed.
- Mixed missions can navigate to a coordinate and then enable a target-dependent step. Missing unused perception does not block coordinate tasks; missing required capabilities reject or interrupt the relevant step.

The native coordinator validates and retains the accepted goal, rather than replacing the vehicle estimator or generating individual motor speeds. Navigation/avoidance chooses feasible references; position and attitude/rate controllers follow them; mixing/output drives the selected simulated vehicle. New measurements close the feedback loop. Arrival requires measured position, speed, clearance and dwell as appropriate, rather than a command acknowledgment alone.

Detailed teaching examples live under guides:

- [One mission, path illustration and ArduPilot code](../guides/mission-contract-and-path.md).
- [Simple request, bounded search and landing](../guides/mission-request-execution.md).
- [AI mission and smooth movement explanation](../AI-MISSION-AND-MOTION-DESIGN.md).

Search and landing-site assessment are additional capabilities; a successful approach-and-hold does not establish them. The guides are explanations of this core design, not alternative architecture versions.

## Native mission runtime

External tooling submits bounded operator/configuration input and the observations required by the active step. A qualified ingress checks source, frame, units, timestamps/clock conversion, sequence/reset behavior, quality/uncertainty, limits, active mode and authority. The native mission tick accepts usable data, advances the task and selects a feasible reference or the configured fallback. Firmware reports actual state and reasons to the console/evidence tools.

MAVLink is an integration option, not an automatic connection to a new mode. Stock GUIDED setpoints do not automatically feed our custom mode; the schema, receiver and acknowledgment/rejection contract need qualification. Determine whether existing messages suffice before choosing a custom dialect.

Native callbacks must be bounded and nonblocking. Keep heavy inference, browser calls, slow I/O and any separately qualified large estimator/planner outside critical callbacks. Native placement can remove a decision boundary; end-to-end latency benefits and scheduler impact remain unmeasured.

## Failure behavior and authority

A stale required target, invalid range, uncertain route or insufficient stopping space invokes the explicit policy for that active step. A static coordinate task does not inherit an unnecessary detector heartbeat requirement. If the same producer supplies required vehicle localization, its loss still matters.

UI/ground-link loss, observation-producer loss, GPS loss and invalid localization are distinct failures. Native execution may continue under its preauthorized policy only while its required inputs and vehicle conditions support it. Hold, return and landing depend on actual navigation/capability; never substitute fabricated state or hidden simulator truth. Reconnecting the browser observes the native task and cannot silently restart or re-arm it.

Existing arming restrictions, configured failsafes and manual override retain authority. A custom mode must initialize, schedule and exit correctly. Reusing libraries does not automatically inherit all AUTO/GUIDED behavior, obstacle avoidance or smoothing semantics.

## Local deployment

The initial flight runtime is our selected ArduPilot-derived SITL executable. Published L09 contains the L08 status observer and bounded task admission. Local L10 additionally executes one known goal through the SITL-only adapter alongside the reused flight stack. Native arrival/typed abort and broader mission coordination remain proposed. External local tooling supplies the console/API, owned-process lifecycle, optional perception and evidence. The browser is not required to keep the native control loop running.

| Placement | Intended role | Qualification status |
| --- | --- | --- |
| macOS | Development, tooling and first basic SITL qualification | Qualify the actual Mac, source pin and tools in the learning phases. |
| Instrumented simulator, preferably Gazebo | Later scene physics and configured sensors with the selected SITL build | Compatible simulator/plugin versions are selected and measured later. |
| Isolated Linux environment | Fallback if the required Mac tool/simulator combination cannot be qualified | Candidate placement; requires its own scoped setup. |
| SkyDive | Separate preserved screen/input demonstration | No qualified ArduPilot bridge is assumed. |

Keep the application API local/loopback and use one selected flight endpoint and active mode for a run. Optional hardware/companion deployment requires separate design and qualification; no cloud/fleet hosting is introduced by this core.

## Maintaining our code against upstream

1. Record upstream origin, commit and matching submodules, then qualify an unchanged flight baseline.
2. Keep native modules and scoped integration patches identifiable against that base; preserve the last qualified build/configuration.
3. Review an update on an integration branch, including changes to modes, navigation, estimation, scheduling, message handling, parameters and failsafes.
4. Resolve semantic and textual conflicts, rebuild and repeat affected qualification scenarios before adopting the new pin. A clean merge is not behavioral compatibility.
5. Retain actual timing/load, nominal/failure outcomes and rollback evidence. Use existing checks/manual observations; new automated tests require an explicit user request.

## Evidence and limits

The upstream source explanations were researched at revision [`363ab1b5efdb67a0d0ade62984685b6d44d0f40d`](https://github.com/ArduPilot/ardupilot/commit/363ab1b5efdb67a0d0ade62984685b6d44d0f40d). This is a research reference, not the qualified project version. Consult the actual source-acquisition record for the selected base.

Primary references supporting the reused responsibilities:

- [Stored mission facilities](https://github.com/ArduPilot/ardupilot/blob/363ab1b5efdb67a0d0ade62984685b6d44d0f40d/libraries/AP_Mission/AP_Mission.h), [AUTO execution](https://github.com/ArduPilot/ardupilot/blob/363ab1b5efdb67a0d0ade62984685b6d44d0f40d/ArduCopter/mode_auto.cpp) and [GUIDED execution](https://github.com/ArduPilot/ardupilot/blob/363ab1b5efdb67a0d0ade62984685b6d44d0f40d/ArduCopter/mode_guided.cpp).
- [Position/navigation responsibilities](https://ardupilot.org/dev/docs/code-overview-copter-poscontrol-and-navigation.html) and [attitude/motor control](https://ardupilot.org/dev/docs/apmcopter-programming-attitude-control-2.html).
- [Custom Copter modes](https://ardupilot.org/dev/docs/apmcopter-adding-a-new-flight-mode.html), [scheduling](https://ardupilot.org/dev/docs/code-overview-scheduling-your-new-code-to-run-intermittently.html) and [threading constraints](https://ardupilot.org/dev/docs/learning-ardupilot-threading.html).
- [Conditional BendyRuler avoidance](https://ardupilot.org/copter/docs/common-oa-bendyruler.html) and [external vehicle estimation](https://ardupilot.org/dev/docs/mavlink-nongps-position-estimation.html).

## Direction and diagram approval record

The user's 2026-10-31 decisions selected ArduPilot/macOS, native in-flight mission ownership, deliberate upstream maintenance, optional perception by mission and a learning-first implementation plan. The subsequent cleanup request selected one maintained core architecture and removed competing views from this folder. See [D13–D18](../DECISIONS.md).

This is the retained design baseline. Broader candidate modules/contracts/layout remain proposed; L08–L10 implementation is limited to the explicitly recorded slices above. Consolidation does not approve the whole design, hardware deployment or UI. Preserve actual approval source/date/scope when a detailed design is explicitly approved. Implementation progress belongs in the phase registry and evidence records.

## Documentation maintenance

Keep this README, locally generated `ardupilot-code-stack.html` and editable `ardupilot-code-stack.json` as the only files in this directory. The public static SVG is exported under `docs/assets/architecture/`; the HTML viewer and review receipts remain ignored. Task illustrations belong with guides/assets, learning diagrams with phase docs, and generated checks/receipts/history in ignored local working folders. Update this core instead of adding another competing overview. Generate and validate the core through Archify; retain fresh evidence outside this folder.
