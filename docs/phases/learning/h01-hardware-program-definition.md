# H01 Define a separate hardware qualification program

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** H Optional hardware planning · Track: optional_hardware · Dependencies: [L27](l27-repeatability-and-combinations.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Document a scoped hardware program before selecting any physical implementation work.

## The concept to learn

Simulation evidence does not qualify a real vehicle or authorize operation.

## Read only what this phase needs

- Qualified simulation subset and actual hardware/resource/sensor requirements.
- Separate physical-deployment and operating-context requirements.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Planning only until separately scoped authorization; no purchase, provisioning or physical operation.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Choose the relevant proven simulation subset and identify transfer gaps.
2. Draft the hardware/process deployment and qualification sequence.
3. Keep procurement/physical work subject to its separately authorized scope.

## Completion evidence

- The proposed hardware scope, limits, resources and qualification plan are concrete and reviewable.

Retain:

- Separate proposed hardware/deployment/qualification document and actual decisions.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Retain the simulation baseline; no physical state is changed by this planning card.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which simulation assumptions need new evidence on actual hardware?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
