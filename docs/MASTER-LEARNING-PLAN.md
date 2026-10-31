# FeatherLane master learning and implementation plan

[Project home](../README.md) · [Capability roadmap](ROADMAP.md) · [Phase registry](phases/registry.json) · [First-seven-phase diagram](assets/learning/learning-workflow.svg)

**DRAFT detailed plan, recorded 2026-10-31.** The user confirmed learning through small, focused phases. Detailed cards, future extensions and diagram layout remain proposed. L01 and L02 are complete. [L03](evidence/l03-first-stock-flight/README.md) observed one unchanged stock simulated takeoff to 3 m, a declared 5-second hold, landing and automatic disarm, followed by clean shutdown. L03 is complete; the guided learner checkpoint was completed in this chat on 2026-10-31 using observed height and vertical-speed telemetry, with flight-state/disarm clarification. The early unready check and startup parsing errors are retained. P01 remains in progress; L04 is proposed next and has not started.

**Next small phase: L04.** No implementation learning phase is active.

This is the execution entry point. `L01`, `L02`, and so on are small learning phases. Existing `P01`–`P09` references remain capability milestones in the roadmap and architecture; their numbers do not dictate the learning order. Master groups organize related results without turning a group into one large implementation task. A phase passing does not automatically complete its parent capability milestone.

## Begin with these seven small phases

| Small phase | What you do | What you learn |
| --- | --- | --- |
| [L01](phases/learning/l01-source-and-orientation.md) Get the source and identify the main folders | Create a dedicated upstream-derived checkout and record its source revision without changing flight behavior. | Source code, a checkout, a commit and a built executable are different things. |
| [L02](phases/learning/l02-basic-sitl-setup.md) Build and launch basic SITL | Run one unchanged ArduCopter SITL instance on the selected environment while disarmed. | SITL is the autopilot executable plus simulated sensors/physics; a 3D world can come later. |
| [L03](phases/learning/l03-first-stock-flight.md) Watch one takeoff hold and landing | Perform one simple stock simulated flight through the existing console. | A requested command, an acknowledgment and achieved movement are separate events. |
| [L04](phases/learning/l04-trace-one-command.md) Trace one flight command through the code | Follow one observed command from its receiver or active mode to navigation, control and motor output. | Mission, mode, navigation, feedback control and estimation have distinct jobs. |
| [L05](phases/learning/l05-one-coordinate.md) Fly to one known coordinate | Reach one nearby known destination using a qualified stock AUTO or GUIDED path. | A destination needs a frame, units, origin and altitude reference. |
| [L06](phases/learning/l06-one-speed-change.md) Change one speed limit and compare | Repeat the same route with one changed speed setting and explain the difference. | Speed limits influence travel time; acceleration and stopping remain separate constraints. |
| [L07](phases/learning/l07-measure-arrival.md) Measure stopping and arrival | Distinguish passing a waypoint from reaching a low-speed held destination. | Completion is a measured position, speed and dwell condition. |

The first stock simulation uses the minimum qualified SITL setup. Gazebo and instrumented sensors are introduced later, after movement makes sense. Use the existing console before building the application UI. Exact commands and versions are selected against the actual Mac and pinned source during the appropriate phase; current documentation does not certify a version tuple.

L01–L04 introduce no custom flight behavior. L05–L07 reuse stock flight behavior while changing or observing one thing at a time. An unfamiliar term should be explained through the visible experiment before its code is expanded.

## The shared phase interface

Every [phase card](phases/README.md) follows the same template:

1. One observable result and one concept to learn.
2. The minimum inputs, prerequisite evidence and source files to read.
3. A narrow change scope and a prediction of what should happen.
4. A short manual experiment using the selected qualified scenario.
5. Actual output/evidence, limitations and a route back to the known baseline.
6. A brief explanation of the result and the next small step.

Keep code focused on that result. Prefer one behavior, one selected mode/path and one scenario. Read upstream code selectively rather than rewrite control, estimation or motor mixing. There is no arbitrary line-count target: necessary integration plumbing is explained, while independent behavior is split into another phase. Future cards are bounded objectives; split them further if source/sensor/tool qualification reveals a second unfamiliar change.

Completion means the stated evidence exists. A later session can set `in_progress`, `ready_for_review`, `complete` or `blocked` with the actual reason/record. Understanding questions guide the explanation. Scope already authorized by the user can proceed, while existing explicit approval boundaries remain intact.

## Master groups and later small phases

### M01 Get a working baseline and understand it

Read the source, run unchanged SITL and explain one stock flight.

Track: `core`. Capability milestones: P01.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L01](phases/learning/l01-source-and-orientation.md) Get the source and identify the main folders | Create a dedicated upstream-derived checkout and record its source revision without changing flight behavior. | none |
| [L02](phases/learning/l02-basic-sitl-setup.md) Build and launch basic SITL | Run one unchanged ArduCopter SITL instance on the selected environment while disarmed. | L01 |
| [L03](phases/learning/l03-first-stock-flight.md) Watch one takeoff hold and landing | Perform one simple stock simulated flight through the existing console. | L02 |
| [L04](phases/learning/l04-trace-one-command.md) Trace one flight command through the code | Follow one observed command from its receiver or active mode to navigation, control and motor output. | L03 |

### M02 Learn movement with one change at a time

Fly to one coordinate, change speed and measure stopping using stock behavior.

Track: `core`. Capability milestones: P03.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L05](phases/learning/l05-one-coordinate.md) Fly to one known coordinate | Reach one nearby known destination using a qualified stock AUTO or GUIDED path. | L04 |
| [L06](phases/learning/l06-one-speed-change.md) Change one speed limit and compare | Repeat the same route with one changed speed setting and explain the difference. | L05 |
| [L07](phases/learning/l07-measure-arrival.md) Measure stopping and arrival | Distinguish passing a waypoint from reaching a low-speed held destination. | L06 |

### M03 Add our native mission behavior in small slices

Admit a coordinate task, execute it natively and report arrival/abort reasons.

Track: `core`. Capability milestones: P03.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L08](phases/learning/l08-native-status-slice.md) Add a small native status slice | Prove one bounded custom native component can build and report status while the stock flight mode remains active. | L07 |
| [L09](phases/learning/l09-native-task-contract.md) Admit one typed coordinate task | Accept or reject a bounded coordinate-task definition in the native component without initiating movement. | L08 |
| [L10](phases/learning/l10-native-known-goal.md) Execute one accepted native goal | Use the native mode adapter to execute one already accepted coordinate task in a clear scene. | L09 |
| [L11](phases/learning/l11-native-arrival-abort.md) Add native arrival and operator abort | Report measured arrival and execute one qualified operator-abort path with clear native reasons. | L10 |

### M04 Observe one obstacle then avoid it

Qualify a scene/sensor, prove stock avoidance, then integrate the selected native path.

Track: `core`. Capability milestones: P03, P05.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L12](phases/learning/l12-instrumented-scene.md) Connect one instrumented simulator scene | Run the qualified flight baseline in one simple instrumented scene, preferably Gazebo. | L11 |
| [L13](phases/learning/l13-observe-one-obstacle.md) Observe one obstacle sensor | See usable distance/proximity observations for one static obstacle before using them for control. | L12 |
| [L14](phases/learning/l14-stock-obstacle-avoidance.md) Qualify one stock avoidance scenario | Demonstrate one clear/blocked obstacle scenario using a documented supported stock mode and existing avoidance. | L13 |
| [L15](phases/learning/l15-native-avoidance-integration.md) Reuse avoidance in our native path | Connect the qualified avoidance path to our native task and repeat the same scene. | L14, L11 |

### M05 Add a small operator interface

Approve a working React/MUI preview, then connect the approved controls to native state.

Track: `core`. Capability milestones: P02, P03.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L16](phases/learning/l16-operator-preview.md) Show a minimal working operator preview | Present a focused interactive React/MUI preview for one mission before application UI integration. | L11 |
| [L17](phases/learning/l17-approved-console-integration.md) Connect the approved minimal console | Connect the approved controls to operator requests and firmware-reported state for one mission. | L16 |

### M06 Add optional object-based goals

Detect a supported target, localize it and reuse the known-goal approach.

Track: `object_capability`. Capability milestones: P04.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L18](phases/learning/l18-optional-target-acquisition.md) Recognize one supported target without moving | Qualify acquisition/identity for one chosen target class or reference in simulation. | L12 |
| [L19](phases/learning/l19-target-spatial-goal.md) Estimate one object stopping goal without moving | Produce a bounded metric stopping goal from target observations and a qualified range/pose source. | L18, L13 |
| [L20](phases/learning/l20-object-approach.md) Approach one confirmed static object | Use the accepted object stopping goal with the existing native approach/arrival machinery. | L19, L15 |

### M07 Explore bounded search and landing as separate extensions

Qualify search, landing-site evidence and landing separately; approach-and-hold does not prove these.

Track: `optional_extension`. Capability milestones: additional proposed discovery extension.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L21](phases/learning/l21-bounded-search.md) Search one bounded area | Visit a small declared set of observation viewpoints and terminate with found/not-found. | L20 |
| [L22](phases/learning/l22-landing-site-observation.md) Assess one candidate landing patch | Assess one bounded candidate ground patch without commanding a landing. | L20 |
| [L23](phases/learning/l23-qualified-site-landing.md) Land at one qualified simulated site | Execute and verify landing at one admitted static simulated site using qualified ArduPilot behavior. | L22, L15 |

### M08 Handle individual failures before combining them

Separate link failures and GPS-denied navigation, then retain repeatability evidence.

Track: `qualification`. Capability milestones: P06, P07, P08.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [L24](phases/learning/l24-one-link-failure.md) Handle one link failure at a time | Demonstrate distinct native outcomes for UI, ground and observation-producer link loss in separate runs. | L17, L11 |
| [L25](phases/learning/l25-external-pose-baseline.md) Qualify one alternative pose source with GPS available | Observe and integrate one selected alternative pose source before relying on it for GPS-denied movement. | L12, L11 |
| [L26](phases/learning/l26-gps-off-known-goal.md) Fly one known goal with GPS unavailable | Run the bounded known-goal mission using the qualified alternative navigation source. | L25, L11 |
| [L27](phases/learning/l27-repeatability-and-combinations.md) Repeat the qualified scenarios then combine failures | Run a fixed evidence campaign for only the capabilities actually qualified. | L15, L24, L26 |

### S Retained separate SkyDive demonstration

Preserve the prototype and separately qualify screen/input behavior; no ArduPilot bridge.

Track: `deferred_skydive`. Capability milestones: P02.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [S01](phases/learning/s01-skydive-prototype-review.md) Review the separate SkyDive prototype | Document reusable screen/input behavior and its limits without changing the prototype. | none |
| [S02](phases/learning/s02-skydive-demonstration.md) Integrate the separate approved SkyDive demonstration | Qualify one selected-region visual approach through the separate game adapter. | S01, L17 |

### H Optional hardware planning

Define a separately authorized hardware program after relevant simulation evidence.

Track: `optional_hardware`. Capability milestones: P09.

| Small phase | Narrow result | Prerequisites |
| --- | --- | --- |
| [H01](phases/learning/h01-hardware-program-definition.md) Define a separate hardware qualification program | Document a scoped hardware program before selecting any physical implementation work. | L27 |

The default next step is always the earliest unmet prerequisite in the selected track. After the baseline, branches can advance independently when their own prerequisites are met. Object acquisition is optional per mission; a valid coordinate-only mission does not need a detector. Search and landing are additional proposed capabilities and are not prerequisites for coordinate-and-hold learning. The SkyDive branch remains a separate, deferred demonstration, not a dependency of ArduPilot SITL. Hardware remains separately scoped optional work.

## Boundaries that carry into every phase

- Keep bounded in-flight mission execution/supervision native in our maintained ArduPilot-derived C++ runtime. External tooling supplies requests/observations and displays actual state.
- Keep browser rendering, heavy perception and slow model calls outside critical flight callbacks.
- Built-in avoidance requires qualified sensing, configuration and a supported/integrated mode. It is not enabled just because an obstacle is drawn in a world.
- Retain ground truth for scoring or a clearly labeled privileged baseline; do not pass it off as sensor-only autonomy.
- Before UI integration, show a working preview using the intended React/MUI components/theme and record explicit approval of that shown scope. Only L17 depends on L16 UI approval; early SITL learning does not.
- Use existing checks and manual observations. No new automated tests, snapshots or test scaffolding are authorized by this plan.
- Remote publication/pushes, purchases, remote resource changes and physical operations retain their separate authorization requirements. A phase plan is not execution evidence.

## Sources and reproducible documents

The canonical state/specification is [registry.json](phases/registry.json). This master page and the phase cards are generated from it and the two templates by [render-learning-plan.py](../scripts/render-learning-plan.py). The script only renders local documentation and the editable first-seven-phase diagram specification; it does not install tools, clone source, run a simulator, start agents or operate a vehicle. The generated pages stay linked from the maintained project documentation.

The user suggested `master-agreement-generator`. Its useful pattern here is one reusable template plus structured specifications and reproducible draft output. Its legal clauses, party roles and signature workflows are unrelated to this engineering plan. The shared phase-card template and JSON registry apply that pattern to learning tasks.

Official setup references were checked on 2026-10-31. Use the actual selected revision/platform instructions during execution, because some tutorial pages contain older commands:

- [ArduPilot source and Git](https://ardupilot.org/dev/docs/where-to-get-the-code.html).
- [macOS build-environment guidance](https://ardupilot.org/dev/docs/building-setup-mac.html).
- [Using SITL](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html).
- [Gazebo integration for the later scene phase](https://ardupilot.org/dev/docs/sitl-with-gazebo.html).
