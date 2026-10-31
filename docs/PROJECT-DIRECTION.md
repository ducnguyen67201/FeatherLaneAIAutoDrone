# Project direction

[Project home](../README.md) · [Roadmap](ROADMAP.md) · [Architecture](architecture/README.md)

Recorded 2026-10-31. This is the initial project direction, not evidence of a deployed system.

## Learning and implementation progression

The user selected small focused phases on 2026-10-31. The [master learning plan](MASTER-LEARNING-PLAN.md) is the execution entry point; `P01`–`P09` remain capability milestones. Start with source acquisition/orientation, basic SITL setup, one stock flight and a read-only source walkthrough. Learn a known-coordinate route, one speed change and measured stopping before adding native mission behavior. Instrumented Gazebo sensing, stock/native avoidance, the approved UI and optional perception follow in separate slices. Every phase keeps an observable result, narrow code scope, prediction, actual evidence and rollback. No implementation is started by producing these cards.

## Intended outcome

The operator chooses a mission, such as navigating to a GPS/local coordinate or acquiring an object and approaching it, reviews its limits and presses Start. The drone takes off, follows a continuously corrected route and stops at a configured distance from the destination. The UI shows actual state, planned motion and the reason for any stop. The eventual mission runtime should work locally without a cloud model or an open browser.

Target perception is optional and selected by the mission. A coordinate-only mission needs valid navigation but no target detector; an object-dependent step requires a qualified target definition, perception and spatial-goal source. Unsupported targets/capabilities are rejected explicitly. This is an extensible mission design, not a promise to recognize every object.

The initial visual demonstration uses the helicopter already present in FPV.SkyDive. It is a static scene object and a destination reference. Reaching it means approaching a nearby stopping region, not colliding with it. A repeatable, smooth approach matters before speed optimization.

Later simulation milestones introduce obstacles, GPS loss and ground-link loss. Mission completion after a fault is conditional on adequate navigation, vehicle health and a preauthorized policy. A controlled abort is the correct outcome when those conditions fail.

## ArduPilot foundation and reuse strategy

**ArduPilot is the project's core flight foundation.** The user's 2026-10-31 clarification calls for cloning its codebase and building selected application capabilities around it. L01 has acquired the [upstream source](https://github.com/ArduPilot/ardupilot) into the visible development folder `ardupilot/` (local branch `featherlane/dev`) and pinned `Copter-4.7.2` at `fb773567896014da007bca58358704d4a0d8516f` with matching submodules. The [L01 execution record](evidence/l01-source-and-orientation/README.md) distinguishes this source baseline from a qualified build. [L02 subsequently built the unchanged source and qualified two fresh disarmed native macOS SITL starts/stops](evidence/l02-basic-sitl-setup/README.md), with actual dependencies, telemetry and limitations retained. [L03 observed one stock simulated takeoff/hold/land and automatic disarm](evidence/l03-first-stock-flight/README.md). Its guided learner checkpoint is complete. [L04 traces that takeoff through the unchanged pinned source](evidence/l04-trace-one-command/README.md); the source work and guided learner checkpoint are complete. [L05 subsequently observed one stock known-coordinate flight](evidence/l05-one-coordinate/README.md), approximately 5 m north at 3 m above home, with a low-speed hold, landing/automatic disarm and guided checkpoint. [L06 repeated that same stock route with one reduced speed setting and restored the original afterward](evidence/l06-one-speed-change/README.md); the recorded comparison and guided learner checkpoint are complete. [L07 measured that stock approach against predeclared position/speed/two-second-dwell and data-quality conditions](evidence/l07-measure-arrival/README.md); its guided learner checkpoint is complete. [L08 then added and observed one SITL-only native status observer](evidence/l08-native-status-slice/README.md), with an isolated custom build and a preserved-stock rollback; its guided learner checkpoint is complete. This does not implement native task execution or a custom flight mode. P03 has only early stock-coordinate/speed/arrival and status-integration slices; its broader gate and P01’s remaining failure-handling work are still open. Follow the official [build guidance](https://ardupilot.org/dev/docs/building-the-code.html) when qualifying the actual machine.

The user subsequently confirmed native mission placement and maintenance of our own ArduPilot-derived codebase. Our bounded C++ in-flight mission logic/supervision will run inside the autopilot runtime, reusing upstream stabilization, state estimation, navigation/controllers, mission facilities and configured failsafes. External application code handles UI/session tooling, perception and evidence rather than owning the ArduPilot flight mission state machine. See the [native mission design and maintenance policy](architecture/README.md).

Keep custom changes identifiable against a pinned upstream commit/submodule set. A proposed native library and mode adapter (`FL_Mission` / `ModeFeatherLane`, candidate names) will own task state, observation freshness, mission limits and completion/abort policy while preserving upstream control and failsafe authority. Module split, mode registration and input/message contracts still need detailed qualification. Standard AUTO/GUIDED remain baseline choices; their message behavior is not automatically inherited by a custom mode.

Review upstream changes in an integration branch and requalify before adoption. Native placement can remove a process/message boundary for local decisions, but end-to-end latency gains remain unmeasured. Keep blocking perception, browser calls and slow I/O outside time-sensitive callbacks. This plan does not rewrite the flight controllers or authorize setup, implementation, remote publication or physical operation.

PX4 remains a reference alternative, not a second implementation track. ArduPilot was chosen by the user for this project; the choice is not a claim that either autopilot is universally better.

## Two simulation paths

| Path                                          | Control interface                                                                       | What it can establish                                                             | What it cannot establish by itself                                                            |
| --------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| FPV.SkyDive on macOS                          | Screen capture, HUD/target tracking and simulated key input through a dedicated adapter | A useful visual demonstration and operator workflow                               | ArduPilot integration, metric position, true obstacle sensing or a physical flight controller |
| ArduPilot SITL with an instrumented simulator | MAVLink commands/telemetry; simulator physics and sensor interfaces                     | Measured trajectories, vehicle behavior, collision outcomes and fault experiments | Real-hardware performance without a separate transfer program                                 |

**No supported ArduPilot-to-SkyDive bridge has been established.** The two backends must remain explicit and separate. Do not route motor commands from ArduPilot into the Steam game and claim equivalence without a separately qualified integration.

Ground-truth simulator state is acceptable for early controller debugging and evaluation. In a sensor-based autonomy demonstration it must be excluded from the navigation inputs and used only to score results.

## macOS development direction

Use macOS for the console and local development. P01 first qualifies a native ArduPilot SITL build for the actual machine and OS version. The official [ArduPilot Gazebo plugin](https://github.com/ArduPilot/ardupilot_gazebo/blob/main/README.md) documents Mac support on specified older releases and Intel/M1 systems; that is not qualification of this machine's current configuration.

The later L12 slice within P03 should qualify ArduPilot with Gazebo using a compatible version set. The [official plugin does not require ROS](https://ardupilot.org/dev/docs/sitl-with-gazebo.html). Add ROS 2 when sensor, localization or planner integration justifies it. If the required simulator/ROS combination cannot run reliably on this Mac, use an isolated Linux VM or an explicitly selected Linux host. Do not assume a macOS container supplies a working accelerated simulator GUI. No VM, remote host or service has been provisioned by this documentation task.

Pin the OS/architecture, ArduPilot commit, simulator version, plugins and dependency versions after successful qualification. Do not label guessed version combinations as supported.

## Proposed application stack

| Area                          | Initial direction                                                         | Reason                                                                         |
| ----------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Local control UI              | React, strict TypeScript, Vite and MUI; pnpm                              | Familiar controls and a small local operator application                       |
| Native flight mission runtime | C++ in our maintained ArduPilot-derived build | Local task state/policy using upstream navigation, controllers and failsafes |
| External API/session tooling | Python 3.12, FastAPI and Pydantic; uv | UI API, simulator lifecycle, perception integration and evidence; no authoritative ArduPilot flight FSM |
| ArduPilot adapter             | MAVLink; qualify pymavlink first in P01                                   | Match the selected autopilot's documented command interfaces                   |
| SkyDive adapter               | Reuse reviewed pieces of the existing native macOS prototype              | Preserve its working capture/input experience without pretending it is MAVLink |
| Optional target perception    | Mission-selected tracker/detector and target configuration              | Obtain a demonstrable baseline before adding a new model                       |
| Localization/planning         | Conventional estimation and planning; ROS 2 only when useful              | Keep responsibilities visible and avoid unnecessary infrastructure             |
| Run storage                   | Local files: mission/configuration JSON, event logs and selected captures | Reproducible experiments without a cloud/database requirement                  |

The native mission placement/C++ and maintained-code direction are confirmed along with ArduPilot/macOS. Remaining application packages and exact native integration details are proposed. No dependency installation or UI approval is implied.

## Control and trajectory design

Use separate feedback loops. ArduPilot runs stabilization and its selected navigation/controller loops. Our native C++ mission component supplies validated references and monitors their execution; external tooling delivers requests/observations and reports its state. The native extension reuses those controllers. Perception and any external localization publish timestamped observations. Use built-in planning/navigation first, with external route or trajectory generation only where a qualified capability gap requires it. The browser displays state and sends operator commands. A language model may assist with mission preparation, but is not required in the flight loop.

For an object-dependent mission, an image box gives a bearing-like observation, not a complete destination in meters. A usable spatial goal needs calibrated camera geometry, a depth/range estimate, the vehicle pose and correct coordinate transforms. A map also needs an origin and a way to localize the vehicle within it.

Plan a path through free space, then a time-dependent reference the vehicle can actually follow. Check speed, acceleration, braking distance and turning limits. Continue measuring position and tracking error while flying; a drawn line cannot compensate for missing state feedback. Controller, estimator and planner rates must be chosen from measured latency and dynamics, not copied from a racing paper.

ArduPilot's [BendyRuler](https://ardupilot.org/copter/docs/common-oa-bendyruler.html) is an initial candidate for local avoidance in documented modes with suitable proximity data. It is not a general semantic 3D planner. Some Guided S-curve/avoidance configurations limit how quickly position targets can change; qualify the chosen command mode before combining it with a rapidly updating external planner. See [Guided options](https://ardupilot.org/copter/docs/ac2_guidedmode.html).

## Meaning of connection and navigation failures

| Failure                          | Meaning                                                  | Intended response                                                                  |
| -------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Browser closed / UI disconnected | Operator view unavailable                                | Local runtime continues only under its already authorized mission policy.          |
| Ground radio/network lost        | Ground station cannot communicate with the vehicle       | Apply the configured link-loss policy; do not require a cloud response.            |
| Companion-to-autopilot link lost | Setpoints/supervision cannot reach the flight controller | Autopilot timeout/failsafe takes over; mission continuity is not assumed.          |
| GPS/GNSS unavailable             | Satellite position source absent                         | Use a qualified alternative estimate, otherwise abort through a feasible fallback. |
| Localization invalid             | Position/velocity estimate cannot be trusted             | Do not command blind position following or claim that Hold/RTL must work.          |
| Internet/DNS unavailable         | Remote services cannot be resolved/reached               | A fully local, already loaded mission should have no internet dependency.          |

The earlier phrase “DNS denial” is ambiguous. The roadmap covers both likely GPS denial and communication loss as separate problems. Actual DNS/internet loss is covered by removing cloud dependencies.

ArduPilot accepts [external non-GPS pose/velocity estimates](https://ardupilot.org/dev/docs/mavlink-nongps-position-estimation.html), but an appropriate sensor/estimator must produce them. `Guided_NoGPS` is an attitude-command mode, not automatic GPS-free position navigation. A 2D map and an IMU alone do not resolve this problem.

## Initial exclusions

No physical flight, equipment purchase, fleet management, cloud hosting, moving-helicopter pursuit or racing controller reproduction is included in the first eight phases. Hardware is a separate optional P09. Avoid expanding into a general drone operating system before the single-drone mission works.
