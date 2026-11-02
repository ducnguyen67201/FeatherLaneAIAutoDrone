# L12 Connect one instrumented simulator scene

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M04 Observe one obstacle then avoid it · Track: core · Dependencies: [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Run the qualified flight baseline in one simple instrumented scene, preferably Gazebo.

## The concept to learn

The scene/physics simulator and the SITL flight runtime have separate responsibilities.

## Read only what this phase needs

- Official Gazebo plugin documentation and compatibility for the actual environment.
- The selected world, vehicle plugin and sensor configuration.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One compatible simulator/plugin/world integration; no AI, ROS by default or obstacle-avoidance changes.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Select and record a compatible version tuple and native-Mac versus explicitly scoped fallback.
2. Launch one simple scene and verify the physics/sensor connection.
3. Repeat the existing baseline movement and document simulator differences.

## Completion evidence

- The chosen scene and SITL exchange the intended outputs/measurements reproducibly.
- No compatibility or collision evidence is claimed from a successful install alone.

Retain:

- Pinned simulator/plugin versions, launch files/commands and one baseline log.

**Actual execution record:** [L12 evidence](../../evidence/l12-instrumented-scene/README.md): native Mac headless Gazebo8.10.0/official plugin with unchanged stock JSON/X-frame flight, fresh disarmed connection and basic-SITL rollback. Arrival dwell completed7.80s, then31.83s sampled hold; peak speed1.05m/s against1m/s target. Mesh-body collision limit retained. Guided checkpoint complete; published at project7b1dc4a07bb335c960c2e72f855b0e3bf07d6885; L13 observed locally.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Stop owned scene processes and return to basic SITL with the previous profile.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which program calculates flight control, and which simulates the world?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L13](l13-observe-one-obstacle.md) Observe one obstacle sensor.
