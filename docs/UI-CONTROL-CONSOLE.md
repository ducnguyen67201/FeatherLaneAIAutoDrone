# Control-console requirements

[Project home](../README.md) · [Roadmap](ROADMAP.md) · [Architecture](architecture/README.md)

Status: proposed product requirements, 2026-10-31. No application UI or approved visual design exists in this folder. The architecture viewers are documentation, not a product UI preview.

## Operator flow

1. Select the simulator backend while idle. Show its actual capabilities and connection state.
2. Select or load a mission type and destination: GPS/local coordinate, supported route or object approach. For SkyDive, capture a fresh reference and select the target region; later phases add semantic acquisition and a spatial map goal.
3. Review the starting state, observation freshness, mission limits and stop policy. Start is unavailable until the selected backend's preconditions pass.
4. Start once. Show actual mission progress and the planned versus observed movement when that backend supplies the data.
5. Complete, abort or stop with an explicit reason and a retained run record.

For ArduPilot missions, show coordinate/frame/altitude fields for coordinate tasks and target/model/selection fields only for object-dependent steps. Show required capability readiness per mission. A missing optional detector must not disable Start for a valid coordinate mission; a missing required perception or localization capability must explain why its step cannot start. Video/target-loss indicators are conditional on the selected task. This is a requirements update, not UI preview approval.

## Initial P02 screen

Use one local operator screen with a backend selector, connection/mission state, camera view, target-selection overlay, observation age, mission settings, Start/Stop controls and a compact event/result panel. Do not add accounts, cloud fleet management or billing.

The UI must distinguish “selected image region” from “helicopter detected.” Show unavailable position/distance as unavailable, not zero. A confidence score does not establish physical range. Label fixture data as simulated in the isolated preview.

Changing backends, target or command profile while a run is active is rejected or requires an explicit stopped transition. Prevent duplicate starts and show command acknowledgment separately from achieved vehicle state.

## Status and command semantics

Display mission state, vehicle state, telemetry connection, video freshness and navigation quality independently. An open browser does not prove a live vehicle connection. Use timestamps and a visible stale/unknown state.

| Action       | SkyDive meaning                                                                          | ArduPilot simulation meaning                                                 |
| ------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Start        | Begin the configured screen/input approach after focus/reference checks                  | Start the validated mission after vehicle/estimate/command checks            |
| Stop / Abort | Release held inputs and attempt a labeled simulator pause; report what actually occurred | Request the configured supported abort behavior and monitor vehicle response |
| Hold         | Not claimed until game control is separately qualified                                   | Available only when the flight mode and navigation state support it          |
| Complete     | Visual threshold plus required review; never invent measured arrival                     | Require the phase's measured arrival and terminal-state criteria             |

In the prototype, throttle can remain set while the game is paused; resuming manually can move the drone. A paused game must not be labeled landed or stable hover. Do not make airborne disarm a generic Stop button.

## Later additions

P03 adds a local coordinate view, planned and actual trajectories, altitude/reference labels and a measured arrival panel. P04 adds detector/track identity, goal uncertainty and target-loss reasons. P05 adds obstacle/clearance and blocked-route status. P06 adds localization source/quality. P07 adds separate link states and a reconnect flow. Fault injection controls must be clearly marked simulation-only.

For the ArduPilot path, the native C++ mission runtime remains authoritative when the UI disconnects. Browser rendering and model inference must not block the flight-control loop. Do not stream full-rate data into an unbounded UI event queue; display a bounded current view while preserving necessary run evidence locally.

For the ArduPilot path, external console/session tooling submits operator requests and displays firmware-reported mission state, active mode, input validity and achieved vehicle state. Our native C++ extension owns in-flight task progression, freshness checks and mission policy; upstream arming/override/failsafe authority is retained. Show local session/connection state separately and avoid a competing external mission state machine. The custom input/status contract remains to be qualified. The SkyDive backend continues to show its own screen/input capabilities.

## Visual and interaction direction

Use React/MUI controls, compact readable telemetry, clear typography, restrained color and consistent spacing. Prefer a neutral dark operational view with clear status accents; exact colors, dimensions and tokens remain subject to preview approval. Avoid decorative sci-fi HUD effects that obscure data.

Provide keyboard operation, visible focus, text labels, adequate contrast, status explanations beyond color, reduced motion and explicit loading/empty/error/disconnected states. Keep essential assets local for offline operation.

## Preview and approval gate

Before integrating UI, build an isolated working preview with the real React/MUI components and intended shared theme. Use minimal labeled fixture data and disconnected callbacks. Demonstrate selection, start/pending/run/stop, stale observations, target absence and failures. Present a working browser URL or open browser view, then wait for explicit approval of that shown scope.

Carry approved preview component code into the application. Material additions require an updated preview. Remove unused preview entry points, fixture copies, temporary captures and preview servers after integration. A static image, diagram or this requirements document does not satisfy UI approval.
