# L01 — ArduPilot source baseline and folder orientation

**Retention update — 2026-11-02:** generated CSV/TXT exports were removed at the user’s request. References below describe the original export provenance; retained summaries/figures and source/recording identities remain. See the [retention note](../README.md).

[Project home](../../../README.md) · [Learning card](../../phases/learning/l01-source-and-orientation.md) · [Master plan](../../MASTER-LEARNING-PLAN.md) · [Registry](../../phases/registry.json)

Executed 2026-10-31 (America/Toronto). **Source acquisition and guided orientation complete. P01 remains in progress; L02 is next and has not started.** This is an unchanged source baseline, not a qualified build, simulator or flight result.

## Concept and prediction

A source checkout is a local copy of the code. A commit identifies one exact saved version. A submodule is another Git repository whose revision is recorded by its parent. A built flight executable is the runnable program produced from source for a selected target; acquiring the source does not produce that program. The root `waf` script can itself be executable, but it is a build launcher rather than the flight program.

Before acquisition, the prediction was: the dedicated checkout will contain `ArduCopter/`, `libraries/`, `Tools/` and `waf`, with clean source and matching pinned submodules; no executable build or flight is expected. The observed result matches this prediction.

## Selected source and location

| Item | Observed value |
| --- | --- |
| Current development checkout | `/Users/ducng/Desktop/workspace/FeatherLaneAIAutoDrone/ardupilot` |
| Official upstream source | `https://github.com/ArduPilot/ardupilot.git` |
| Current development origin | `https://github.com/ducnguyen67201/FeatherLaneArduPilot.git` |
| Selected release tag | `Copter-4.7.2` |
| Exact source commit | `fb773567896014da007bca58358704d4a0d8516f` |
| Checkout state | Local branch `featherlane/dev` at the baseline commit; no custom commits or flight-code edits |
| History | Shallow, single release checkout; full upstream history was not downloaded |
| Recursive submodules | 21 initialized checkouts, all matching their parent gitlinks and individually clean |
| Qualification | Source only; no dependency installation, build, SITL session or flight performed |

The source was initially acquired under `.local/upstream/ardupilot`. After the user clarified that this is the long-lived development checkout, it was moved to the visible project-root `ardupilot/` folder and local branch `featherlane/dev` was created at the same baseline commit. The destination was absent before the move. All 21 recursive submodules still resolve correctly; the source content, origin and commit are unchanged. See the [relocation record](checkout-relocation.json). The surrounding documentation project still has no `.git` directory. No write was issued to `FeatherLaneFlight`, `skydive-control-dogfood` or unrelated private paths; their contents were not independently audited.

The official [source-download guidance](https://ardupilot.org/dev/docs/where-to-get-the-code.html) and [clone instructions](https://ardupilot.org/dev/docs/git-clone.html) identify the upstream repository. The live [Copter-4.7.2 release page](https://github.com/ArduPilot/ardupilot/releases/tag/Copter-4.7.2) describes this as the stable/official Copter release from 11 October 2026. The Git tag resolved to the commit above before cloning, and the local tag and HEAD were checked afterward. Choosing a fixed release provides a bounded source reference for learning; it does not establish compatibility with this Mac. The earlier architecture research revision `363ab1b5efdb67a0d0ade62984685b6d44d0f40d` was not adopted as the project baseline.

Historical acquisition commands, run from the project root with the original destination absent (the current checkout is now `ardupilot/`):

```sh
git clone --depth 1 --single-branch --branch Copter-4.7.2 --no-recurse-submodules https://github.com/ArduPilot/ardupilot.git .local/upstream/ardupilot
git -C .local/upstream/ardupilot submodule update --init --recursive --depth 1 --jobs 4
```

The committed `.gitmodules` was inspected before initialization. Submodule update used the parent commit's pins, without `--remote`; it did not adopt each dependency's latest branch. Nested submodules are included in the record. The official [submodule guide](https://ardupilot.org/dev/docs/git-submodules.html) is background guidance; the selected commit's actual recursive structure is the evidence here. No Git global configuration or credentials were changed, and no remote fork, push or publication was created.

For a later fresh acquisition, verify `HEAD` and the tag against the exact recorded commit before proceeding; a tag name alone is not an immutable pin. The shallow history is sufficient for this source walkthrough; later upstream comparison/maintenance may require deliberately fetching more history.

## Short walkthrough of the actual source

All paths below are relative to this selected checkout. Links point to the exact pinned upstream revision. These are file-role observations, not a full command trace or runtime qualification.

| Where to look | Plain-language role and inspected example |
| --- | --- |
| `ArduCopter/` | Vehicle-specific behavior. A flight mode chooses the behavior for the active vehicle task. [`mode_guided.cpp:64`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/mode_guided.cpp#L64) dispatches Guided behavior; [`Copter.cpp:113`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/Copter.cpp#L113) lists recurring work, including sensors, controllers and mode updates. This revision uses `Copter.cpp`, not an assumed `ArduCopter.cpp`. |
| `libraries/` | Reused building blocks. A controller compares desired movement with estimated movement and adjusts its output. [`AC_PosControl.h:38`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_AttitudeControl/AC_PosControl.h#L38) and [`AC_AttitudeControl.h:47`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_AttitudeControl/AC_AttitudeControl.h#L47) define position and orientation control. Both live in `libraries/AC_AttitudeControl/`. [`AC_WPNav.h:17`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_WPNav/AC_WPNav.h#L17) defines waypoint navigation, which turns destinations into motion references using controllers. |
| `Tools/` | Developer utilities. [`Tools/autotest/sim_vehicle.py:1`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/Tools/autotest/sim_vehicle.py#L1) describes the simulation launcher. Its build and launch functions were read, not run. It is external tooling, not the authoritative in-flight mission runtime. |
| Root `waf`, `wscript`, `ArduCopter/wscript` | Build entry point and recipes. [`waf:20`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/waf#L20) locates `modules/waf/waf-light`; root `wscript` describes configuration/build work, and [`ArduCopter/wscript:3`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/wscript#L3) lists vehicle libraries and program targets such as `arducopter`. None was invoked. |
| `modules/` and `.gitmodules` | Pinned external source dependencies, including the Waf build tool and MAVLink definitions. Their presence is source acquisition, not installation of Python packages or qualification of a toolchain. |

The connection is visible in [`ArduCopter/Copter.h:476`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/Copter.h#L476): the vehicle holds `AC_AttitudeControl`, `AC_PosControl` and `AC_WPNav` objects. Copter-specific behavior uses these library components. Reading that relationship does not demonstrate that any controller ran.

## Retained evidence and limits

- [Revision manifest](source-baseline.json): exact main commit, credential-free origins and all 21 recursive submodule revisions, including nested dependencies.
- Raw recursive submodule listing (generated export removed): each line starts with a space, indicating a checkout matching its parent's recorded commit.
- Observed Git output (generated export removed): origin, HEAD/tag identity, commit metadata, shallow status, empty worktree status and empty diff. Every submodule was also checked individually with untracked files included.
- Manual inspection confirmed the main folders and cited source declarations. The checkout had no `build/` directory, and no build launcher or simulator script was executed.
- This is agent-observed evidence, not independent verification, signature authentication, build qualification or flight evidence. The Mac toolchain and simulator compatibility remain unexamined in L01.
- No new automated tests, snapshots or test scaffolding were authored or run. Upstream test sources arrived unchanged as part of the requested source checkout.

The supplied supplement references `docs/CODEX-NAVIGATION-GUIDE.md`; that file is absent in this project. Project `AGENTS.md`, README, direction, roadmap, master plan, registry and L01 card were read. No navigation guide or inherited PX4 phase dispatcher was invented.

## Learning checkpoint, status and rollback

The learner answered “ArduCopter here ?” to the folder question. The assistant confirmed `ArduCopter/` for vehicle behavior and clarified `libraries/AC_AttitudeControl/` for reused controllers. This is a guided checkpoint; independent mastery of both locations is not claimed.

L01 is complete for source acquisition and guided orientation. P01's build/flight gate remains unmet. L02 is the next small phase, subject to its own scope; it was not started. UI and architecture approval flags remain false, and no proposed custom module is implemented.

The unchanged release tag and recorded commit/submodule set retain the flight-code baseline. The local `featherlane/dev` branch is ready for later scoped development in `ardupilot/`; future custom changes should be identifiable commits on that branch or task branches derived from it. No reset or cleanup command was applied to unrelated paths.

Pre-edit copies of the maintained documents, generator and generated learning assets are retained locally at `.local/l01-source-orientation/rollback/` with their project-relative paths. If rolling back this session, compare and restore only the relevant task-owned changes; preserve any later edits. Keep the evidence and source baseline unless removal is separately requested. The acquired checkout can remain parked unused while L02 is deferred.

Documentation changes record the source pin and actual phase state, link this evidence, and refresh the existing learning workflow. They do not alter the proposed flight architecture or its approval requirements. Design documents and diagrams do not qualify the selected source; current execution status lives in the registry and this record. The separate documentation-consolidation chat may relocate design assets; it does not change this source baseline.

Handoff checks resolved 89 local Markdown file targets in the L01/status documents, confirmed unchanged future phase specifications and approval flags, and repeated the existing generator with identical output for the master plan, 30 cards and workflow JSON. The [refreshed learning workflow](../../assets/learning/learning-workflow.svg) and [editable source](../../phases/learning-workflow.json) passed fresh Archify validation, delivery/provenance and real-browser checks at their consolidated paths. Automated diagram evidence is retained locally under `.archify/workflow-l01-source-status-20261031/review-2/`; no perceptual review or user diagram approval is claimed. A final Git check still found the source clean and all 21 recursive submodules matching.

The location correction has its own pre-edit documentation copies under `.local/l01-checkout-location-correction/rollback/`. The [relocation record](checkout-relocation.json) preserves before/after Git and submodule state. The original acquisition commands and raw Git evidence above remain historical observations rather than being rewritten as if the source had originally been cloned into the new path.

On 2026-10-31 the user separately authorized public publication of the full project plus a linked firmware fork. The surrounding folder is now a Git repository, and `ardupilot/` is its pinned submodule. Firmware `origin` points to the [development fork](https://github.com/ducnguyen67201/FeatherLaneArduPilot); remote `upstream` preserves the official ArduPilot source. The development branch was published at the unchanged baseline commit. Initial acquisition/relocation evidence above records the earlier state; it does not describe current publication status. See the [repository guide](../../REPOSITORIES.md).
