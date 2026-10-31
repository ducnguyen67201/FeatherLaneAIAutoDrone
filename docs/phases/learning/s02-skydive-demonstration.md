# S02 Integrate the separate approved SkyDive demonstration

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** S Retained separate SkyDive demonstration · Track: deferred_skydive · Dependencies: [S01](s01-skydive-prototype-review.md), [L17](l17-approved-console-integration.md)

**Additional prerequisite:** Any added SkyDive UI scope requires its own working preview approval.

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Qualify one selected-region visual approach through the separate game adapter.

## The concept to learn

Screen/input control has different Stop and arrival semantics from ArduPilot.

## Read only what this phase needs

- Approved backend/target-selection UI scope and prototype reuse note.
- Focus/permissions/input handling and visual review criteria.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One separate backend/scene/command profile; split UI additions behind the existing preview gate.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Show/approve any added interactive UI scope before integration.
2. Integrate only scoped reusable adapter pieces and one scene/profile.
3. Perform the fixed continuous-approach review and retain all outcomes and cleanup.

## Completion evidence

- The proposed repeatability gate is actually observed or its limitation/failure retained.
- No metric arrival or ArduPilot bridge is inferred from visual closeness.

Retain:

- Shown-scope approval, recordings, configuration and actual visual review.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Stop owned tooling, release inputs and preserve the original prototype/configuration.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Why is a paused game not the same as a landed or hovering aircraft?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
