# L24 Handle one link failure at a time

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M08 Handle individual failures before combining them · Track: qualification · Dependencies: [L17](l17-approved-console-integration.md), [L11](l11-native-arrival-abort.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Demonstrate distinct native outcomes for UI, ground and observation-producer link loss in separate runs.

## The concept to learn

Different links have different owners and failure consequences.

## Read only what this phase needs

- Native cached task policy, heartbeat ownership and selected failsafe configuration.
- Required versus unused observation producers.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One failure type per run and a narrowly scoped response/status change if required.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Fix the expected policy for one link and retain a nominal baseline.
2. Disconnect that link in a bounded simulation and observe the actual response/reconnect behavior.
3. Repeat separately for the next relevant link; split code work if the response requires another independent behavior.

## Completion evidence

- Each link failure is labeled correctly and no reconnect silently re-arms/restarts.
- Observation-producer loss is not reported as merely a lost browser view.

Retain:

- Per-link configuration, event timelines and observed native/vehicle response.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore the connection/configuration and return to the retained nominal baseline.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Why may losing the browser be different from losing the navigation/perception producer?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L25](l25-external-pose-baseline.md) Qualify one alternative pose source with GPS available.
