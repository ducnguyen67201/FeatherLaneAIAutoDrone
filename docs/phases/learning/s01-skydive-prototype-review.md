# S01 Review the separate SkyDive prototype

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** S Retained separate SkyDive demonstration · Track: deferred_skydive · Dependencies: none

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Document reusable screen/input behavior and its limits without changing the prototype.

## The concept to learn

A visual game demonstration and an instrumented ArduPilot flight are different evidence paths.

## Read only what this phase needs

- Existing prototype recordings/configuration and the unresolved contact report.
- Capture, region tracking, HUD decoding and key scheduling responsibilities.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Read-only review and a scoped reuse note; no changes to the preserved prototype.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Inspect the existing source/evidence within scope.
2. Identify reusable pieces and distinguish tracking from semantic detection.
3. Record the interface limits and proposed separate integration.

## Completion evidence

- Existing evidence is labeled honestly and prototype/private files remain preserved.

Retain:

- Reuse map, actual evidence references and limitations.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

No prototype modifications to revert; preserve the reviewed originals.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which claims can this visual demonstration support, and which need instrumented SITL evidence?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [S02](s02-skydive-demonstration.md) Integrate the separate approved SkyDive demonstration.
