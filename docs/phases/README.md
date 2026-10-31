# Learning phases and capability milestones

[Master learning plan](../MASTER-LEARNING-PLAN.md) · [Capability roadmap](../ROADMAP.md) · [Registry](registry.json)

Use the master plan for the execution order and open one small phase card at a time. Begin with [L01 source acquisition and orientation](learning/l01-source-and-orientation.md), then [L02 basic SITL setup](learning/l02-basic-sitl-setup.md) and [L03 first stock flight](learning/l03-first-stock-flight.md). L01 is complete with a [source/orientation execution record](../evidence/l01-source-and-orientation/README.md). [L02 build/disarmed SITL qualification](../evidence/l02-basic-sitl-setup/README.md) is also complete. L03 is next and remains planned; no arming or flight has been qualified.

`registry.json` is the canonical state/specification. Existing `phases` entries retain the P00–P09 capability milestones and evidence boundaries. `learning_groups` and `learning_phases` describe the small work units and dependencies. Read `active_learning_phase` and `next_proposed_learning_phase` for the current selection. Passing a small phase does not automatically satisfy all acceptance criteria of a capability milestone.

The shared interface is defined by [learning-phase.template.md](learning-phase.template.md). It includes the result, concept, input/dependency requirements, read/change scope, prediction, procedure, completion evidence, rollback and explanation checkpoint. Future sessions record actual results in the registry and retain their detailed run artifacts. Do not invent completion because a card was generated or a build succeeded.

The [master template](master-learning-plan.template.md) and registry render the maintained master/card pages with:

```sh
python3 scripts/render-learning-plan.py
```

Run that command from the project root. It performs local documentation generation only, including the editable first-seven-phase workflow. To refresh its rendered viewer after changing the diagram specification, use the installed Archify skill's full validation/delivery/browser workflow and a fresh review evidence directory. The learning diagram is kept here with the phase documentation, separate from the single core architecture.

The generator applies the template-plus-structured-specification pattern suggested by the user via master-agreement-generator. This is an engineering learning plan; legal agreement clauses, counterparties and signatures are outside its purpose.

The UI gate is unchanged: L16 must show a working preview with the actual React/MUI components/theme and record explicit approval of the shown scope before L17 integration. SkyDive is retained as a separate deferred S01/S02 branch. Hardware H01 and optional search/landing L21–L23 have their own prerequisites. These branches do not block the first simulation/code lessons.
