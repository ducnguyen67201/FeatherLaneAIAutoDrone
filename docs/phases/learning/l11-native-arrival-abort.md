# L11 Add native arrival and operator abort

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M03 Add our native mission behavior in small slices · Track: core · Dependencies: [L10](l10-native-known-goal.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Report measured arrival and execute one qualified operator-abort path with clear native reasons.

## The concept to learn

A task lifecycle is different from the lower-level controller loop.

## Read only what this phase needs

- Native state transitions, L07 arrival observations and selected supported fallback.
- Upstream arming, override and failsafe interaction.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Small native arrival/dwell and operator-stop transitions; no arbitrary failure framework.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Bind the measured arrival contract and bounded input-validity checks to the active task.
2. Implement one qualified operator-stop/abort transition with actual response reporting.
3. Manually demonstrate nominal arrival and an interrupted run.

## Completion evidence

- Completion follows measured conditions, and abort shows actual state/reason.
- Reconnect or duplicate requests do not restart or re-arm the task.

Retain:

- State transition timeline, nominal/abort logs and measured terminal behavior.

**Actual execution record:** [L11 evidence](../../evidence/l11-native-arrival-abort/README.md): native2000ms dwell/COMPLETE at7.79s, then29.76s sampled hold. Fresh USER_3 abort selected stock BRAKE; two-second sampled stop completed4.11s after acknowledgment, at least3.08m from goal. Duplicates/consumed requests, LAND/disarm, exact-L10 rollback and cleanup observed. Guided checkpoint complete after clarification; feature publication authorized; L12 not started.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Revert the isolated lifecycle addition and use the last qualified configuration.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Can a task be complete while the aircraft remains airborne, and what policy follows?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
