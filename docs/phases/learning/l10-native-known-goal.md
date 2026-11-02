# L10 Execute one accepted native goal

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M03 Add our native mission behavior in small slices · Track: core · Dependencies: [L09](l09-native-task-contract.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Use the native mode adapter to execute one already accepted coordinate task in a clear scene.

## The concept to learn

Our coordinator selects the goal; reused navigation and controllers calculate movement.

## Read only what this phase needs

- Qualified mode entry/exit and initialization from the selected revision.
- Actual native call path into navigation/control; stock GUIDED messages are not assumed to feed this mode.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One native known-goal execution path with vehicle/authority/navigation checks; reuse the L05 goal.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Specify qualified entry/exit and the currently valid inputs before enabling movement.
2. Connect the accepted task to the selected existing navigation/control path.
3. Run the same known-goal scenario and compare its movement with the stock baseline.

## Completion evidence

- The native owner executes the accepted goal and retains upstream authority/failsafe behavior.
- Any difference from the stock baseline is explained and recorded.

Retain:

- Scoped integration diff, build pin, native state events and comparative trajectory.

**Actual execution record:** [L10 evidence](../../evidence/l10-native-known-goal/README.md): final mode31 native goal executed at 0.99 m/s peak; two-second sampled dwell completed at 7.93 s, followed by 50.27 s qualifying hold and operator LAND/disarm. Duplicate/rejected command behavior, exact-stock rollback and cleanup observed. Guided learner checkpoint complete after the 2026-11-02 clarification; L10 feature publication authorized; L11 not started.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Return to the retained stock build/mode and baseline scenario.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which part of the code changed the destination, and which generated motor demand?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L11](l11-native-arrival-abort.md) Add native arrival and operator abort.
