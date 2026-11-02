# L13 Observe one obstacle sensor

[Master learning plan](../../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../../ROADMAP.md) · [Registry](../registry.json)

**DRAFT phase card. Status: complete.** M04 Observe one obstacle then avoid it · Track: core · Dependencies: [L12](l12-instrumented-scene.md)

Generated from the learning-phase record in `docs/phases/registry.json` and `docs/phases/learning-phase.template.md`. Change those sources and run `python3 scripts/render-learning-plan.py`; do not hand-edit this generated card. Planning or generating this card does not perform its work.

## One observable result

See usable distance/proximity observations for one static obstacle before using them for control.

## The concept to learn

A visible obstacle and a valid metric obstacle observation are different.

## Read only what this phase needs

- Selected sensor geometry, mounting frame, range, timestamp and validity fields.
- Actual observation transport and the downstream consumer.

Paths naming ArduPilot files refer to the future selected checkout. Resolve exact methods, units and lines against the pinned build; earlier research examples are not a qualified version.

## Allowed change scope

One simulated obstacle sensor and bounded observation path; no autonomous dodge behavior.

Default to one behavior or integration slice. Explain each changed file and its role. If another unfamiliar subsystem or independent behavior becomes necessary, split that work into another card before broadening the implementation. Keep other parameters and scenario conditions fixed where possible.

## Walk through the phase

Before changing anything, explain the expected visible result in ordinary language and write one prediction. Then:

1. Place one obstacle at known evaluation positions and configure one sensor.
2. Inspect observation direction, distance, timestamps, coverage and absence/invalid states.
3. Compare measurements with declared evaluation truth without feeding hidden truth into autonomy.

## Completion evidence

- Sensor values and invalid/out-of-view behavior are understood and recorded.
- Required clearance directions and coverage limits are explicit.

Retain:

- Sensor configuration, observation samples and comparison notes.

**Actual execution record:** [L13 evidence](../../evidence/l13-obstacle-observation/README.md): one front 21-ray planar lidar, static box, bounded Python observation adapter and existing MAVLink rangefinder. Stable3m/5m returns, off-axis/beyond/under-range/above-plane no-return, reader dropout NoData/recovery and sensor-disabled baseline observed disarmed. No-return is not clearance; no flight/avoidance or firmware changes. Local/unpublished; guided checkpoint complete after the under-range clarification. Screenshot publication pending readable attachment.

Use proportionate existing checks and manual observations. Do not create automated tests, snapshots or test scaffolding without an explicit user request. A successful install/build is evidence only for that operation.

## Return to the known baseline

Disable the new sensor/integration and retain the baseline scene.

Keep custom changes identifiable against the pinned upstream/submodule base and preserve unrelated state. Upstream updates are separate review/requalification work.

## Explain the result

Can a target bounding box establish the distance or clearance measured by this sensor?

Use a short explanation in the user's own words as the learning checkpoint. Report what happened, what remains unclear and the next small step. Continue within already authorized scope; existing UI, external-action and hardware approval boundaries still apply.

Next card in this group: [L14](l14-stock-obstacle-avoidance.md) Qualify one stock avoidance scenario.
