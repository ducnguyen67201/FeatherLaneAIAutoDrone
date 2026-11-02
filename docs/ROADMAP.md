# Phased development roadmap

[Project home](../README.md) · [Direction](PROJECT-DIRECTION.md) · [Phase registry](phases/registry.json)

These are capability milestones recorded on 2026-10-31, refined by the user's learning-first request. Use the [master learning plan](MASTER-LEARNING-PLAN.md) and its small `Lxx` phase cards for execution order. Existing `Pxx` IDs stay stable for architecture references; they are not single work sessions. P00 documents the direction, P01–P08 cover software/simulation capabilities, and P09 remains optional hardware. L01 source acquisition/orientation and L02 native disarmed SITL qualification are complete; L03 stock simulated takeoff/hold/land/disarm and its guided learner checkpoint are complete. L04’s source walkthrough and guided learner checkpoint are complete. L05’s single stock coordinate flight and guided checkpoint are complete. L06’s same-route speed comparison and guided learner checkpoint are complete. L07’s measured arrival exercise and guided learner checkpoint are complete; P01 and P03 remain in progress. See the [L01 evidence](evidence/l01-source-and-orientation/README.md), [L02 build/run evidence](evidence/l02-basic-sitl-setup/README.md), and [L03 flight evidence](evidence/l03-first-stock-flight/README.md).

The first sequence is L01 source → L02 basic SITL setup → L03 stock flight → L04 source walkthrough → L05 one coordinate → L06 one speed change → L07 measured arrival. Use the stock console before building an application UI. Gazebo is introduced at L12 after the simpler flight baseline. The SkyDive demonstration is a separate deferred branch and does not block SITL learning.

Phase gates below are proposed acceptance criteria, not measured results. Fix the scenario, thresholds and evidence required before implementing each phase. Do not equate a passing build with a successful flight.

## P00 — Direction and documentation baseline

**Outcome:** a separate project folder that records ArduPilot/macOS, the existing prototype, UI requirements, architecture proposals and this roadmap.

**Delivered by this documentation task:** these documents, editable architecture sources, rendered diagrams and a phase registry. The 2026-10-31 user decisions confirm ArduPilot as the core foundation and native mission logic in our maintained ArduPilot-derived code, with the reuse/build distinction. Revised diagram layouts, exact module/mode split, messages and timing budgets remain proposed; no implementation or deployment is recorded. Documentation completion does not complete P01.

## P01 — Project foundation and ArduPilot on macOS

**Target:** clone and qualify upstream ArduPilot as the flight foundation, then use its existing capabilities to complete a basic controlled simulated flight without AI perception.

Deliver:

- Clone upstream ArduPilot into a dedicated checkout, separate from FeatherLane application code. Record its origin, qualified commit and submodule revisions along with the actual Mac architecture, OS and tools. Keep setup reproducible through documented commands and pinned application dependencies. L01 has acquired the untouched source and recursive submodules in the visible `ardupilot/` development checkout (local branch `featherlane/dev`); L02 has qualified the unchanged native macOS build and two fresh disarmed SITL launches, with frozen Python dependencies and clean shutdown. L03 subsequently observed one stock takeoff to 3 m, a declared five-second hold, LAND and automatic disarm; its guided learner checkpoint is complete. L04’s read-only source walkthrough and guided learner checkpoint are complete; P01 still needs the remaining rejected/failed-connection handling evidence. See the [source baseline](evidence/l01-source-and-orientation/README.md) and [L02 record](evidence/l02-basic-sitl-setup/README.md).
- Reuse existing flight control, estimation, navigation/modes, telemetry and failsafes. Qualify an upstream baseline before adding native mission behavior; keep firmware changes identifiable against the pinned revision.
- Establish the maintenance plan for our ArduPilot-derived code: identifiable custom commits, pinned upstream/submodules, a review/integration branch for updates and repeatable manual qualification before adoption. Native in-flight mission logic is the confirmed direction; P01 first proves the upstream baseline so later custom behavior has a reference.
- Establish proposed external Python/uv session tooling, a MAVLink adapter and local run artifacts. The native C++ flight mission component follows upstream baseline qualification. Keep the executable entry point obvious and document start/stop/cleanup.
- Qualify native SITL first. Record a bounded fallback decision if it fails; do not spend indefinitely repairing simulator graphics before validating basic vehicle control.
- Read heartbeat/state, issue supported arm/takeoff/hold/land actions and check their resulting vehicle state. Own and clean up only processes started by the application.
- Document command authority, coordinate frames, units, stale-data limits and the difference between a command acknowledgment and achieved behavior.

**Gate:** from a fresh launch, manually demonstrate takeoff → controlled hold → land → disarm, with telemetry and a complete log. Demonstrate rejected/failed connection handling and clean shutdown without leaving a second controller active. Record simulator limitations. No perception, obstacle avoidance or autonomous target arrival is claimed.

**Learning slices:** L01–L04 establish the stock baseline. L05–L07 then introduce movement concepts; L08–L11 add native task logic in small steps. P02 remains a separate operator/demo capability, with UI preview/integration at L16–L17 and the preserved SkyDive branch at S01–S02.

## P02 — Initial UI and a continuous SkyDive approach

**Target:** start once from the original spawn and approach the selected static helicopter in FPV.SkyDive without intermediate manual corrections.

Deliver:

- Review and reuse the existing screen capture, selected-region tracker, HUD decoding and native key scheduler through a dedicated adapter. Keep this backend separate from ArduPilot.
- Build an isolated, interactive React/MUI preview for simulator selection, reference/target selection, start, stop, observation freshness and run results. Obtain explicit approval before integrating that shown UI.
- Make the model/tracker and command loop asynchronous. Log timestamps and dropped/stale observations. No per-frame cloud/LLM call is required.
- Define the approach envelope and terminal behavior honestly: releasing keys and pausing a game is not a qualified hover or landing. Show the actual stop reason.
- Prevent menu navigation during an ordinary approach. End-of-run pause/review is explicitly labeled. Handle focus loss and operator stop.

**Gate:** three consecutive approaches from the same recorded scene/configuration, with no intermediate Escape/menu checkpoint, target reselection or manual steering. Review each recording for a visible close approach without contact. Record failures as well as successes. This is a visual gate, not proof of distance or collision sensing. If the game cannot provide a reliable controlled terminal stop, record that limitation and carry metric stopping to P03.

**Existing baseline:** one visually reviewed continuous approach in a separate prototype. That does not pass the new repeatability gate. The later user-reported contact remains unresolved.

## P03 — Instrumented ArduPilot missions and trajectory view

**Target:** use real autopilot commands to approach a known spatial destination and stop there in simulation.

**Observed partial progress:** [L05](evidence/l05-one-coordinate/README.md) flew one stock GUIDED GPS-coordinate goal approximately 5 m north at 3 m above home, held at low speed, landed and automatically disarmed. L05 itself included no speed changes, native mission code, Gazebo, UI or failure campaign. [L06](evidence/l06-one-speed-change/README.md) then repeated that route with WP_SPD10->1m/s, observed lower speed/longer travel, landed/disarmed and restored10; its guided learner checkpoint is complete. [L07](evidence/l07-measure-arrival/README.md) then measured entry, slowing and a predeclared two-second sampled hold with data-quality limits; landing/disarm and cleanup followed, and its guided learner checkpoint is complete. [L08](evidence/l08-native-status-slice/README.md) subsequently built/observed one SITL-only native C++ mode/arming observer and selected the preserved stock executable again; the guided learner checkpoint is complete. [L09](evidence/l09-native-task-contract/README.md) then locally built/observed admission-only typed coordinate tasks with bounded fields, explicit reasons and retained-L08 rollback; its guided checkpoint is complete. [L10](evidence/l10-native-known-goal/README.md) now locally builds/executes one admitted goal through SITL-only ModeFeatherLane (mode31), reusing Guided position/attitude control and motor mixing. Its final flight peaked at0.99m/s, completed an externally measured two-second dwell at7.93s and held another50.27s before operator LAND/disarm. Exact-stock rollback and cleanup were observed; the guided checkpoint is complete after clarification. L10 is now published. [L11](evidence/l11-native-arrival-abort/README.md) locally observes native two-second dwell/COMPLETE and continued hold, plus one explicit USER_3 abort through stock BRAKE with measured stopping. Both flights ended with operator LAND/disarm; exact-L10 rollback and cleanup passed. Its guided checkpoint is complete after clarification; L11 is now published. [L12](evidence/l12-instrumented-scene/README.md) locally qualifies a headless Gazebo/official-plugin/stock-SITL flight and rollback, with mesh-collision limits retained. Its guided checkpoint is complete and L12 is published. [L13](evidence/l13-obstacle-observation/README.md) locally observes3m/5m front-lidar returns, narrow coverage/under-range no-return, receiver timeout/recovery and sensor-disabled rollback. The drone remained disarmed and avoidance disabled; guided checkpoint complete after clarification; L13 is published. [L14](evidence/l14-stock-obstacle-stop/README.md) observes stock LOITER stopping before a box with forward input held. Both final cases peak0.49m/s after limiting pilot lean; initial failures, LAND/disarm and baseline rollback are retained. L14 is published with guided checkpoint complete after the3D walkthrough. [L15](evidence/l15-native-obstacle-stop/README.md) locally integrates stock avoidance as a native stop veto, with clear/blocked/observation-loss outcomes and stock rollback observed; guided checkpoint complete after BRAKE clarification, local/unpublished, no detour or L16. These early slices do not complete P03’s broader gate or P01’s remaining failed/rejected-connection handling.

Deliver:

- Qualify ArduPilot plus an instrumented simulator, preferably the official Gazebo plugin. Record a compatible version tuple and native macOS versus isolated Linux placement.
- Start with a known destination position. Establish the local origin, axis conventions, altitude reference, units and command/telemetry time bases.
- Implement bounded native C++ in-flight mission state and supervision in our ArduPilot-derived runtime: starting, flying, approaching, holding, complete, aborting and failed, with transition reasons. Keep connection/session/UI state external. Reuse upstream navigation/controllers, mission facilities where applicable and configured failsafes.
- Qualify the [native mission module/mode design](architecture/README.md), configuration/goal ingress, event telemetry/logging, scheduler budget, coordinate/time/quality contracts and manual override. `ModeFeatherLane` now exists as the narrow L10 SITL adapter; broader `FL_Mission` coordination and lifecycle remain proposed. Stock AUTO/GUIDED remain baseline execution choices; do not assume their message handling automatically works in a new mode.
- Show planned versus actual trajectory, measured vehicle state and explicit localization provenance. Obtain approval for any materially new UI scope before integration.
- Retain ground-truth position, collision events, command acknowledgments and actual stopping behavior. Label early ground-truth-driven control as a privileged baseline.

**Gate:** repeat takeoff → known-position approach → stop/hold → land across several starting poses. Proposed initial arrival criterion: position error ≤1 m, speed ≤0.3 m/s continuously for 2 s, with no collision. Agree/fix suitable values for the chosen simulator before the run campaign. Demonstrate target rejection, command timeout and mission abort. A pause screenshot cannot pass this gate.

**Dependency:** P01. L05–L11 establish coordinate motion/native ownership using basic SITL, L12 adds the instrumented scene, and L16–L17 add the operator UI after its preview approval. These slices contribute to P03; none alone proves the entire milestone. P02 is not a prerequisite for the early flight/code walkthrough.

## P04 — Optional object perception and spatial goals

**Target:** add an optional object-based mission capability that derives a destination from camera/sensor observations. Helicopter approach is the initial example; coordinate missions from P03 do not require this capability.

Deliver:

- Define a mission-selected target rule and capability contract. Select or develop a model that recognizes the chosen target; use the simulated helicopter as the first evaluation case, without hardwiring the mission runtime to that class. Check model classes, weights, license and representative frames before integration.
- Preserve target identity across frames and distinguish an operator-selected image patch from semantic recognition.
- Add calibrated depth/range and camera-to-vehicle/world transforms. Convert target observations into a bounded stopping goal beside the object; avoid setting the goal inside the object.
- Report uncertainty and observation age. Define target loss, ambiguity and reacquisition behavior rather than continuing on an unbounded stale box.

**Gate:** demonstrate acquisition and approach from multiple viewpoints, including false candidates, temporary occlusion and target absence. Compare goal/pose estimates with simulator truth for evaluation only. Record success rate and errors; one good bounding box is insufficient.

**Dependency:** P03. The existing available YOLO weights do not include a helicopter class and cannot be declared suitable without replacement or additional work.

## P05 — Obstacle-aware routes and controlled arrival

**Target:** reach a nearby stopping region through free space with feedback and feasible braking.

**Observed partial progress:** [L14](evidence/l14-stock-obstacle-stop/README.md) qualifies stock LOITER stopping in one front-obstacle scene. [L15](evidence/l15-native-obstacle-stop/README.md) locally adds the native avoidance veto and explicit blocked/invalid BRAKE outcomes, with a clear goal and scan-reader loss exercised. Guided checkpoint complete after BRAKE clarification and user acknowledgment. No detour, general route feasibility or complete P05 gate is established.

Deliver:

- Supply actual proximity/depth data and a local obstacle representation. A target detector alone does not provide obstacle avoidance.
- Qualify ArduPilot's built-in avoidance for the chosen modes and sensor inputs. Use an external planner only where the mission requires behavior beyond that capability.
- Reuse qualified ArduPilot navigation/avoidance first. Where an external planner is necessary, generate feasible routes/references, account for vehicle limits and braking distance, and monitor tracking error. Replan when the valid world/goal estimate changes; ArduPilot continues executing its selected control loops.
- Define blocked route, insufficient clearance and planner timeout outcomes. Stop/hold only when the navigation state supports it.

**Gate:** complete documented layouts with clear passages, blocked passages and a near-goal obstacle. Show actual clearance/collision evidence and controlled terminal speed. A blocked mission should produce an explicit bounded failure or safe fallback instead of contact or indefinite movement.

**Dependency:** P03; P04 is additionally required for object-based scenarios. Coordinate-only obstacle scenarios do not require a target detector. Keep initial speed conservative; increase only after evidence supports it.

## P06 — GPS-denied localization

**Target:** maintain usable position and velocity estimates without satellite navigation.

Deliver:

- Select a sensor/estimator appropriate to the simulator and future payload: visual-inertial odometry or lidar-inertial odometry are candidates, not interchangeable installed features.
- Establish map alignment, initial pose/origin, coordinate transforms, timestamps and estimator quality checks. A map file alone cannot locate the vehicle.
- Feed the validated estimate into ArduPilot using supported external-navigation interfaces, reusing its onboard estimator integration rather than replacing it. Qualify source switching where GPS is initially available.
- Handle drift, feature-poor scenes, degraded sensing and loss of estimate. Keep ground truth outside the autonomous control path.

**Gate:** first fly with GPS unavailable from mission start; then test loss during flight as a separate scenario. Compare trajectory error to truth and demonstrate a feasible fallback when localization quality fails. Completing a mission using hidden simulator position does not pass.

**Dependency:** P03 and a stable nominal controller; combine with P04–P05 only after localization works independently.

## P07 — Ground-link loss and local mission continuity

**Target:** continue an already authorized mission after losing the operator connection when local navigation remains valid.

Deliver:

- Separate the browser/ground link from the companion-to-autopilot link. Configure and document heartbeat ownership and ArduPilot failsafe behavior for each.
- Cache bounded mission configuration in the native runtime and required map/models with their local compute producer before starting. No internet/DNS or cloud decision is required while flying; losing a producer can still invalidate observations.
- Keep the native C++ mission supervisor inside the selected ArduPilot runtime and independent of external UI/session tooling. Reconnecting the UI displays firmware-reported state; it must not silently restart or re-arm a mission.
- Define continue, wait, return or land policies using what the aircraft can actually estimate and execute. Return-to-home is not assumed to work after losing all position information.

**Gate:** separately disconnect the UI, the ground link, the internet and the companion-to-autopilot link. Show the intended distinct outcome and retained local evidence. Then demonstrate GPS loss plus ground-link loss with qualified local navigation. An autopilot-link failure must not be reported as successful autonomous continuation.

**Dependency:** P06 for the combined denial case; nominal ground-link experiments may begin after P03.

## P08 — Repeatability and combined-failure evaluation

**Target:** establish where the system works and where it fails before expanding scope.

Deliver:

- Freeze scenario definitions, seeds/configurations, model weights, simulator/autopilot versions and success/failure rules.
- Evaluate nominal missions and individual faults before combined GPS, link, perception, latency and navigation failures.
- Retain all outcomes with collision count, arrival error, stopping speed, completion time, observation/control latency and recovery behavior where measurable.
- Review startup/shutdown, offline operation, failure explanations and UI state accuracy. Use existing automated checks and manual experiments; do not generate a test suite without the user's request.

**Gate:** complete a predeclared campaign, initially proposed as at least 20 nominal runs plus explicitly counted fault scenarios. Publish the actual counts and outcomes locally, including failures and unsupported cases. The run count is a planning target, not a statistical reliability or certification claim.

**Dependency:** the actually selected/qualified capabilities. Nominal coordinate/avoidance campaigns need their P03/P05 evidence; object campaigns additionally need P04. GPS and link combinations need the relevant P06/P07 gates. Optional search/landing cases need their own L21–L23 qualification. A failed fault gate is fixed before claiming the corresponding combined capability.

## P09 — Optional physical-drone qualification

**Target:** transfer only the proven subset to separately selected hardware.

Deliver only after a separate hardware decision and authorization: flight-controller/companion/sensor selection, calibration, software-in-the-loop/hardware-in-the-loop qualification where suitable, manual baseline flights, supervised nominal autonomous operation, and bounded fault evaluation.

**Gate:** define and review a separate physical validation plan using the selected aircraft and operating environment. Simulation results are evidence for preparation, not proof that a real aircraft is qualified. This phase does not authorize purchases, physical operation or interference/jamming experiments.

## Evidence required at every handoff

Record implemented scope, exact start command, configuration and versions, manually exercised behavior, run artifact locations, actual outcomes and limitations. Keep proposed work distinct from completed work. A phase report can be `planned`, `in_progress`, `ready_for_review` or `complete`; approval and publication are separate events.

No calendar duration is promised yet. P01 will expose machine/setup constraints, and P03 will expose simulator compatibility. Estimate effort after those results rather than inventing a delivery date now.
