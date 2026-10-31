# FeatherLane master learning and implementation plan

[Project home](../README.md) · [Capability roadmap](ROADMAP.md) · [Phase registry](phases/registry.json) · [First-seven-phase diagram](assets/learning/learning-workflow.svg)

**DRAFT detailed plan, recorded {{DATE}}.** The user confirmed learning through small, focused phases. Detailed cards, future extensions and diagram layout remain proposed. {{IMPLEMENTATION_STATUS}}

**Next small phase: {{NEXT_PHASE}}.** {{ACTIVE_STATUS}}

This is the execution entry point. `L01`, `L02`, and so on are small learning phases. Existing `P01`–`P09` references remain capability milestones in the roadmap and architecture; their numbers do not dictate the learning order. Master groups organize related results without turning a group into one large implementation task. A phase passing does not automatically complete its parent capability milestone.

## Begin with these seven small phases

{{FIRST_PHASES}}

The first stock simulation uses the minimum qualified SITL setup. Gazebo and instrumented sensors are introduced later, after movement makes sense. Use the existing console before building the application UI. Exact commands and versions are selected against the actual Mac and pinned source during the appropriate phase; current documentation does not certify a version tuple.

L01–L04 introduce no custom flight behavior. L05–L07 reuse stock flight behavior while changing or observing one thing at a time. An unfamiliar term should be explained through the visible experiment before its code is expanded.

## The shared phase interface

Every [phase card](phases/README.md) follows the same template:

1. One observable result and one concept to learn.
2. The minimum inputs, prerequisite evidence and source files to read.
3. A narrow change scope and a prediction of what should happen.
4. A short manual experiment using the selected qualified scenario.
5. Actual output/evidence, limitations and a route back to the known baseline.
6. A brief explanation of the result and the next small step.

Keep code focused on that result. Prefer one behavior, one selected mode/path and one scenario. Read upstream code selectively rather than rewrite control, estimation or motor mixing. There is no arbitrary line-count target: necessary integration plumbing is explained, while independent behavior is split into another phase. Future cards are bounded objectives; split them further if source/sensor/tool qualification reveals a second unfamiliar change.

Completion means the stated evidence exists. A later session can set `in_progress`, `ready_for_review`, `complete` or `blocked` with the actual reason/record. Understanding questions guide the explanation. Scope already authorized by the user can proceed, while existing explicit approval boundaries remain intact.

## Master groups and later small phases

{{GROUP_PHASES}}

The default next step is always the earliest unmet prerequisite in the selected track. After the baseline, branches can advance independently when their own prerequisites are met. Object acquisition is optional per mission; a valid coordinate-only mission does not need a detector. Search and landing are additional proposed capabilities and are not prerequisites for coordinate-and-hold learning. The SkyDive branch remains a separate, deferred demonstration, not a dependency of ArduPilot SITL. Hardware remains separately scoped optional work.

## Boundaries that carry into every phase

- Keep bounded in-flight mission execution/supervision native in our maintained ArduPilot-derived C++ runtime. External tooling supplies requests/observations and displays actual state.
- Keep browser rendering, heavy perception and slow model calls outside critical flight callbacks.
- Built-in avoidance requires qualified sensing, configuration and a supported/integrated mode. It is not enabled just because an obstacle is drawn in a world.
- Retain ground truth for scoring or a clearly labeled privileged baseline; do not pass it off as sensor-only autonomy.
- Before UI integration, show a working preview using the intended React/MUI components/theme and record explicit approval of that shown scope. Only L17 depends on L16 UI approval; early SITL learning does not.
- Use existing checks and manual observations. No new automated tests, snapshots or test scaffolding are authorized by this plan.
- Remote publication/pushes, purchases, remote resource changes and physical operations retain their separate authorization requirements. A phase plan is not execution evidence.

## Sources and reproducible documents

The canonical state/specification is [registry.json](phases/registry.json). This master page and the phase cards are generated from it and the two templates by [render-learning-plan.py](../scripts/render-learning-plan.py). The script only renders local documentation and the editable first-seven-phase diagram specification; it does not install tools, clone source, run a simulator, start agents or operate a vehicle. The generated pages stay linked from the maintained project documentation.

The user suggested `master-agreement-generator`. Its useful pattern here is one reusable template plus structured specifications and reproducible draft output. Its legal clauses, party roles and signature workflows are unrelated to this engineering plan. The shared phase-card template and JSON registry apply that pattern to learning tasks.

Official setup references were checked on {{DATE}}. Use the actual selected revision/platform instructions during execution, because some tutorial pages contain older commands:

- [ArduPilot source and Git](https://ardupilot.org/dev/docs/where-to-get-the-code.html).
- [macOS build-environment guidance](https://ardupilot.org/dev/docs/building-setup-mac.html).
- [Using SITL](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html).
- [Gazebo integration for the later scene phase](https://ardupilot.org/dev/docs/sitl-with-gazebo.html).
