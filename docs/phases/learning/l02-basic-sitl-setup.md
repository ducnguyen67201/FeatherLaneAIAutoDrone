# L02 Build and launch basic SITL

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M01 Get a working baseline and understand it · Track: core · Dependencies: [L01](l01-source-and-orientation.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Run one unchanged ArduCopter SITL instance on the selected environment while disarmed.

## The concept to learn

SITL is the autopilot executable plus simulated sensors/physics; a 3D world can come later.

## Read only what this phase needs

- Official macOS build setup and the selected source revision's prerequisite/build scripts.
- Tools/autotest/sim_vehicle.py and the actual build output/startup log.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Machine/toolchain qualification, scoped dependencies and a reproducible basic SITL launch; no Gazebo, ROS, AI or product UI.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Record actual Mac architecture/OS and inspect required tools and any prerequisite script before using it.
2. Qualify the unchanged build and launch one standard vehicle with the minimum useful ground-console view.
3. Read heartbeat/mode/readiness, then stop only owned processes and repeat the launch.

## Completion evidence

- One disarmed instance starts, reports usable state and shuts down cleanly.
- Actual versions, endpoint and repeatable commands are recorded. A platform blocker is recorded as blocked, not complete.

Retain:

- Mac/toolchain version tuple, source pin, start/stop commands and startup log.
- Any native-Mac limitation and a bounded fallback decision.

**Actual execution record:** 2026-10-31: unchanged Copter-4.7.2 built on macOS 15.7.7 arm64 / Apple Clang 17 / Python 3.12.12. Two sequential fresh stock quad SITL launches reported disarmed STABILIZE, simulated GPS and EKF3 GPS use; owned processes stopped and sockets cleared after each. [Execution/runbook](../../evidence/l02-basic-sitl-setup/README.md), [environment/source tuple](../../evidence/l02-basic-sitl-setup/environment.json) and [actual run results](../../evidence/l02-basic-sitl-setup/run-results.json). Startup dependency failure, four MAVProxy parsing errors per run and terrain limitations retained. Learning checkpoint completed in this chat on 2026-10-31: learner explained compilation, SITL and the ground console; follow-up clarified SITL as the simulation setup and successful launch versus successful flight. No arming/flight or custom firmware. L03 remains planned; P01 remains in_progress.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Stop owned simulator processes and return to the recorded baseline; document installed dependencies and preserve user configuration.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which process runs ArduPilot, and where do its sensor measurements come from?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L03](l03-first-stock-flight.md) Watch one takeoff hold and landing.
