# L01 Get the source and identify the main folders

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M01 Get a working baseline and understand it · Track: core · Dependencies: none

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Create a dedicated upstream-derived checkout and record its source revision without changing flight behavior.

## The concept to learn

Source code, a checkout, a commit and a built executable are different things.

## Read only what this phase needs

- Project README and direction; upstream source-download guide.
- Selected checkout: ardupilot — ArduCopter/, libraries/, Tools/, waf and pinned submodules.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Source acquisition and local version/origin notes only; no firmware edits or simulator installation.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Choose a dedicated checkout location and inspect existing paths before creating it.
2. Clone the official source, select and record a base revision and matching submodules.
3. Walk through the three main folders and explain where vehicle logic, reusable libraries and developer tools live.

## Completion evidence

- Origin, exact commit and submodule revisions are recorded.
- The user can point to vehicle code versus shared libraries; no build/flight success is inferred.

Retain:

- Checkout path, credential-free origin, commit and submodule listing.
- A short folder map and untouched-baseline status.

**Actual execution record:** 2026-10-31: source acquisition and guided orientation complete. Copter-4.7.2 at fb773567896014da007bca58358704d4a0d8516f; main worktree and all 21 recursive submodules clean and matching parent pins. Source only, not build/flight qualified. Learner identified ArduCopter/; shared-controller location clarified. [Execution record](../../evidence/l01-source-and-orientation/README.md), [revision manifest](../../evidence/l01-source-and-orientation/source-baseline.json) and [Git output](../../evidence/l01-source-and-orientation/git-evidence.txt). L02 remains planned; P01 remains in_progress. Follow-up location correction: visible `ardupilot/` development checkout on local branch `featherlane/dev`, with the source pin and all submodules unchanged.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Keep the acquired source separate; revert only task-owned notes/checkout changes if needed and preserve unrelated paths.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Which folder contains Copter-specific behavior, and which contains reused controllers?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L02](l02-basic-sitl-setup.md) Build and launch basic SITL.
