# L03 Watch one takeoff hold and landing

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M01 Get a working baseline and understand it · Track: core · Dependencies: [L02](l02-basic-sitl-setup.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Perform one simple stock simulated flight through the existing console.

## The concept to learn

A requested command, an acknowledgment and achieved movement are separate events.

## Read only what this phase needs

- Selected stock mode and console commands qualified for this build.
- Telemetry/log fields for mode, altitude, vertical speed, landed state and arming.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

No custom flight code. Use the unchanged vehicle and a clear basic scene.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Explain the expected takeoff, hold, land and disarm sequence before running it.
2. Issue each supported action and observe its resulting state.
3. Save a short command/state timeline and cleanly end the session.

## Completion evidence

- Takeoff, a controlled hold, landing and disarm are observed and recorded.
- Rejected/unready states are explained rather than hidden by a success label.

Retain:

- Command/state timeline and the retained simulator/flight log.
- Observed limitations and one sentence explaining the result.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Use the qualified simulator stop/terminal procedure and restore its baseline configuration.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What evidence tells us that takeoff actually happened rather than merely being accepted?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L04](l04-trace-one-command.md) Trace one flight command through the code.
