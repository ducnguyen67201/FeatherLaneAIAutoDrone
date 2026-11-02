# L14 Qualify one stock avoidance scenario

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M04 Observe one obstacle then avoid it · Track: core · Dependencies: [L13](l13-observe-one-obstacle.md)

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

**Actual execution record:** [L14 evidence](../../evidence/l14-stock-obstacle-stop/README.md): unchanged stock LOITER/Stop with front rangefinder/proximity. Final low-lean profile peaked0.49m/s in both cases; clear advanced about4.6m, blocked completed a2s low-speed dwell while input held at13.75s. Gazebo minimum center gap2.23m / declared0.7m-disc gap1.53m. LAND/disarm and default baseline rollback observed. Initial speed/timing failures retained. Local/unpublished; human3D-scene visibility confirmed and both logs replayed, guided checkpoint complete after the3D walkthrough; L15 not started.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore baseline parameters and the clear scene.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What additional inputs made avoidance work compared with a plain waypoint command?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L15](l15-native-avoidance-integration.md) Reuse avoidance in our native path.
