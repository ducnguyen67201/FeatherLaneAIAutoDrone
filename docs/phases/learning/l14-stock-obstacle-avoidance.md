# L14 Qualify one stock avoidance scenario

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M04 Observe one obstacle then avoid it · Track: core · Dependencies: [L13](l13-observe-one-obstacle.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Demonstrate one clear/blocked obstacle scenario using a documented supported stock mode and existing avoidance.

## The concept to learn

Avoidance needs a destination, usable observations and a qualified mode/configuration.

## Read only what this phase needs

- Selected stock avoidance behavior and its mode/input constraints.
- AC_WPNav_OA/AP_OAPathPlanner or the actual chosen code path in the pinned source.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One stock avoidance configuration and static scene; no custom planner or native-mode avoidance yet.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Fix conservative motion/clearance criteria and the intended supported stock mode.
2. Run a clear route and a route with the single obstacle.
3. Observe the detour or bounded failure and inspect actual clearance/stop behavior.

## Completion evidence

- The recorded stock path behaves as configured, with limitations retained.
- A detected obstacle is not assumed to guarantee a globally feasible route.

Retain:

- Exact parameters, sensor profile, route/clearance observations and failures.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore baseline parameters and the clear scene.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What additional inputs made avoidance work compared with a plain waypoint command?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L15](l15-native-avoidance-integration.md) Reuse avoidance in our native path.
