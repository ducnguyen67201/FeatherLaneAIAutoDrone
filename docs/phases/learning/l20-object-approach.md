# L20 Approach one confirmed static object

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M06 Add optional object-based goals · Track: object_capability · Dependencies: [L19](l19-target-spatial-goal.md), [L15](l15-native-avoidance-integration.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Use the accepted object stopping goal with the existing native approach/arrival machinery.

## The concept to learn

Perception changes the goal source while qualified flight execution remains reusable.

## Read only what this phase needs

- Goal-admission hysteresis/age policy and native active-step capability requirements.
- The previously qualified route, clearance, stop and abort behavior.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One object-dependent task step; no unbounded search or arbitrary landing.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Enable the required target/geometry capability only for this task.
2. Approach a confirmed static target using the accepted stable goal.
3. Manually exercise absence/stale identity/large goal correction and retain the bounded outcome.

## Completion evidence

- Measured arrival and clearance meet the fixed scenario contract, or the failure reason is retained.
- Coordinate missions still run without an unused detector.

Retain:

- Native/perception timelines, arrival/clearance measurements and failed cases.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Select the retained coordinate mission and disable the optional perception path.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which part changed compared with the known-coordinate mission?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
