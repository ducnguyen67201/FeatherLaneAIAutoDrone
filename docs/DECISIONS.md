# Decisions and open questions

[Project home](../README.md) · [Direction](PROJECT-DIRECTION.md)

Recorded 2026-10-31 from the user's project-planning request. Only choices explicitly made by the user are marked confirmed. Proposed designs are not approved, implemented or deployed by being documented here.

| ID  | Decision / assumption                                                                                            | Status and source                                                                                                     |
| --- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| D01 | Create a separate project under the Desktop workspace. Working name: FeatherLane AI Auto Drone.                  | User requested a new folder; exact display/folder name selected as a working name.                                    |
| D02 | Use ArduPilot as the autopilot.                                                                                  | Confirmed by the user's latest request.                                                                               |
| D03 | Develop from macOS.                                                                                              | Confirmed by the user. Actual machine/toolchain qualification is P01.                                                 |
| D04 | Develop phase by phase, starting with setup, a target-reaching demonstration and later lost-connection behavior. | Confirmed direction. The Pxx capability breakdown is proposed; D17 refines execution into small learning phases.                                                   |
| D05 | Provide a UI for controlling and inspecting missions.                                                            | Confirmed requirement. Visual design and implementation remain unapproved.                                            |
| D06 | First visual scene: FPV.SkyDive on Steam, static helicopter as destination reference.                            | Conversation context. Approach nearby without contact; no moving-aircraft pursuit.                                    |
| D07 | Preserve separate SkyDive and instrumented ArduPilot adapters.                                                   | Proposed architecture based on the absence of a qualified game/autopilot interface.                                   |
| D08 | Use local runtime/control rather than one slow model response per flight action.                                 | Proposed implementation direction addressing the user's observed latency concern.                                     |
| D09 | Prefer conventional autopilot control; add models for perception and estimation where necessary.                 | Proposed; reproducing MonoRace's direct motor controller is outside initial scope.                                    |
| D10 | Interpret earlier “DNS denial” as potentially GPS denial or communication loss.                                  | Unconfirmed wording. Plan covers both separately; literal internet/DNS loss is also considered.                       |
| D11 | External tooling/perception: Python/uv; console: React/MUI/pnpm; MAVLink integration; ROS 2 only if justified. | Proposed packages. Native flight mission placement/C++ is separately confirmed by D15; Python no longer owns that logic. |
| D12 | Keep the initial P00 task documentation-only. | Historical P00 boundary. D18 separately authorizes L01 source acquisition/orientation; application, flight and deployment work remain outside L01. |
| D13 | Treat ArduPilot as the core flight foundation; plan an upstream clone and pin, reuse built-in capabilities and add our application around them. | Confirmed by the user's 2026-10-31 clarification and request to update the architecture/docs. Scope is foundation and reuse/build direction; no clone, firmware change, setup or deployment performed. |
| D14 | Earlier proposal: external Python mission handlers/supervision. | Superseded by D15 on 2026-10-31. Standard AUTO/GUIDED remain available for baseline qualification; external Python no longer owns the planned ArduPilot flight mission lifecycle. |
| D15 | Maintain our own ArduPilot-derived code with native C++ in-flight mission logic/supervision; integrate upstream updates deliberately while retaining our changes. | Confirmed by the user's 2026-10-31 message: “This is plan and rule, and we would maintain it.” The accepted scope is placement and maintenance direction. Proposed library/mode names, contracts and new diagram layouts are not separately approved; no clone, firmware implementation or deployment is performed. |
| D16 | Mission-driven optional perception: support coordinate/route tasks without a detector and object-dependent steps using qualified target perception/localization. Helicopter is one example target, not the core mission definition. | Confirmed by the user on 2026-10-31: detection is optional; examples include going to GPS point A or detecting a helicopter and approaching it. Exact schema, supported targets and revised diagram layouts remain proposed; no implementation is recorded. |

| D17 | Organize work under one master learning plan with small focused phases and a shared phase-card interface; first acquire source, set up basic SITL, observe a stock flight and connect it to code. | Confirmed by the user on 2026-10-31: learn by doing and keep code small/focused. The Lxx cards refine existing Pxx capability milestones; detailed cards/layouts remain proposed. This task produces planning documents, not a clone, install or flight. |

| D18 | Execute L01 only: acquire official upstream source locally, pin its commit/submodules and learn the main folders. | User-authorized phase launch on 2026-10-31. Selected source baseline: `Copter-4.7.2`, `fb773567896014da007bca58358704d4a0d8516f`. [Observed execution](evidence/l01-source-and-orientation/README.md); no build/simulator/flight qualification or remote fork/push. Selection of this source revision is an implementation choice, not user approval of a qualified build. User follow-up on 2026-10-31 clarified that this is our development source, not temporary acquisition storage: moved the checkout to visible `ardupilot/`, with local branch `featherlane/dev`; exact baseline/submodules unchanged. |

The earlier documentation request did not approve the rendered layouts, full detailed architecture or UI. D18 authorizes only the subsequent L01 source/orientation work; the approval flags remain unchanged. See the [architecture approval record](architecture/README.md#direction-and-diagram-approval-record).

## Repository publication

On 2026-10-31 the user requested publication on their GitHub profile, selected **public**, and then selected **Full project + linked firmware fork**. The project repository is [FeatherLaneAIAutoDrone](https://github.com/ducnguyen67201/FeatherLaneAIAutoDrone); its `ardupilot/` submodule pins the [FeatherLaneArduPilot](https://github.com/ducnguyen67201/FeatherLaneArduPilot) firmware fork. The development branch remains `featherlane/dev` at the unchanged L01 baseline. This authorizes repository creation and source publication, without changing L02 status or firmware/UI/architecture qualification. See the [repository guide](REPOSITORIES.md).

## Questions to resolve during the relevant phase

- **P01:** exact Mac architecture/OS; native SITL compatibility; qualified MAVLink command set and simulator fallback if required.
- **P02:** precise SkyDive spawn/settings, input mapping, repeatability limits and whether a terminal controlled stop is achievable through the available interface.
- **P03:** compatible simulator/autopilot versions, coordinate conventions and arrival thresholds; whether an isolated Linux runtime is necessary.
- **P04:** supported target definitions/models (helicopter as the initial example), representative imagery, camera calibration and depth/range source. “YOLO ready” does not prove this model supports the target.
- **P05:** built-in avoidance sufficiency versus an external planner, and the actual required obstacle geometries.
- **P06:** availability/type of map, initial localization, sensor payload, acceptable drift and GPS-denied mission limits.
- **P07:** exact link being lost and the permitted continue/abort policy for each mission state.
- **P09:** whether physical hardware is wanted at all; aircraft, payload, budget and operating context if so.

These questions do not block creation of the plan. Resolve them before the implementation steps that depend on their answers.

## Change policy

Update direction, roadmap, registry and diagrams together when a decision changes. Record approval source/date/scope for approved designs; do not treat approval of a diagram as implementation evidence. Keep future app implementation, external publication and physical operations scoped to their own authorization.
