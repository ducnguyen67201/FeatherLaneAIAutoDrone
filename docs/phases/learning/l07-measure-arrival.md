# L07 Measure stopping and arrival

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M02 Learn movement with one change at a time · Track: core · Dependencies: [L06](l06-one-speed-change.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

Distinguish passing a waypoint from reaching a low-speed held destination.

## The concept to learn

Completion is a measured position, speed and dwell condition.

## Read only what this phase needs

- Selected waypoint/hold behavior and relevant recorded telemetry.
- Current proposed arrival thresholds, to be fixed for the scenario before qualification.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

Manual/log-based observation of stopping; no new controller or automatic test suite.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Define the scenario's position, speed and dwell conditions before the run.
2. Observe deceleration, first entry into the region and continued hold.
3. Compare the waypoint-reached indicator with the full arrival contract.

## Completion evidence

- Arrival/stop behavior is measured honestly, including drift, overshoot or failure.
- The user can explain why a waypoint flag alone may be insufficient.

Retain:

- Position/speed/dwell timeline and the chosen scenario thresholds.

**Actual execution record:** [Measured entry, stopping and arrival](../../evidence/l07-measure-arrival/README.md): fixed1m/.3m/s/2s dwell plus height/state/freshness/gap conditions before stock L05-config run. First region entry2.418s at2.190m/s; first all-bounds sample3.164s; nine samples completed dwell at5.165s; further17.254s of qualifying sampled hold before LAND. About0.100m overshoot; no waypoint-reached message observed in selected GUIDED position path. Flight, landing/disarm, cleanup and guided checkpoint complete on 2026-10-31. Learner identified that first entry was too fast and one later low-speed sample was insufficient; continued held conditions were needed. Guided clarification fixed the timing, speed<=0.3m/s rather than exact zero, and two-second dwell terminology. Guided understanding, not independent examination. No parameter/controller changes or new tests.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Return to the L05 configuration; retain the failed run and reason if arrival is not achieved.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

What evidence distinguishes a pass-through from a controlled stop?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Return to the master plan to select the next unmet prerequisite in this track.
