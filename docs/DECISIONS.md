# Decisions and open questions

[Project home](../README.md) · [Direction](PROJECT-DIRECTION.md)

Recorded 2026-10-31 from the user's project-planning request. Only choices explicitly made by the user are marked confirmed. Proposed designs are not approved, implemented or deployed by being documented here.

| ID  | Decision / assumption                                                                                            | Status and source                                                                                                     |
| --- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| D01 | Create a separate project under the Desktop workspace. Working name: FeatherLane AI Auto Drone.                  | User requested a new folder; exact display/folder name selected as a working name.                                    |
| D02 | Use ArduPilot as the autopilot.                                                                                  | Confirmed by the user's latest request.                                                                               |
| D03 | Develop from macOS.                                                                                              | Confirmed by the user. Actual machine/toolchain qualification is P01.                                                 |
| D04 | Develop phase by phase, starting with setup, a target-reaching demonstration and later lost-connection behavior. | Confirmed direction. The Pxx capability breakdown is proposed; D17 refines execution into small learning phases.                                                   |
| D05 | Provide a UI for controlling and inspecting missions.                                                            | Confirmed requirement. Visual design and implementation remain unapproved.                                            |
| D06 | First visual scene: FPV.SkyDive on Steam, static helicopter as destination reference.                            | Conversation context. Approach nearby without contact; no moving-aircraft pursuit.                                    |
| D07 | Preserve separate SkyDive and instrumented ArduPilot adapters.                                                   | Proposed architecture based on the absence of a qualified game/autopilot interface.                                   |
| D08 | Use local runtime/control rather than one slow model response per flight action.                                 | Proposed implementation direction addressing the user's observed latency concern.                                     |
| D09 | Prefer conventional autopilot control; add models for perception and estimation where necessary.                 | Proposed; reproducing MonoRace's direct motor controller is outside initial scope.                                    |
| D10 | Interpret earlier “DNS denial” as potentially GPS denial or communication loss.                                  | Unconfirmed wording. Plan covers both separately; literal internet/DNS loss is also considered.                       |
| D11 | External tooling/perception: Python/uv; console: React/MUI/pnpm; MAVLink integration; ROS 2 only if justified. | Proposed packages. Native flight mission placement/C++ is separately confirmed by D15; Python no longer owns that logic. |
| D12 | Keep the initial P00 task documentation-only. | Historical P00 boundary. D18 separately authorizes L01 source acquisition/orientation; application, flight and deployment work remain outside L01. |
| D13 | Treat ArduPilot as the core flight foundation; plan an upstream clone and pin, reuse built-in capabilities and add our application around them. | Confirmed by the user's 2026-10-31 clarification and request to update the architecture/docs. Scope is foundation and reuse/build direction; no clone, firmware change, setup or deployment performed. |
| D14 | Earlier proposal: external Python mission handlers/supervision. | Superseded by D15 on 2026-10-31. Standard AUTO/GUIDED remain available for baseline qualification; external Python no longer owns the planned ArduPilot flight mission lifecycle. |
| D15 | Maintain our own ArduPilot-derived code with native C++ in-flight mission logic/supervision; integrate upstream updates deliberately while retaining our changes. | Confirmed by the user's 2026-10-31 message: “This is plan and rule, and we would maintain it.” The accepted scope is placement and maintenance direction. Proposed library/mode names, contracts and new diagram layouts are not separately approved; no clone, firmware implementation or deployment is performed. |
| D16 | Mission-driven optional perception: support coordinate/route tasks without a detector and object-dependent steps using qualified target perception/localization. Helicopter is one example target, not the core mission definition. | Confirmed by the user on 2026-10-31: detection is optional; examples include going to GPS point A or detecting a helicopter and approaching it. Exact schema, supported targets and revised diagram layouts remain proposed; no implementation is recorded. |

| D17 | Organize work under one master learning plan with small focused phases and a shared phase-card interface; first acquire source, set up basic SITL, observe a stock flight and connect it to code. | Confirmed by the user on 2026-10-31: learn by doing and keep code small/focused. The Lxx cards refine existing Pxx capability milestones; detailed cards/layouts remain proposed. This task produces planning documents, not a clone, install or flight. |

| D18 | Execute L01 only: acquire official upstream source locally, pin its commit/submodules and learn the main folders. | User-authorized phase launch on 2026-10-31. Selected source baseline: `Copter-4.7.2`, `fb773567896014da007bca58358704d4a0d8516f`. [Observed execution](evidence/l01-source-and-orientation/README.md); no build/simulator/flight qualification or remote fork/push. Selection of this source revision is an implementation choice, not user approval of a qualified build. User follow-up on 2026-10-31 clarified that this is our development source, not temporary acquisition storage: moved the checkout to visible `ardupilot/`, with local branch `featherlane/dev`; exact baseline/submodules unchanged. |

The earlier documentation request did not approve the rendered layouts, full detailed architecture or UI. D18 authorizes only the subsequent L01 source/orientation work; the approval flags remain unchanged. See the [architecture approval record](architecture/README.md#direction-and-diagram-approval-record).

## L02 local setup authorization and observed result

On 2026-10-31 the user requested L02 with step-by-step explanations. This authorizes scoped local dependencies, the unchanged native Mac Copter build and disarmed simulator startup/observation/shutdown/repeat. [The L02 record](evidence/l02-basic-sitl-setup/README.md) retains the actual successful build, two fresh disarmed launches, cleanup and limitations. No flight, custom firmware, new tests, remote changes or UI integration was performed. Detailed architecture/UI approval flags remain false. At L02 completion the next proposed learning phase was L03; its subsequent execution is recorded below. P01 remains in progress.

## Repository publication

On 2026-10-31 the user requested publication on their GitHub profile, selected **public**, and then selected **Full project + linked firmware fork**. The project repository is [FeatherLaneAIAutoDrone](https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone); its `ardupilot/` submodule pins the [FeatherLaneArduPilot](https://github.com/ducnguyen67201/FeatherLaneArduPilot) firmware fork. The development branch remains `featherlane/dev` at the unchanged L01 baseline. This authorizes repository creation and source publication, without itself qualifying a build/flight or approving UI/architecture. The subsequent L02 qualification is recorded separately above. See the [repository guide](REPOSITORIES.md).

## Questions to resolve during the relevant phase

- **P01:** L02 records the actual Mac/toolchain and native SITL baseline; L03 records one supported stock flight sequence. Remaining source walkthrough and rejected/failed-connection handling still need their own evidence.
- **P02:** precise SkyDive spawn/settings, input mapping, repeatability limits and whether a terminal controlled stop is achievable through the available interface.
- **P03:** compatible simulator/autopilot versions, coordinate conventions and arrival thresholds; whether an isolated Linux runtime is necessary.
- **P04:** supported target definitions/models (helicopter as the initial example), representative imagery, camera calibration and depth/range source. “YOLO ready” does not prove this model supports the target.
- **P05:** built-in avoidance sufficiency versus an external planner, and the actual required obstacle geometries.
- **P06:** availability/type of map, initial localization, sensor payload, acceptable drift and GPS-denied mission limits.
- **P07:** exact link being lost and the permitted continue/abort policy for each mission state.
- **P09:** whether physical hardware is wanted at all; aircraft, payload, budget and operating context if so.

These questions do not block creation of the plan. Resolve them before the implementation steps that depend on their answers.

## Change policy

Update direction, roadmap, registry and diagrams together when a decision changes. Record approval source/date/scope for approved designs; do not treat approval of a diagram as implementation evidence. Keep future app implementation, external publication and physical operations scoped to their own authorization.

## L03 local stock-flight authorization and observed result

On 2026-10-31 the user requested saving/publishing L02 and starting “CO3 in new track”; the delegated new-chat handoff identifies this as L03. This authorized one bounded local stock SITL flight, with explanation before actions. On local branch `codex/l03-first-stock-flight`, unchanged Copter-4.7.2 took off to 3 m in GUIDED, held for a declared five-second observation, then landed in LAND and automatically disarmed. [L03 evidence](evidence/l03-first-stock-flight/README.md) retains command acceptance separately from achieved movement, the early unready prearm result, four startup parsing errors, raw-log manifest and clean owned-session shutdown. The flight exercise and guided learner explanation checkpoint are complete. On 2026-10-31 the learner identified observed telemetry, including height near 3 m and vertical speed, as evidence; follow-up clarified in-air/on-ground state and automatic disarming. This records guided understanding, not independent verification. P01 remains in progress and L04 has not started. No firmware/parameter changes, new tests, product UI, remote changes or physical operation were performed. UI/architecture approval flags remain false.

On 2026-10-31, after confirming understanding of the launcher/MAVProxy/telemetry flow, the user asked to push the L03 files and move to the next phase. This authorizes committing and pushing the curated L03 record on `codex/l03-first-stock-flight`, followed by the scoped L04 read-only source walkthrough. It does not authorize merging/updating `main`, publishing L04 changes, another flight or firmware changes.

## L04 read-only command walkthrough

Following the user’s 2026-10-31 request to publish L03 and move to the next phase, L04 traced the observed GUIDED `takeoff 3` through the pinned C++ receiver, mode/target setup, estimator feedback, position/attitude controllers, motor mixer and SITL output/physics boundary. [Source-linked evidence](evidence/l04-trace-one-command/README.md) distinguishes static source inspection from a runtime function trace. No firmware edits, rebuild, new flight, debugger, new tests or runtime instrumentation were performed. The read-only walkthrough and guided learner checkpoint are complete. On 2026-10-31 the learner identified read_inertia/AHRS state reads and AP_MotorsMatrix mixing; guided clarification distinguished estimation from feedback control and established that both run inside ArduPilot. This is not an independent examination. At walkthrough completion L05 had not started and L04 had not been committed or published; P01 remains in progress. UI/architecture approval flags remain false.

On 2026-10-31, after the guided checkpoint, the user explicitly asked to push L04 to its branch and start L05. This authorizes the completed L04 record’s commit/push followed by one scoped local stock coordinate-flight exercise. It does not authorize a main-branch merge/update, L05 publication, firmware edits or physical operation.

## L05 one stock coordinate flight

After the user’s 2026-10-31 authorization to publish L04 and start L05, one fresh unchanged stock quad flew in GUIDED to latitude -35.3632172°, longitude 149.1652374°, 3 m above home. [L05 evidence](evidence/l05-one-coordinate/README.md) retains the predeclared frame/goal/bounds, accepted COMMAND_INT DO_REPOSITION, measured movement, five-second low-speed hold, landing/automatic disarm and clean owned-session shutdown. The guided learner identified height above home; follow-up explained why an AMSL reference would change the height. Startup invalid positions were retained/flagged and excluded from derived distance; four parsing errors remain uninvestigated. No firmware/speed changes, new tests, UI, remote changes or physical operation occurred in L05. At exercise completion L05 was complete/local/uncommitted and L06 had not started. P03 has only this initial stock-coordinate slice; its broader gate and P01’s remaining failure-handling evidence are incomplete. UI/architecture approval flags remain false.

On 2026-10-31, after confirming understanding, the user explicitly asked to push the completed L05 files and continue to the next phase. This authorizes the L05 branch commit/push and the scoped L06 single-speed-setting comparison on the same route, with restoration of the original setting. It does not authorize main-branch merge/update, L06 publication, other tuning, custom firmware or physical operation.

## L06 one speed-setting comparison

Following the user’s 2026-10-31 request to publish L05 and continue, L06 repeated the identical global coordinate/3m-above-home request in fresh stock SITL. The sole intentional flight-setting change was WP_SPD10->1m/s; its pinned units, GUIDED consumption and parameter-save path were inspected. [L06 evidence](evidence/l06-one-speed-change/README.md) records lower measured peak speed and longer time to the same sampled near-goal/low-speed bounds, five-second hold, landing/disarm, restored WP_SPD10 and owned-session cleanup. Full parameter comparison exposed stock hover-throttle learning and flight-statistics updates; these were source-explained and retained rather than reset. The flight exercise and guided learner checkpoint are complete. On 2026-10-31 the learner identified acceleration and slowing as reasons measured speed varies and WP_SPD as a horizontal speed target; follow-up clarified that the graphed horizontal braking occurred at the destination while height was held, before the later landing. This records guided understanding, not independent examination. At exercise completion L06 was local/uncommitted and L07 had not started; P01/P03 broader gates remain open. No firmware/controller/acceleration tuning, new tests, UI or physical work occurred. UI/architecture approval flags remain false.

On 2026-10-31, after the guided checkpoint, the user explicitly requested pushing L06 and moving to the next phase. This authorizes the completed L06 branch commit/push followed by L07’s manual/log-based stopping/arrival observation, without custom controller/test-suite work. No main merge/update, L07 publication, unrelated tuning, custom firmware or physical operation is included.

## L07 measured stopping and arrival

After the user’s 2026-10-31 request to publish L06 and go to the next phase, L07 repeated the L05 stock configuration/coordinate without firmware parameter changes. [L07 evidence](evidence/l07-measure-arrival/README.md) fixes position/speed/height/state/freshness/gap and two-second dwell conditions before launch. First region entry occurred while too fast; the sampled rule completed later, with small overshoot and a continued held result before LAND/automatic disarm and clean shutdown. No MISSION_ITEM_REACHED was observed, consistent with the selected GUIDED position path; source inspection distinguishes the separate waypoint notification semantics from this measured rule. The flight/measurement exercise and guided learner checkpoint are complete. On 2026-10-31 the learner explained that the first region entry was too fast, a single low-speed sample was insufficient and continued held conditions were required. Guided clarification fixed the timing (all bounds at3.16s, two-second dwell completed5.16s), the speed threshold (<=0.3m/s, not exact zero) and dwell terminology. This records guided understanding, not independent examination. L07 remains local/uncommitted, L08 has not started and P01/P03 broader gates remain open. No custom controller/arrival runtime, new tests, UI or physical work was introduced. UI/architecture approval flags remain false.


## L08 authorization and status-only native slice

On 2026-10-31, the user asked to start the next phase and explicitly selected “L08 — add a small native C++ status component” rather than the later P08 campaign. This authorizes the scoped local native observer/build/scheduling/manual SITL work in the L08 card. The existing core diagram was updated and shown before C++ implementation; no separate detailed-design approval is inferred. The proposed slice copies stock mode/arming state and emits bounded status only, under SITL guards. Stock modes retain flight authority. L09 task admission and L10 custom movement remain separate. No L07/L08 publication, main update, upstream adoption or physical operation is authorized.


[L08 evidence](evidence/l08-native-status-slice/README.md) records the isolated successful build and one custom disarmed SITL session: 13 native status reports matched nearby stock heartbeat mode/arming state, including STABILIZE → GUIDED → STABILIZE. A separate run of the exact preserved stock executable retained 78.04s of disarmed heartbeats without the custom status. Both sessions stopped disarmed/on-ground, and no owned processes or selected sockets remained. The five-file custom source diff remains identifiable against the unchanged upstream/submodule baseline. Scheduler diagnostics use the stopped SITL clock and do not establish a host CPU timing bound. This is the first custom native implementation, limited to status observation; no native mission runtime or custom movement exists. The guided checkpoint is complete after clarification of observer versus stock mode/controller/mixer ownership. L07/L08 remain local/uncommitted, no push/merge was performed, and UI/architecture approval flags remain false.


## L07/L08 publication and L09 authorization

After completing the L08 checkpoint, the user explicitly selected “Yes—push L07/L08, then start L09.” This authorizes the completed L07/L08 feature-branch publication in the project and firmware repositories, including the exact firmware gitlink, followed by local L09 task-admission work. It does not authorize merging/updating main, publishing L09, physical operation or adopting new upstream source. Firmware is published before the parent gitlink; exact branch SHAs are checked after each push.


L07/L08 publication completed with remote SHA verification: project `09c3229e3ed4cb7d9a8998b1f85ec16def0448a8` and firmware `3f467d90be284654c5721ac3d94c26863f771275` on their `codex/l08-native-status-slice` branches. Main remained `c45c9e19ae279011d5779fa2669df3fac0f21a29`; the firmware stock branch remained at the pinned upstream base. L09 is isolated on local `codex/l09-native-task-contract` branches. Its authorized slice is versioned coordinate-task admission, with no arm/mode/target/motor actions or L09 publication. The proposed ingress/state scope was shown in the maintained core diagram before implementation.


## L09 observed task admission

[L09 evidence](evidence/l09-native-task-contract/README.md) retains the project-local version1 COMMAND_INT/USER_1 mapping and six-file native admission slice. The final source produced22 explicit admission reports with one acceptance/two duplicates and19 rejections; every report after acceptance preserved task1. Invalid/unsupported fields, unavailable navigation, wrong configured source/mode/transport and conflicting/busy state were manually observed without arming or issuing a navigation target. Review corrected sub-centimetre rounding and epsilon version acceptance; all earlier sources/outcomes remain separate evidence. The final session retained93 disarmed heartbeats and on-ground extended state, with about1.4cm maximum estimated horizontal variation. The exact L08 executable returned USER_1 UNSUPPORTED while reporting L08 status; all owned sessions were stopped with cleanup inventory retained. L09’s guided checkpoint is complete, L09 remains local/uncommitted and unpublished, and L10 has not started. P01/P03 broader gates and UI/architecture approval flags are unchanged.


## L09 publication, coding convention and L10 authorization

On 2026-10-31, after the guided L09 checkpoint and code-style revisions, the user requested that AGENTS.md require matching the surrounding author/repository conventions, then explicitly requested pushing the code and continuing with L10. This authorizes the completed L09 feature branches and exact firmware gitlink publication, followed by the scoped native known-goal execution slice in local SITL. It does not authorize updating/merging main, publishing L10, physical operation, unrelated flight capabilities or an upstream update. The durable coding rule covers descriptive names, named limits with units, useful nearby comments, spacing/list conventions, scoped diffs and actual verification.


## L09 publication and L10 observed native execution

L09 publication completed with exact remote SHA verification: project `d8afe552351f4f246822857c49a6fa37edbc0bc7` and firmware `39cf614d1aae2ee4acb93f9294ebf66178967acb`, both on `codex/l09-native-task-contract`. The project includes the durable AGENTS.md author/repository-style rule. Main and the stock firmware branch remain unchanged.

[L10 evidence](evidence/l10-native-known-goal/README.md) records the locally implemented seven-file SITL-only mode adapter, build and two actual native goal/hold/LAND/disarm sessions. The first used29, exposing an installed-client RATE_ACRO label conflict; the final fresh-source flight uses project-local31, displayed as `Mode(31)`. Final peak speed was0.99m/s; an offline sampled two-second dwell completed7.93s after start, followed by50.27s qualifying hold. Duplicate start installed no new goal, selected stock target/speed commands were rejected, and a consumed task did not restart after exit. The exact preserved stock binary returned USER_2 UNSUPPORTED and rejected mode31; all owned sessions stopped disarmed/on-ground with no selected sockets remaining.

This is native goal selection and controller reuse, not native arrival/completion: L11 owns arrival/typed abort and has not started. Reference/navigation fallback is source-inspected but not fault-injected; no timing gain, full failsafe equivalence, hardware qualification, UI integration or broader milestone completion is claimed. L10 remains local/uncommitted/unpublished on `codex/l10-native-known-goal`; its guided checkpoint is pending. Detailed architecture/UI approval flags remain false.


## L10 guided checkpoint and publication / L11 authorization

On 2026-11-02 the learner confirmed understanding after the native-mode lifecycle walkthrough and explicitly requested: “push it and continue to L11.” L10’s guided checkpoint is complete after clarification of native goal ownership, inherited controller reuse, stock takeoff and operator LAND. This authorizes L10 feature-branch publication in both repositories with exact gitlink, followed by local L11 arrival/dwell and one explicit operator-abort path. Main merge, L11 publication, hardware and unrelated capabilities remain outside scope.


## L10 publication and L11 observed lifecycle

L10 publication was verified at project `d0f30a8f1c33af2f54740fc2b0675f453e0d5ba2` and firmware `11573fb26ffe99022431a32d0b40502d03f9b02a`, with the exact parent gitlink. Main and stock source pins remain unchanged. Both current local branches are `codex/l11-native-arrival-abort`.

On2026-11-02 the authorized L11 slice added four-file native lifecycle integration against published L10. Its proposed scope was shown in the maintained core diagram before code. [Actual evidence](evidence/l11-native-arrival-abort/README.md) records native2000ms dwell/COMPLETE at7.79s after accepted start and29.76s continued sampled hold. A fresh operator USER_3 during movement selected stock BRAKE, reported ABORTED and completed a two-second sampled stop4.11s after acknowledgment, at least3.08m short of the goal. Duplicate/consumed requests did not restart or re-arm; explicit operator LAND/disarm ended both sessions. The exact preserved L10 executable returned USER_3 UNSUPPORTED, and all owned sessions stopped with cleanup retained.

COMPLETE is task state, not landing/disarm; ABORTED reports successful handoff, with stopping evidenced separately. No new controller, external authoritative FSM, automated tests, full failure campaign, hardware or L11 publication is introduced. Native guard/reset/fallback and blocked BRAKE branches are source-inspected, not fault-injected. L11’s guided checkpoint is pending; L12 has not started and broader P01/P03 gates remain incomplete.


## L11 guided checkpoint / publication and L12 authorization

On2026-11-02 the learner confirmed understanding after clarification of task-state completion versus GCS reporting, powered hover versus aircraft speed, and explicit next actions. The guided L11 checkpoint is complete. The user then requested pushing this work and continuing the next phase, authorizing L11 feature-branch publication with exact firmware gitlink, then local L12 instrumented simulator/world integration. Main merge, L12 publication, physical operation, AI/ROS/avoidance and unrelated changes remain outside this slice.


## L11 publication and L12 observed external simulator baseline

L11 publication is remote-SHA verified at project `56b32a2c6d10bc58a85ae4ebab4ff98520da3acc` and firmware `a00f32be2a91639c8dee1c41c09e1c5e5635d547`, with the exact parent gitlink. Both current local branches are `codex/l12-instrumented-scene`; firmware source and all21 recursive pins remain unchanged.

The authorized L12 local integration selected native headless Gazebo Sim8.10.0/physics7.5.0/DART6.19.5 in an isolated269-package conda-forge environment, plus official plugin `f116b03552d05c8d0b0bed5ed67033a1183121d1`. The existing stock Copter4.7.2 executable used its JSON model and official Iris QUAD/X profile; no L12 firmware changes were needed. A scoped CMake wrapper builds only the unchanged official actuator/state plugin; one plain world and manual launch scripts provide the integration. The proposal/core and local deployment diagram were shown before implementation.

[Actual evidence](evidence/l12-instrumented-scene/README.md) records disarmed clock/IMU/actuator exchange, stock takeoff3m, a nearby coordinate about5m north atWP_SPD1, sampled arrival at7.80s with31.83s subsequent hold, LAND/disarm, fresh disarmed scene connection and basic-SITL rollback. Peak speed1.05m/s is recorded against the1m/s target. Separately recorded Gazebo poses show the displacement; this shared simulated plant is privileged baseline input/evaluation, not sensor-only or independent physical validation.

The DART build omitted the official mesh base_collision; primitive leg/rotor collisions and level landing do not qualify body/obstacle contact. GUI/camera, avoidance/AI/ROS, native L11 transfer to the new plant, fault/reliability campaigns, scheduler bounds and hardware remain unqualified. No new automated tests or external authoritative flight FSM were created. The temporary Homebrew tap was removed; no tap trust or Gazebo formula was installed. The environment/source/raw logs remain project-local. L12 is local/unpublished with guided checkpoint pending; L13 has not started.


The learner subsequently identified Gazebo as the movement/measurement simulator and ArduCopter SITL as the control/estimation/output runtime. L12’s guided checkpoint is complete on2026-11-02. This does not authorize L12 publication or start L13.


## L12 publication / L13 authorization

On2026-11-02 the user requested pushing completed L12 and continuing the next phase, including the attached screenshot. This authorizes L12 feature-branch publication and the matching unchanged firmware reference, followed by local L13 one-obstacle sensor/observation work without dodge/control behavior. The screenshot attachment is unreadable through the supplied macOS TemporaryItems path (Operation not permitted), so image inclusion remains pending a readable attachment; no access-control bypass is attempted. Main merge, L13 publication and physical operation remain outside scope.
