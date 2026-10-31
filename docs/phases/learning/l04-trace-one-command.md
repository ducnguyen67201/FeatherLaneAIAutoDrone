# L04 Trace one flight command through the code

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M01 Get a working baseline and understand it · Track: core · Dependencies: [L03](l03-first-stock-flight.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Follow one observed command from its receiver or active mode to navigation, control and motor output.

## The concept to learn

Mission, mode, navigation, feedback control and estimation have distinct jobs.

## Read only what this phase needs

- Selected checkout: relevant GCS_MAVLink handler and active mode file.
- The calls actually used by that mode into AC_WPNav, AC_PosControl, AC_AttitudeControl, AP_Motors and estimator state.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Read-only walkthrough and annotations; optional existing debugger/log tools only after checking their effect on timing.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Choose one action from the previous flight and locate its actual receiver/mode path.
2. Read only the functions needed to connect the action to reference generation and control.
3. Draw the observed chain in plain language and connect each stage to the saved flight timeline.

## Completion evidence

- The user can explain the selected path and identify which part estimates state versus produces motor demand.
- Source links/line references match the pinned checkout, rather than older tutorial APIs.

Retain:

- A short source-linked walkthrough for one command.
- A note about any gaps or timing effect of observation tools.

**Actual execution record:** [Pinned-source GUIDED takeoff walkthrough](../../evidence/l04-trace-one-command/README.md): request admission, target, estimator feedback, position/attitude control, motor mixer and simulated outputs traced against the L03 evidence. Guided learner checkpoint completed in this chat on 2026-10-31: learner located read_inertia/AHRS state reads and AP_MotorsMatrix mixing. Follow-up clarified that the estimator supplies current state, controllers consume it, and both estimation and control run inside ArduPilot rather than MAVProxy. This is guided understanding, not an independent examination. No new flight, firmware changes or runtime instrumentation.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Remove only optional task-owned debug instrumentation; keep the unchanged baseline available.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Where is the destination selected, and where are individual motor outputs calculated?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
