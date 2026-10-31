# L05 Fly to one known coordinate

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M02 Learn movement with one change at a time · Track: core · Dependencies: [L04](l04-trace-one-command.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Reach one nearby known destination using a qualified stock AUTO or GUIDED path.

## The concept to learn

A destination needs a frame, units, origin and altitude reference.

## Read only what this phase needs

- The selected stock destination-ingress path and coordinate conversion.
- Existing mission/path illustration for frame terminology.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One destination via existing console/mission tooling; no custom mission runtime or target detector.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Write down the goal and coordinate/height conventions and predict the movement.
2. Use one qualified stock execution path in an obstacle-free scene.
3. Compare requested goal with measured vehicle position and speed.

## Completion evidence

- The intended coordinate is reached through the selected stock path.
- The origin/sign conventions and actual terminal behavior are documented.

Retain:

- Goal/frame, parameters and measured trajectory.
- Source-linked explanation of destination acceptance.

**Actual execution record:** [One stock coordinate flight](../../evidence/l05-one-coordinate/README.md): GUIDED DO_REPOSITION to latitude -35.3632172°, longitude 149.1652374°, 3 m above home; about 5 m north. Accepted request, measured movement, five-second low-speed goal hold, LAND/automatic disarm and clean shutdown observed. Guided height-reference checkpoint complete on 2026-10-31. Startup invalid positions and four parsing errors retained; no speed tuning or firmware edits. One run only; P03 broader gate and P01 failure-handling remain open.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Restore the known mission/parameters and use the qualified terminal procedure.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What would change if the same numeric coordinate used a different origin or altitude frame?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L06](l06-one-speed-change.md) Change one speed limit and compare.
