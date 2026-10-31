# Project and firmware repositories

[Project home](../README.md) · [Learning plan](MASTER-LEARNING-PLAN.md) · [Source baseline](evidence/l01-source-and-orientation/README.md)

The user authorized public publication on 2026-10-31 and selected the full project plus a linked firmware fork.

| Repository | Contents | Working branch |
| --- | --- | --- |
| [FeatherLaneAIAutoDrone](https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone) | Project documentation, phase registry, evidence and future application/tooling | `main` |
| [FeatherLaneArduPilot](https://github.com/ducnguyen67201/FeatherLaneArduPilot) | ArduPilot-derived flight source with upstream history and license files retained | `featherlane/dev` |

The visible `ardupilot/` folder is a Git submodule: the project records an exact firmware commit rather than copying or flattening its history. The initial published firmware pin is `fb773567896014da007bca58358704d4a0d8516f` (`Copter-4.7.2`), with its unchanged recursive submodules. The server-side fork retains upstream history; the existing local checkout is still shallow.

## Clone on another machine

```sh
git clone --recurse-submodules https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone.git
cd FeatherLaneAIAutoDrone
```

Git checks out the exact recorded firmware revision. A detached submodule HEAD after cloning is normal. Before editing firmware, select its development branch:

```sh
git -C ardupilot switch featherlane/dev
```

This does not install dependencies, build ArduPilot or launch a simulator. Follow the appropriate learning card for those operations. To restore missing submodule source at the recorded pins, use `git submodule update --init --recursive`, without `--remote`.

## Where changes belong

- Edit project documents and future external application/tooling from the project root.
- Edit native flight code inside `ardupilot/`. It has its own Git history and commits. Use `git -C ardupilot status` to inspect those changes.
- After an authorized firmware commit/push, the parent project can record its new pin with `git add ardupilot` and a project commit. Publish the firmware commit before publishing a project pointer to it.
- Git operations and code changes do not establish build or flight qualification. L02 remains planned; the current source is unchanged from upstream.

In the firmware checkout, `origin` is `https://github.com/ducnguyen67201/FeatherLaneArduPilot.git`, and `upstream` is `https://github.com/ArduPilot/ardupilot.git`. New recursive clones set `origin` from `.gitmodules`; they can add the credential-free upstream remote when needed. Fetching or integrating an upstream update is separate reviewed work. Do not run `git submodule update --remote` as a routine setup step: it can select a different firmware revision.

## Publication scope

The initial project commit includes maintained documentation, editable diagram sources, static diagram assets, the existing Word design export, phase/evidence records, the documentation generator and the firmware gitlink. The Word export retains its design-time context; the live registry and source records carry current execution status.

`.local/`, `.archify/`, generated HTML viewers, review receipts, logs, environment files, credentials, dependencies and build outputs are excluded. The separate `FeatherLaneFlight` and SkyDive checkouts are not part of either publication. Static diagrams are available in [the core architecture](architecture/README.md) and [the learning plan](MASTER-LEARNING-PLAN.md); their editable JSON sources remain beside their maintained documentation. No new application license or qualified release is declared by this initial publication.
