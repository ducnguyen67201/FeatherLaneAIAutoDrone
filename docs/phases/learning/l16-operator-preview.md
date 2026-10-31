# L16 Show a minimal working operator preview

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M05 Add a small operator interface · Track: core · Dependencies: [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Present a focused interactive React/MUI preview for one mission before application UI integration.

## The concept to learn

A preview demonstrates controls and states; it does not prove vehicle execution.

## Read only what this phase needs

- Control-console requirements and current native state/request contract.
- The intended real React/MUI components and shared theme.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One isolated working preview with labeled fixtures and disconnected callbacks; no live vehicle control.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Build only connection/state, one coordinate mission, Start/Stop and event/result display.
2. Demonstrate pending, rejection, active, complete, stale and aborted states.
3. Show the working preview and record explicit approval of the shown scope before L17 integration.

## Completion evidence

- The interactive preview is usable and its actual approval source/date/scope is recorded.
- Static architecture images are not counted as UI approval.

Retain:

- Preview artifact/source and the actual shown-scope approval record when obtained.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Remove only task-owned preview processes/assets; retain needed component code and recorded review context.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which displayed states came from fixtures, and which would need firmware telemetry?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L17](l17-approved-console-integration.md) Connect the approved minimal console.
