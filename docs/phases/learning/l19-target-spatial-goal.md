# L19 Estimate one object stopping goal without moving

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M06 Add optional object-based goals · Track: object_capability · Dependencies: [L18](l18-optional-target-acquisition.md), [L13](l13-observe-one-obstacle.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Produce a bounded metric stopping goal from target observations and a qualified range/pose source.

## The concept to learn

Pixels, relative direction and a metric navigation destination are different representations.

## Read only what this phase needs

- Camera/range calibration, capture-time pose, transforms, frames and uncertainty.
- Object extent, vehicle extent and stopping-region construction.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One geometry/goal producer and native input validation; no autonomous object approach yet.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Verify range conventions and camera-to-body/navigation transforms.
2. Build a stopping region outside the target's occupied space and attach quality/time/uncertainty.
3. Compare goal error with evaluation truth across the bounded scenario.

## Completion evidence

- Goal geometry and validity limits are measured and the native receiver rejects stale/invalid goals.
- Hidden simulator object coordinates do not drive claimed sensor-based goals.

Retain:

- Calibration/profile, frame contract, goal observations and error results.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable the object-goal producer and retain the qualified coordinate task.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Why is the center of a detection box not a safe destination in meters?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L20](l20-object-approach.md) Approach one confirmed static object.
