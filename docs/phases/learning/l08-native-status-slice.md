# L08 Add a small native status slice

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: planned.** M03 Add our native mission behavior in small slices · Track: core · Dependencies: [L07](l07-measure-arrival.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Prove one bounded custom native component can build and report status while the stock flight mode remains active.

## The concept to learn

Our native task logic belongs inside the maintained autopilot while reusing upstream flight facilities.

## Read only what this phase needs

- Chosen revision's mode/module registration, build and scheduling conventions.
- Native mission architecture and update-maintenance policy.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One minimal native component/build/scheduling slice and bounded status output. Stock mode retains flight execution; custom mode activation/movement follows in L10.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Select the smallest native component/status slice and list its necessary build/scheduling plumbing.
2. Add bounded status output while the qualified stock mode continues to own movement.
3. Build and manually verify the reported state and return to the untouched stock build.

## Completion evidence

- The native status slice builds and reports actual status while stock mode retains flight execution.
- Custom commits/diffs remain identifiable against the untouched baseline.

Retain:

- Scoped diff, build result, status output and scheduling/resource notes.

**Actual execution record:** none; this phase has not been executed.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Revert the isolated custom slice or select the retained upstream build.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which part is our addition, and which stock behavior still owns movement?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L09](l09-native-task-contract.md) Admit one typed coordinate task.
