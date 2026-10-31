# L15 Reuse avoidance in our native path

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M04 Observe one obstacle then avoid it · Track: core · Dependencies: [L14](l14-stock-obstacle-avoidance.md), [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Connect the qualified avoidance path to our native task and repeat the same scene.

## The concept to learn

Custom modes do not automatically inherit stock AUTO/GUIDED behavior.

## Read only what this phase needs

- Native adapter type/initialization and the selected avoidance handoff.
- Planner processing/error/success and upstream mode/failsafe interaction.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One explicit native avoidance integration and blocked-route policy; no general urban planner.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Identify the exact shared navigation/avoidance objects and failure semantics.
2. Integrate the qualified path while preserving native task ownership and input validity.
3. Compare clear, single-obstacle and blocked behavior with L14.

## Completion evidence

- Our mode uses the intended avoidance path and reports blocked/invalid outcomes honestly.
- No infinite continuation on missing observations or unknown route viability is claimed.

Retain:

- Integration diff, scenario comparison, native reasons and actual trajectory.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Return to the last qualified native clear-scene build or the stock avoidance baseline.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which stock feature was reused, and which integration did we still need to write?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
