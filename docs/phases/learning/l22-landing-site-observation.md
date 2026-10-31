# L22 Assess one candidate landing patch

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M07 Explore bounded search and landing as separate extensions · Track: optional_extension · Dependencies: [L20](l20-object-approach.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Assess one bounded candidate ground patch without commanding a landing.

## The concept to learn

Recognizing the nearby object does not establish landing-surface or descent suitability.

## Read only what this phase needs

- Selected ground sensing/geometry, footprint, surface assumptions and descent corridor.
- Validity/uncertainty and no-qualified-site policy.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One observable landing-site assessment capability; no general arbitrary-terrain claim or descent control.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Choose a simple declared surface and required footprint/clearance evidence.
2. Evaluate one acceptable and one unsuitable/unknown patch.
3. Publish a bounded candidate plus validity reasons for native acceptance/rejection.

## Completion evidence

- The candidate claim matches measured surface/corridor evidence and rejected cases.
- An unknown patch is not treated as acceptable merely because it is beside the target.

Retain:

- Surface/corridor observations, assessment limits and acceptance/rejection reasons.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable site assessment and retain the approach-and-hold task.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What additional evidence is required for landing beyond locating the truck?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L23](l23-qualified-site-landing.md) Land at one qualified simulated site.
