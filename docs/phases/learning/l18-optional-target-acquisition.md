# L18 Recognize one supported target without moving

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M06 Add optional object-based goals · Track: object_capability · Dependencies: [L12](l12-instrumented-scene.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Qualify acquisition/identity for one chosen target class or reference in simulation.

## The concept to learn

A detector finds image regions; supported targets and identity need evaluation.

## Read only what this phase needs

- Selected detector/tracker classes, license/runtime and representative imagery.
- Held-out scene/viewpoint evaluation and target-absence/identity-switch cases.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One optional perception capability and its observations; no motion triggered by detections.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Define one target/instance rule and representative labeled/negative scenes.
2. Evaluate an existing model first and adapt only if necessary.
3. Record acquisition failures, false detections, absence and identity continuity on held-out scenes.

## Completion evidence

- The supported target claim matches retained evaluation evidence and limitations.
- An unsupported class is reported explicitly rather than assumed recognized.

Retain:

- Model/profile/license references, dataset split rationale and actual outcomes.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable the optional worker; retain coordinate-only missions and preserve weights/data outside scope.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What does this detector output, and what does it still not know about the object?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L19](l19-target-spatial-goal.md) Estimate one object stopping goal without moving.
