# FeatherLane AI Auto Drone

An incremental autonomous-drone project: select a destination, start a mission from a local control UI, and have the drone approach it using feedback. Later milestones add obstacle avoidance, GPS-denied navigation and operation after losing the ground connection.

**Direction recorded: 2026-10-31. Autopilot: ArduPilot. Development computer: macOS. Status: L01/L02 complete; L03 stock simulated flight and guided learner checkpoint complete; P01 remains in progress.**

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

This folder contains the project plan and the visible ArduPilot development checkout at [`ardupilot/`](ardupilot/) on local branch `featherlane/dev`. [L01 acquired and recorded](docs/evidence/l01-source-and-orientation/README.md) the unchanged `Copter-4.7.2` source at `fb773567896014da007bca58358704d4a0d8516f`, including all 21 recursive submodule pins. [L02 built that unchanged source and qualified two fresh disarmed native SITL launches](docs/evidence/l02-basic-sitl-setup/README.md) on macOS 15.7.7 arm64. Both reported simulated GPS/EKF3 state and stopped with no owned processes or sockets remaining. The SkyDive prototype and `FeatherLaneFlight` remain separate and untouched. [L03 observed one stock simulated takeoff to 3 m, a five-second hold, landing and automatic disarm](docs/evidence/l03-first-stock-flight/README.md), then cleanly stopped the session. Its guided learner checkpoint is complete. **L04 is next but has not started. P01 is not complete.**

## Working rules

Keep flight feedback and control independent of slow model calls and browser rendering. Start with conventional ArduPilot control and add perception/planning where needed. Record observed results separately from proposed behavior. New automated tests belong to the user unless explicitly requested; existing checks and proportionate manual verification are allowed.

The control UI is specified, not implemented or visually approved. Its implementation requires a real interactive preview and explicit approval of the shown scope.
