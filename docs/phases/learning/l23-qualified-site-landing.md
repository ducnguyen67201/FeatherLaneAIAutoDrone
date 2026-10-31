# L23 Land at one qualified simulated site

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M07 Explore bounded search and landing as separate extensions · Track: optional_extension · Dependencies: [L22](l22-landing-site-observation.md), [L15](l15-native-avoidance-integration.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Execute and verify landing at one admitted static simulated site using qualified ArduPilot behavior.

## The concept to learn

A landing command, descent guidance and confirmed touchdown are separate conditions.

## Read only what this phase needs

- Selected LAND/precision-landing path, mode handoff and required estimator/target inputs.
- Site validity during descent and feasible interruption/terminal policy.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One native landing handoff and touchdown verification for the admitted scenario.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Qualify the selected landing path and native handoff in the simple site scenario.
2. Execute descent while checking required state/site observations.
3. Verify touchdown and terminal state; record the feasible outcome when the site/input becomes invalid.

## Completion evidence

- Actual touchdown/terminal evidence is retained, with no arbitrary-site capability inferred.
- Landing failure/interruption is distinguished from arrival or a paused simulator.

Retain:

- Site admission, mode/flight timeline and actual landing/failure outcomes.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Return to the qualified approach-and-hold scenario and previous mode/build.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What measurement proves that landing completed?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
