# L27 Repeat the qualified scenarios then combine failures

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M08 Handle individual failures before combining them · Track: qualification · Dependencies: [L15](l15-native-avoidance-integration.md), [L24](l24-one-link-failure.md), [L26](l26-gps-off-known-goal.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Run a fixed evidence campaign for only the capabilities actually qualified.

## The concept to learn

One successful run is not repeatability or a general reliability claim.

## Read only what this phase needs

- Actual accepted scenario/phase evidence, fixed thresholds and version/configuration pins.
- Capability-specific P08 campaign and failure metrics.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Manual/existing-check campaign; no new automated tests, snapshots or test scaffolding.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Predeclare nominal and individual-fault scenarios and their counts before tuning.
2. Retain all outcomes and compare against fixed criteria.
3. Combine faults only after each relevant capability passes; include object/search/landing cases only when their own prerequisites passed.

## Completion evidence

- Reported counts include failures, exclusions and unsupported cases.
- Phase/milestone completion reflects actual evidence rather than an optimistic aggregate.

Retain:

- Scenario manifest, all run outcomes, versions and accepted limits.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Retain the last qualified version/configuration and fix one failed capability at a time.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What claim does this campaign support, and what remains unproven?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
