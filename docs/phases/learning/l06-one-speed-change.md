# L06 Change one speed limit and compare

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M02 Learn movement with one change at a time · Track: core · Dependencies: [L05](l05-one-coordinate.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Repeat the same route with one changed speed setting and explain the difference.

## The concept to learn

Speed limits influence travel time; acceleration and stopping remain separate constraints.

## Read only what this phase needs

- The selected mode's actual speed parameter/API, units and persistence semantics.
- Measured position and velocity traces from L05.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One qualified speed setting; keep route, controller tuning and scene fixed.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Record the original setting and predict the visible effect of the change.
2. Repeat the identical route with the single change.
3. Compare actual speed/travel/stop behavior, then restore or explicitly retain the chosen setting.

## Completion evidence

- The changed setting and observed effect are clear, including any difference from the prediction.
- No unexplained additional parameter or controller changes were introduced.

Retain:

- Before/after values, comparable run logs and a short explanation.

**Actual execution record:** [Same-route speed comparison](../../evidence/l06-one-speed-change/README.md): only intentional setting WP_SPD10->1m/s, restored10 after landing/disarm. Peak measured speed3.120->0.990m/s and first identical low-speed near-goal sample3.258->5.782s. Same coordinate/frame/height; stock hover-learning/statistics updates retained and explained. Flight/cleanup and guided checkpoint complete on 2026-10-31. Learner identified acceleration, slowing and WP_SPD as a horizontal speed target. Follow-up clarified braking at the destination while holding height versus later landing/descent; guided understanding, not independent examination. One pair only; no controller tuning, firmware edits or new tests.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore the recorded original setting and repeat the baseline if needed.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Did the requested speed equal the observed speed throughout the route, and why?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L07](l07-measure-arrival.md) Measure stopping and arrival.
