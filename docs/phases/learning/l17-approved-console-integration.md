# L17 Connect the approved minimal console

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M05 Add a small operator interface · Track: core · Dependencies: [L16](l16-operator-preview.md)

**Additional prerequisite:** Explicit approval of the working L16 preview scope; new scope needs its own preview.

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Connect the approved controls to operator requests and firmware-reported state for one mission.

## The concept to learn

The browser observes and requests; native code owns in-flight progression.

## Read only what this phase needs

- Approved preview scope and the qualified native ingress/status contract.
- External session/process ownership and stale/reconnect behavior.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Only the approved console scope and smallest necessary external session adapter.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Integrate the approved controls and bounded event/status display.
2. Exercise start/rejection/stop and reconnect against the qualified native mission.
3. Remove obsolete preview scaffolding and leave a clear start/stop entry point.

## Completion evidence

- The UI reports actual native state and a reconnect cannot silently restart a mission.
- Only owned processes are launched/cleaned and obsolete preview material is removed.

Retain:

- Approval reference, source diff, manual UI/mission observations and cleanup record.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Stop owned tooling and return to the existing console/qualified native baseline.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What happens to an already accepted native mission when the browser closes?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
