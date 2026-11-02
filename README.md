# FeatherLane AI Auto Drone

An incremental autonomous-drone project: select a destination, start a mission from a local control UI, and have the drone approach it using feedback. Later milestones add obstacle avoidance, GPS-denied navigation and operation after losing the ground connection.

**Direction recorded: 2026-10-31. Autopilot: ArduPilot. Development computer: macOS. Status: L01–L07 and guided checkpoints complete; L08 native status slice and guided checkpoint complete; L09 admission and checkpoint complete/published; L10 native goal and checkpoint complete/published; L11 native arrival/operator-abort and checkpoint complete/published; L12 Gazebo scene/checkpoint complete and published; L13 front-lidar observations/checkpoint complete and published; L14 stock stopping and guided checkpoint complete/published; L15 native stop integration manually observed locally, guided checkpoint pending; P01/P03 remain in progress.**

**ArduPilot is the core flight foundation, and our in-flight mission logic will live inside it.** We will maintain an ArduPilot-derived codebase with our own bounded C++ mission behavior, reusing upstream control, estimation, navigation, mission facilities and failsafes. External tooling handles the console, simulator sessions, evidence and separately qualified perception. P01 qualifies an upstream baseline before custom flight behavior; upstream updates are reviewed and requalified before adoption. See the [native mission design](docs/architecture/README.md) and [reuse/build responsibilities](docs/architecture/README.md#module-ownership). The separate SkyDive demonstration uses screen/input control; it is not powered by ArduPilot.

Missions can use supplied GPS/local coordinates or optional target perception. Helicopter recognition is one example capability, not a core requirement for every mission.

The first visual target is the static helicopter in FPV.SkyDive on Steam. Success means a controlled approach to a nearby stopping point, without touching the helicopter. Maximum speed, interception of moving aircraft and physical flight are outside the initial scope.

## Source repositories

[Project/application repository](https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone) · [ArduPilot firmware fork](https://github.com/ducnguyen67201/FeatherLaneArduPilot) · [Repository and clone guide](docs/REPOSITORIES.md)

The visible `ardupilot/` folder is a pinned Git submodule of our firmware fork. Develop firmware on `featherlane/dev`; upstream remains available separately for reviewed updates. Clone the project with `git clone --recurse-submodules https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone.git`.

## Start here

Start with the [master learning plan](docs/MASTER-LEARNING-PLAN.md). Work one small `Lxx` phase at a time; the older `Pxx` items below are capability milestones. The first four steps acquire source, launch unchanged SITL, observe one stock flight and trace its code. Gazebo, custom mission code, UI and perception follow in later slices.

- [Detailed AI mission and smooth approach design](docs/AI-MISSION-AND-MOTION-DESIGN.md) · [Editable Word document](docs/exports/featherlane-ai-mission-and-motion-design.docx)
- [Project direction and system boundaries](docs/PROJECT-DIRECTION.md)
- [Phase-by-phase roadmap and acceptance gates](docs/ROADMAP.md)
- [Core architecture](docs/architecture/README.md)
- [Control-console requirements](docs/UI-CONTROL-CONSOLE.md)
- [Decisions, assumptions and open questions](docs/DECISIONS.md)
- [Research, frameworks and existing prototype evidence](docs/RESEARCH-AND-BASELINE.md)
- [Phase status registry](docs/phases/registry.json)

## Capability milestones

| Phase | Target                                                                        |
| ----- | ----------------------------------------------------------------------------- |
| P01   | Clone/pin upstream ArduPilot and qualify its existing SITL control on macOS. |
| P02   | Build the initial control UI and repeat a continuous SkyDive target approach. |
| P03   | Fly measured missions in an instrumented ArduPilot simulation.                |
| P04   | Add optional object perception and spatial goals; helicopter is one example.   |
| P05   | Plan around obstacles, follow the route and stop near the destination.        |
| P06   | Navigate with GPS unavailable using an alternative position estimate.         |
| P07   | Handle ground-connection loss with a local mission runtime.                   |
| P08   | Evaluate repeatability and combined failures with retained evidence.          |
| P09   | Optional: qualify a physical drone through a separately approved program.     |

There are **eight software/simulation capability milestones and one optional hardware milestone**, each broken into smaller learning phases in the master plan. P00 is this documentation baseline. Each phase must pass its own gate before its result is treated as proven. P03 depends technically on P01; a Steam-game limitation must not indefinitely block instrumented simulation.

## What exists today

A separate SkyDive prototype exists at `/Users/ducng/Desktop/workspace/skydive-control-dogfood`. One saved run was visually reviewed as a continuous close approach. It does not establish reliable autonomous arrival, measured distance, collision avoidance, landing or repeatability. The current tracker follows a selected image region; it is not a verified helicopter detector.

This folder contains the project plan and the visible ArduPilot development checkout at [`ardupilot/`](ardupilot/) with preserved stock branch `featherlane/dev` and published status work on `codex/l08-native-status-slice` and published admission work on `codex/l09-native-task-contract`; L10 is published on `codex/l10-native-known-goal`, and L11 is published on `codex/l11-native-arrival-abort`, and current local native stop work is on `codex/l15-native-obstacle-stop`. [L01 acquired and recorded](docs/evidence/l01-source-and-orientation/README.md) the unchanged `Copter-4.7.2` source at `fb773567896014da007bca58358704d4a0d8516f`, including all 21 recursive submodule pins. [L02 built that unchanged source and qualified two fresh disarmed native SITL launches](docs/evidence/l02-basic-sitl-setup/README.md) on macOS 15.7.7 arm64. Both reported simulated GPS/EKF3 state and stopped with no owned processes or sockets remaining. The SkyDive prototype and `FeatherLaneFlight` remain separate and untouched. [L03 observed one stock simulated takeoff to 3 m, a five-second hold, landing and automatic disarm](docs/evidence/l03-first-stock-flight/README.md), then cleanly stopped the session. Its guided learner checkpoint is complete. [L04 traced the takeoff request through the pinned source](docs/evidence/l04-trace-one-command/README.md); its guided learner checkpoint is complete. [L05 reached one known GPS coordinate about 5 m north at 3 m above home, held, landed and disarmed](docs/evidence/l05-one-coordinate/README.md); its guided checkpoint is complete. [L06 repeated that route with WP_SPD reduced from10 to1 m/s and restored it afterward](docs/evidence/l06-one-speed-change/README.md); speed/travel comparison and guided learner checkpoint are complete. [L07 measured region entry, low speed and a two-second sampled arrival hold](docs/evidence/l07-measure-arrival/README.md), then landed/disarmed and cleaned up; its guided learner checkpoint is complete. [L08 added a SITL-only native C++ status observer](docs/evidence/l08-native-status-slice/README.md), built it separately, matched disarmed mode/arming reports against stock telemetry, and returned to the unchanged stock executable. Its guided learner checkpoint is complete. [L09 locally added typed coordinate-task admission](docs/evidence/l09-native-task-contract/README.md): final-source requests were accepted/rejected with explicit reasons and no movement; retained-L08 rollback was verified. L09’s guided checkpoint is complete; the user authorized its feature-branch publication before L10. [L10 now executes that admitted coordinate through a SITL-only native mode adapter](docs/evidence/l10-native-known-goal/README.md), reusing upstream Guided/controllers. The final flight reached the goal at a 0.99 m/s peak and held, then operator LAND/disarm completed. Exact-stock rollback and cleanup were observed. **L10 and its guided checkpoint are complete and published. [L11 now locally observes native arrival/dwell completion and operator abort to stock BRAKE](docs/evidence/l11-native-arrival-abort/README.md), with LAND/disarm, exact-L10 rollback and cleanup. L11 is published with its guided checkpoint complete. [L12 now locally qualifies a headless Gazebo scene with one stock flight, fresh disarmed connection and basic-SITL rollback](docs/evidence/l12-instrumented-scene/README.md). Its mesh-collision limit is retained; L12 is published with guided checkpoint complete. [L13 observes one front lidar and stock rangefinder validity](docs/evidence/l13-obstacle-observation/README.md), with sensor-disabled rollback, no flight/avoidance and guided checkpoint complete after clarification. L13 is published. [L14 qualifies one stock LOITER/Stop comparison](docs/evidence/l14-stock-obstacle-stop/README.md), with speed/timing corrections retained and the guided checkpoint complete after the3D walkthrough. L14 is published. [L15 now locally integrates native stopping](docs/evidence/l15-native-obstacle-stop/README.md), with clear arrival, obstacle and observation-loss BRAKE handoffs and stock rollback observed; its guided checkpoint is pending. P01 and P03 are not complete.**

## Working rules

Keep flight feedback and control independent of slow model calls and browser rendering. Start with conventional ArduPilot control and add perception/planning where needed. Record observed results separately from proposed behavior. New automated tests belong to the user unless explicitly requested; existing checks and proportionate manual verification are allowed.

The control UI is specified, not implemented or visually approved. Its implementation requires a real interactive preview and explicit approval of the shown scope.
