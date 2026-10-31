# L09 Admit one typed coordinate task

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M03 Add our native mission behavior in small slices · Track: core · Dependencies: [L08](l08-native-status-slice.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Accept or reject a bounded coordinate-task definition in the native component without initiating movement.

## The concept to learn

Data validation and authorization precede navigation.

## Read only what this phase needs

- Proposed mission contract, actual ingress/receiver and native state model.
- Frame/origin/reset, units, limits and required-input rules.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One small typed task and its actual scoped ingress/status contract; no general language interpreter or movement.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Choose/version the minimal coordinate task and identify its producer/receiver.
2. Implement bounded acceptance/rejection and explicit reasons for invalid frame, limits or prerequisites.
3. Manually submit a valid example and relevant invalid cases without starting flight execution.

## Completion evidence

- Valid data is accepted and invalid/unsupported data is rejected with reasons.
- Task admission cannot silently arm or start motion.

Retain:

- Exact schema/message mapping, submitted examples and native responses.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable/remove the scoped ingress change and retain the L08 status baseline.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Why can a syntactically valid coordinate still be an invalid mission?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L10](l10-native-known-goal.md) Execute one accepted native goal.
