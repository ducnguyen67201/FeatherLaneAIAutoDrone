# L25 Qualify one alternative pose source with GPS available

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M08 Handle individual failures before combining them · Track: qualification · Dependencies: [L12](l12-instrumented-scene.md), [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Observe and integrate one selected alternative pose source before relying on it for GPS-denied movement.

## The concept to learn

A map or an IMU alone is not a qualified position estimate.

## Read only what this phase needs

- Selected sensor/estimator assumptions, origin/frame/time alignment and quality/reset semantics.
- ArduPilot external-navigation integration for the pinned build.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One source/profile and observation/integration qualification; split sensor setup, alignment and fusion into additional cards if any becomes a separate unfamiliar change.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Select one appropriate estimator/sensor source and define the alignment contract.
2. Observe its drift/quality while GPS remains available for baseline comparison.
3. Qualify its intended ArduPilot integration without claiming GPS-denied flight.

## Completion evidence

- Alternative pose validity, frame alignment and limitations are measured.
- Evaluation truth is not secretly used as the alternative sensor-only estimate.

Retain:

- Sensor/estimator/profile pin, alignment/quality results and observed reset/loss behavior.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable the alternative source configuration and retain the GPS baseline.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What produces the alternative position estimate before ArduPilot can use it?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L26](l26-gps-off-known-goal.md) Fly one known goal with GPS unavailable.
