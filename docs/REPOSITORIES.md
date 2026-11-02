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
- Git operations and code changes do not establish build or flight qualification. [L02 separately qualified the unchanged native build and two disarmed SITL launches](evidence/l02-basic-sitl-setup/README.md); [L03 observed one bounded stock simulated flight](evidence/l03-first-stock-flight/README.md), with its guided learner checkpoint complete and P01 still in progress. This L02/L03 statement concerns the stock baseline; the later L08 custom commit is recorded below.

In the firmware checkout, `origin` is `https://github.com/ducnguyen67201/FeatherLaneArduPilot.git`, and `upstream` is `https://github.com/ArduPilot/ardupilot.git`. New recursive clones set `origin` from `.gitmodules`; they can add the credential-free upstream remote when needed. Fetching or integrating an upstream update is separate reviewed work. Do not run `git submodule update --remote` as a routine setup step: it can select a different firmware revision.

## Publication scope

The initial project commit includes maintained documentation, editable diagram sources, static diagram assets, the existing Word design export, phase/evidence records, the documentation generator and the firmware gitlink. The Word export retains its design-time context; the live registry and source records carry current execution status.

`.local/`, `.archify/`, generated HTML viewers, review receipts, raw run logs, secret-bearing environment files, credentials, dependencies and build outputs are excluded. Selected L02 console transcripts, version/configuration manifests and result summaries are maintained under `docs/evidence/l02-basic-sitl-setup/`; these are the curated phase record, not the local runtime environment. The separate `FeatherLaneFlight` and SkyDive checkouts are not part of either publication. Static diagrams are available in [the core architecture](architecture/README.md) and [the learning plan](MASTER-LEARNING-PLAN.md); their editable JSON sources remain beside their maintained documentation. No new application license or qualified release is declared by this initial publication.

L03 is local work on `codex/l03-first-stock-flight`, based on published L02 commit `7a2c6652dbd8088b66d8d9c2cb123c0bc52a78ee`. The user subsequently authorized committing/pushing its maintained phase record on this branch before moving to L04. Publication does not include a merge or update to `main`. Its curated evidence is under `docs/evidence/l03-first-stock-flight/`; raw telemetry and onboard logs remain ignored under `.local/l03/`.

L03 publication was verified at commit `fd6ae48fec7530164ada79f2f255f272a0e5a325`; remote `main` remained `c45c9e19ae279011d5779fa2669df3fac0f21a29`. L04’s read-only source walkthrough was prepared on `codex/l04-trace-one-command`, branched from the published L03 commit. After the checkpoint, the user separately authorized committing/pushing L04 before starting L05. This does not include merging/updating `main` or publishing L05.

L04 publication was verified at commit `c0f6254470fea3c4c22d4de43cfae0df21cef07d`; `main` remained unchanged. L05 was prepared on `codex/l05-one-coordinate`, branched from that L04 commit. Its curated flight/coordinate evidence is under `docs/evidence/l05-one-coordinate/`; raw runs, local capture/processing helpers and dependencies remain ignored. The user subsequently authorized committing/pushing this completed L05 record before starting L06; no main merge/update or L06 publication is included.

L05 publication was verified at `9dd52dc050401887de4b4d352d26b368c2a54251`; `main` stayed unchanged. L06 was prepared on `codex/l06-one-speed-change`, branched from that L05 commit. Its curated comparison/evidence is under `docs/evidence/l06-one-speed-change/`; raw runs and full parameter snapshots remain ignored under `.local/l06/`. The user subsequently authorized committing/pushing the completed L06 records before L07; no main merge/update or L07 publication is included.

L06 publication was verified at `c26ffa094744a8c4122af60ab91ca13534b3d9f9`; `main` stayed unchanged. L07 is local, uncommitted work on `codex/l07-measure-arrival`, branched from that L06 commit. Its curated contract/timeline/evidence is under `docs/evidence/l07-measure-arrival/`; raw runs and local helpers remain ignored under `.local/l07/`. No L07 commit, push or merge was performed.


L08 starts on local `codex/l08-native-status-slice` branches in both repositories. The parent inherits all unpublished L07 documentation/evidence without discarding it. Firmware HEAD remains the pinned `fb773567896014da007bca58358704d4a0d8516f`; L08’s five-file addition is an identifiable working diff. The clean baseline branch `featherlane/dev` is preserved. The isolated custom output is `.local/l08/build/`; the original stock binary and an exact retained copy remain available. See [L08 evidence](evidence/l08-native-status-slice/README.md). No L07/L08 push or merge is authorized or performed.


The user subsequently authorized L07/L08 publication before L09. Firmware commit `3f467d90be284654c5721ac3d94c26863f771275` on `codex/l08-native-status-slice` contains only the observed five-file SITL status observer against the preserved stock base. The parent publication records that exact commit and the completed L07/L08 evidence. Main and `featherlane/dev` remain unchanged; L09 publication requires separate authorization.


L07/L08 publication was remote-SHA verified at project `09c3229e3ed4cb7d9a8998b1f85ec16def0448a8` and firmware `3f467d90be284654c5721ac3d94c26863f771275`. The parent gitlink points to that published firmware commit. Copied transcript whitespace was normalized in follow-up documentation commits; raw logs and applicable patch context were preserved. Main and the stock firmware branch did not change. L09 starts locally on `codex/l09-native-task-contract` in both repositories, with the published L08 source/executable as rollback.


The user subsequently authorized publishing completed L09 before L10. Firmware commit `39cf614d1aae2ee4acb93f9294ebf66178967acb` on `codex/l09-native-task-contract` contains the six-file admission-only slice and the requested naming/comments/build-list refinements. Its remote SHA was verified before preparing the parent pointer. The project publication includes the durable AGENTS.md coding convention and maintained evidence. Main and the stock firmware branch remain unchanged; L10 publication is outside this authorization.


L09 project publication is now verified at `d8afe552351f4f246822857c49a6fa37edbc0bc7`, with gitlink `39cf614d1aae2ee4acb93f9294ebf66178967acb`. Both current local branches are `codex/l10-native-known-goal`, rooted in those published commits. L10 is an uncommitted seven-file firmware integration, with its exact patch, source/submodule manifest, separate build binary, nominal flight and rollback retained in [L10 evidence](evidence/l10-native-known-goal/README.md). No L10 publication or main/stock update occurred. The final native mode31 run and exact-stock rollback are observed; guided checkpoint pending.

L10 firmware publication is remote-SHA verified at `11573fb26ffe99022431a32d0b40502d03f9b02a` on `codex/l10-native-known-goal`; its seven-file patch is identical to the final observed L10 source. The parent feature commit records this exact gitlink. The user authorized publishing both feature branches on2026-11-02 before local L11.


L10 parent publication is remote-SHA verified at `d0f30a8f1c33af2f54740fc2b0675f453e0d5ba2`, linking firmware `11573fb26ffe99022431a32d0b40502d03f9b02a`. L11 branches are local `codex/l11-native-arrival-abort` in both repositories; firmware HEAD/gitlink remain published L10 with an uncommitted four-file lifecycle diff. [L11 evidence](evidence/l11-native-arrival-abort/README.md) retains the exact patch, isolated build, actual nominal/abort flights and preserved-L10 rollback. No L11 push or main/stock update occurred.

L11 firmware publication is remote-SHA verified at `a00f32be2a91639c8dee1c41c09e1c5e5635d547` on `codex/l11-native-arrival-abort`, matching the recorded final-source four-file lifecycle patch. The parent feature publication records that exact gitlink; the user authorized both repositories before local L12.


L11 parent publication is verified at `56b32a2c6d10bc58a85ae4ebab4ff98520da3acc`, linking firmware `a00f32be2a91639c8dee1c41c09e1c5e5635d547`. L12 uses local branches `codex/l12-instrumented-scene` with no firmware working diff. New scene/build/launch/lock files live in `simulation/gazebo/`; simulator/plugin builds, pinned third-party checkout and raw logs stay ignored under `.local/l12/`. [L12 evidence](evidence/l12-instrumented-scene/README.md) qualifies one stock external-physics flight plus fresh connection/rollback with explicit limits. No L12 publication or main/stock update occurred.
