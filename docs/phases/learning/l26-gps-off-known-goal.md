# L26 Fly one known goal with GPS unavailable

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M08 Handle individual failures before combining them · Track: qualification · Dependencies: [L25](l25-external-pose-baseline.md), [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Run the bounded known-goal mission using the qualified alternative navigation source.

## The concept to learn

Losing GPS differs from losing all usable localization.

## Read only what this phase needs

- Qualified source selection/transition and navigation-health policy.
- Known-goal behavior and actual feasible fallback when position validity is lost.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One GPS-unavailable-from-start scenario; GPS loss during flight follows as a separate run/change.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Fix the navigation inputs and verify there is no hidden ground-truth control path.
2. Repeat the known-goal mission with GPS unavailable from the start.
3. Separately examine in-flight GPS loss only after the baseline works.

## Completion evidence

- Actual trajectory error and terminal behavior are retained with explicit sensing provenance.
- Invalid localization produces the qualified feasible response rather than assumed Hold/RTL.

Retain:

- Input provenance, source configuration, trajectory error and failure outcomes.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore the qualified GPS profile and nominal scenario.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Why does turning off GPS not automatically mean the vehicle can still hold position?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L27](l27-repeatability-and-combinations.md) Repeat the qualified scenarios then combine failures.
