# L21 Search one bounded area

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M07 Explore bounded search and landing as separate extensions · Track: optional_extension · Dependencies: [L20](l20-object-approach.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Visit a small declared set of observation viewpoints and terminate with found/not-found.

## The concept to learn

A target description supplies what to seek; a search region and policy supply where to look.

## Read only what this phase needs

- Request-to-action notes, camera visibility and permitted route/viewpoint geometry.
- Time/energy/geographic limits and preauthorized no-target policy.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One bounded search policy using existing motion/perception; no language-driven exploration outside its limits.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Fix a small search region/viewpoint set, visibility assumptions and termination rules.
2. Visit permitted viewpoints while recording actual coverage and confirmed candidates.
3. Demonstrate target absence and budget exhaustion without expanding the search silently.

## Completion evidence

- The search ends within its declared bounds with explicit evidence/reason.
- Occluded or unobserved space is not claimed searched.

Retain:

- Viewpoint/coverage record, budgets and found/not-found outcomes.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable the search step and return to one confirmed-target approach.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

How does the system choose where to go before it sees the target?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L22](l22-landing-site-observation.md) Assess one candidate landing patch.
