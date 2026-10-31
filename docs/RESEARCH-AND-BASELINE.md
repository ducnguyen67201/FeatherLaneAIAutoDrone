# Research and existing baseline

[Project home](../README.md) · [Direction](PROJECT-DIRECTION.md) · [Roadmap](ROADMAP.md)

Captured 2026-10-31. This is a practical starting bibliography and a record of this conversation's prototype evidence, not an exhaustive literature review or independent reproduction of the referenced systems.

## What the racing research contributes

The original discussion began with TU Delft's [science behind the autonomous racing drone](https://www.tudelft.nl/en/2026/tu-delft/the-science-behind-worlds-fastest-autonomous-racing-drone). The article URL was not directly accessible during this documentation pass; technical details below use the authors' [MonoRace preprint](https://arxiv.org/abs/2601.15222).

MonoRace combines monocular vision, an IMU and model-assisted state estimation, using known racing-gate geometry for calibration/refinement. Its compact learned controller outputs motor commands at a reported 500 Hz. That is a specialized trained system; replacing the gate label with “helicopter” does not supply the missing geometry, state estimate or control policy. These are author-reported results, not performance measured in our prototype. [MonoRace](https://arxiv.org/abs/2601.15222)

The transferable lesson is to maintain a timely motion estimate and close the control loop locally. Our initial priority is reliable arrival and controlled stopping. We do not need to reproduce a racing network or optimize for maximum speed.

Other useful research references include [Swift / champion-level drone racing](https://www.nature.com/articles/s41586-023-06419-4) and [Learning High-Speed Flight in the Wild](https://rpg.ifi.uzh.ch/AgileAutonomy.html), with its [research code](https://github.com/uzh-rpg/agile_autonomy). Treat training environments, sensors, assumptions and licenses as part of each method. No MonoRace source repository has been qualified as a dependency in this plan.

## What frameworks actually provide

| Layer / framework                                                                                                           | Useful starting capability                                                      | Work still belonging to this project                                                                  |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [ArduPilot](https://ardupilot.org/dev/docs/companion-computers.html)                                                        | Flight control, estimation, missions, supported external commands and failsafes | Task semantics, perception, spatial goals, suitable sensor/estimator integration and mission policies |
| [PX4](https://docs.px4.io/main/en/ros2/px4_ros2_interface_lib)                                                              | Alternative autopilot with external ROS 2 mode/control interfaces               | The same high-level autonomy integration; not a required second backend here                          |
| [ROS 2 integration for ArduPilot](https://ardupilot.org/dev/docs/ros2.html)                                                 | Middleware interfaces and access to robotics components                         | Sensor/frame/time integration, lifecycle management and behavior validation                           |
| [Aerostack2](https://aerostack2.github.io/) / [source](https://github.com/aerostack2/aerostack2)                            | ROS 2 aerial-robotics framework with mission/behavior components                | A compatible platform, configuration and the specific perception/navigation mission                   |
| [CMU AirStack](https://github.com/castacks/AirStack)                                                                        | Research autonomy/simulation integration to study                               | Compatibility, compute requirements and adaptation; not a qualified native Mac dependency             |
| [Agilicious](https://github.com/uzh-rpg/agilicious)                                                                         | Agile-flight research stack                                                     | Hardware/software fit and access/license review before adoption                                       |
| [EGO-Planner](https://github.com/ZJU-FAST-Lab/ego-planner) / [EGO-Swarm](https://github.com/ZJU-FAST-Lab/ego-planner-swarm) | Candidate trajectory-planning research                                          | Supported ROS branch, maps/odometry inputs, vehicle interface and collision/latency validation        |

ROS 2 is middleware; an autopilot is a flight-control system; a mission framework organizes behaviors. They are complementary layers. Adding all of them does not automatically produce a fully autonomous drone. Use the smallest combination that passes the current phase.

The separate [aerial-autonomy-stack](https://github.com/JacopoPan/aerial-autonomy-stack) should not be confused with CMU's AirStack. Research repositories may have different supported operating systems, ROS versions and hardware assumptions. The original [Fast-Planner](https://github.com/HKUST-Aerial-Robotics/Fast-Planner) and [VINS-Fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) are useful references, not drop-in promises for a new ROS 2/macOS application.

## ArduPilot references for this roadmap

- [Guided mode](https://ardupilot.org/copter/docs/ac2_guidedmode.html): external commands and mode-specific options; qualify target update behavior.
- [BendyRuler](https://ardupilot.org/copter/docs/common-oa-bendyruler.html) and [proximity sensors](https://ardupilot.org/copter/docs/common-proximity-landingpage.html): avoidance needs suitable observations and supported modes.
- [Non-GPS navigation](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html) and [external pose/velocity estimates](https://ardupilot.org/dev/docs/mavlink-nongps-position-estimation.html): alternative positioning is a separate subsystem.
- [Ground-station failsafe](https://ardupilot.org/copter/docs/gcs-failsafe.html): link loss is configured behavior, distinct from navigation loss.
- [Official Gazebo integration](https://ardupilot.org/dev/docs/sitl-with-gazebo.html), [plugin source and platform notes](https://github.com/ArduPilot/ardupilot_gazebo/blob/main/README.md), and [ROS 2/Gazebo setup](https://ardupilot.org/dev/docs/ros2-gazebo.html): qualify a compatible setup rather than mixing unrelated installation guides.
- [ArduPilot licensing explanation](https://ardupilot.org/dev/docs/license-gplv3.html): review firmware modifications and companion software separately when distribution becomes relevant.

## Existing SkyDive prototype

Location: `/Users/ducng/Desktop/workspace/skydive-control-dogfood`. This is an existing separate experiment, not code installed in the new project.

It uses native macOS screen capture/input, a selected-region optical-flow tracker, HUD extraction and a bounded key scheduler. It is a feedback-based image-space approach. It does not contain a qualified map, metric pose/velocity estimator, obstacle avoidance, landing controller or stable terminal-hover controller. It does not repeatedly ask a general-purpose language model to choose each flight action.

The documented continuous run is in `runs/continuous-arrival-20261030/` inside that prototype:

| Recorded property                                     | Result                                                      |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| Run                                                   | `continuous-flight-01`                                      |
| Start                                                 | Original ground spawn, throttle zero; HUD altitude 29       |
| Duration                                              | Approximately 42.724 seconds                                |
| Observations                                          | 457; one skipped observation                                |
| Manual steering during run                            | None recorded                                               |
| Intermediate checkpoint resumes / target reselections | Zero / zero                                                 |
| Automatic stop                                        | `visual_threshold_needs_review`                             |
| Automatic arrival verified                            | False                                                       |
| Saved visual review                                   | Close beside the helicopter over its pad; paused at the end |

Source: `visual-review.json`, alongside the JSONL log, summary and stop-frame capture. This is one successful visual review under one configuration. It does not establish measured distance, repeatability, controlled landing or hover. Earlier paused/checkpoint trials are not equivalent to one continuous flight.

The user subsequently reported touching “some target” and stopping. The object and cause were not diagnosed. Preserve that as an unresolved collision/contact report, not another success.

The earlier `operator_stop` output with zero observations means the operator stopped before the system recorded an active tracking observation; it provides no evidence of autonomous progress or arrival. Run summaries and actual footage must be interpreted together.

## Detector status

The available weights at `/Users/ducng/Desktop/workspace/RedTeamHackathon/TeamWolley/models/vehicle_detector.pt` have classes `tank`, `boat`, `jet` and `ice_cream_truck`. They do **not** contain `helicopter`. The SkyDive approach used region tracking; a close approach does not prove semantic helicopter detection. P04 must qualify an appropriate model and imagery.

Do not copy unrelated private data, credentials, models or the old project's implementation into this folder automatically. Review scope and licenses when reusing specific components.

## Further local background

The existing prototype also has `VERIFICATION.md` and `research/autonomous-drone-landscape-2026-10-31.md`. Treat these as historical background. The new project's maintained direction and phase status live here; the original `FeatherLaneFlight` project remains separate and unchanged.
