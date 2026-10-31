# L04 — Trace the stock GUIDED takeoff request

[Project](../../../README.md) · [Learning card](../../phases/learning/l04-trace-one-command.md) · [Observed L03 flight](../l03-first-stock-flight/README.md)

Started locally on 2026-10-31 after the user confirmed understanding and requested pushing L03, then moving to the next phase. L03 was published and its remote SHA verified as `fd6ae48fec7530164ada79f2f255f272a0e5a325` on `codex/l03-first-stock-flight`; `main` stayed at `c45c9e19ae279011d5779fa2669df3fac0f21a29`. This walkthrough was prepared locally on `codex/l04-trace-one-command`, branched from that L03 commit. After its guided checkpoint, the user separately authorized committing/pushing L04 and starting L05.

**Status: complete.** Source inspection, annotations and the guided learner explanation checkpoint are finished. Firmware remains unchanged at `Copter-4.7.2`, `fb773567896014da007bca58358704d4a0d8516f`. P01 remains in progress. L05 has not started.

## Concept and prediction

The selected action is the already-observed `takeoff 3` in GUIDED. Before source inspection, the predicted chain was: receive the request, set the height target, compare it with estimated state, calculate thrust/orientation demands, then produce motor outputs. No simulator launch, arming, flight, rebuild, debugger, instrumentation or parameter change was needed to inspect this path.

A mission is a sequence of tasks. A mode selects the active flight behavior. Navigation/reference generation supplies a desired movement. Estimation supplies the best available current state. Feedback controllers compare desired versus estimated state and calculate demands; the motor mixer distributes the demands among motors. L03 used a direct GUIDED takeoff request, not an uploaded AUTO mission or our proposed native mission extension.

## The chain in ordinary language

```text
Operator asks for takeoff to 3 metres in MAVProxy
    ↓ MAVLink takeoff command, altitude parameter = 3
ArduPilot decodes the request and checks the active mode/state
    ↓ if admitted, initializes GUIDED takeoff and returns acceptance
Repeated scheduled GUIDED takeoff control
    ↓ desired height and near-zero horizontal movement
Position controller compares desired state with estimated state
    ↓ required thrust and thrust direction
Attitude/rate controllers maintain orientation and rotation rates
    ↓ throttle plus roll/pitch/yaw demands
Motor mixer calculates each motor's share
    ↓ output-channel values
SITL output backend supplies them to the built-in physics model
    ↓ simulated movement and sensor feedback support the next updates
```

This is a responsibility/data-flow drawing, not a single synchronous call stack. The command handler returns after admitting the target. The scheduler subsequently refreshes estimates and runs control/output work repeatedly. No new architecture or UI approval is proposed by this walkthrough.

## Source-linked walkthrough

### 1. Console request

The installed MAVProxy 1.8.75 `mavproxy_cmdlong.py::cmd_takeoff` parses `3` as a float and sends `MAV_CMD_NAV_TAKEOFF` (22) using COMMAND_LONG with altitude in parameter 7. The installed source was inspected; MAVProxy is external console tooling, not firmware. See the L03 console/onboard command records.

### 2. Decode and acknowledge

The receiver decodes COMMAND_LONG, converts it through `try_command_long_as_command_int`, dispatches it and sends COMMAND_ACK with the returned result. That ACK does not wait for measured arrival. [COMMAND_LONG receiver](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/GCS_MAVLink/GCS_Common.cpp#L5391).

### 3. Admit takeoff

The Copter handler requires the relative-altitude frame and passes `packet.z` in metres to the active mode. Failed admission returns FAILED; valid handoff returns ACCEPTED. The build supplies the relative-altitude frame when converting the console command. [Copter takeoff handler](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/GCS_MAVLink_Copter.cpp#L611).

### 4. Check current state

`do_user_takeoff_U_m` requires armed motors, a landed state, a mode supporting user takeoff, a target above the current altitude and an enabled motor interlock when applicable. It invokes the mode-specific start method and then sets auto-armed. These checks are separate from the earlier normal arming checks. [Shared mode admission checks](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/takeoff.cpp#L18).

### 5. Set the destination

GUIDED interprets the requested height as above home on the normal branch and converts it to altitude above the estimator origin. It selects the TakeOff submode, holds heading, initializes the vertical controller and starts `_AutoTakeoff`. The alternative qualified-rangefinder branch exists in source; this walkthrough does not claim L03 used it. [GUIDED target initialization](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/mode_guided.cpp#L160).

### 6. Run the selected behavior

`ModeGuided::run` selects its TakeOff submode; `takeoff_run` calls `_AutoTakeoff::run`. The latter handles spool-up and the on-ground throttle ramp, then supplies the desired vertical position with zero desired vertical velocity, updates the vertical/horizontal controllers and passes thrust direction/heading to attitude control. [Repeated stock takeoff behavior](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/takeoff.cpp#L115).

### 7. Compare height and motion

`D_update_controller` calculates position error into a velocity target, velocity error into acceleration demand and acceleration error into thrust/throttle demand. It calls `set_throttle_out`. These are feedback calculations using estimated state, not a fixed throttle selected by MAVProxy. [Vertical position/velocity/acceleration controller](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_AttitudeControl/AC_PosControl.cpp#L1072).

### 8. Maintain orientation

`input_thrust_vector_heading` converts the requested thrust direction/heading into the attitude-controller path. The rate controller uses measured gyro rates to calculate roll, pitch and yaw demands. `set_throttle_out` passes the collective throttle demand to the motors interface with the configured angle compensation. [Multicopter rate controller](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_AttitudeControl/AC_AttitudeControl_Multi.cpp#L441).

### 9. Calculate individual motors

`AP_MotorsMulticopter::output` runs spool logic, calls the matrix mixer and converts outputs for the channels. `AP_MotorsMatrix::output_armed_stabilizing` mixes collective throttle with roll/pitch/yaw demands and motor factors; `output_to_motors` converts enabled actuator values to PWM-form output values. This is the individual-motor calculation, not the original command receiver. [Matrix motor mixing](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AP_Motors/AP_MotorsMatrix.cpp#L213).

### 10. Apply simulated outputs

`rc_write` routes motor output through SRV channels to the SITL RCOutput backend. The backend stores output values (or pending values until push). SITL_State copies PWM outputs into simulator input and calls the vehicle model. MultiCopter calculates forces and updates dynamics/position. No physical motor was connected. [Built-in multicopter physics](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/SITL/SIM_Multicopter.cpp#L59).

## Where current state comes from

[`Copter::read_AHRS`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/Copter.cpp#L883) calls the estimator interface update. [`Copter::read_inertia`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/inertia.cpp#L4) refreshes the position controller’s estimates; [`AC_PosControl::update_estimates`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/libraries/AC_AttitudeControl/AC_PosControl.cpp#L1439) obtains position/velocity through the AHRS interface. L03 reported EKF3 using simulated GPS. This step supplies current state; it does not choose the requested 3 m destination or mix motor outputs. The full estimator and sensor algorithms are outside this one-command walkthrough.

For this simple vertical takeoff, the inspected normal path directly uses the position controllers in `_AutoTakeoff`. AC_WPNav appears for configuration/terrain helpers, but the source does not justify drawing a waypoint-route update as the main takeoff controller. No coordinate route or obstacle planning was performed.

AHRS is an internal ArduPilot software interface to estimation; it is not itself a physical sensor. In `read_inertia()`, `ahrs.get_location` supplies location to copy into `current_loc.lat/lng`. `get_relative_position_D_origin_float` supplies down-positive position relative to the estimator origin; negating it gives altitude above that origin, then the code converts to the home reference when available. The function reads/copies estimated state rather than implementing sensor fusion itself. In SITL the sensor observations are simulated. Estimation, feedback control and motor mixing all remain inside the native autopilot program.

## Timing and the retained flight

[The scheduler task table](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/Copter.cpp#L113) schedules rate control, motor output, estimator/inertial updates and flight-mode work. [`update_flight_mode`](https://github.com/ArduPilot/ardupilot/blob/fb773567896014da007bca58358704d4a0d8516f/ArduCopter/mode.cpp#L497) dispatches the active mode. These tasks exchange state across repeated iterations; the conceptual arrows above do not imply they all execute immediately within the command receiver or in diagram order in one tick. The L03 saved profile has `SCHED_LOOP_RATE=400` and `FSTRATE_ENABLE=0`; these are configuration observations, not measured deadline, latency or achieved-rate guarantees.

The existing [L03 event record](../l03-first-stock-flight/command-state-events.json), [onboard log summary](../l03-first-stock-flight/onboard-log-summary.json) and [trajectory](../l03-first-stock-flight/trajectory.csv) ground the explanation:

| L03 reception time after first vehicle message | Observation | Connection to source responsibilities |
| --- | --- | --- |
| 62.122 s | Takeoff accepted; onboard command is 22, relative-altitude frame 3, altitude 3 m | Request admitted and takeoff target initialized; not arrival. |
| 63.345 / 66.347 s | TAKEOFF / IN_AIR state and recorded climb | Behavior continued after the handler returned. No instruction-level runtime trace is claimed. |
| 85.054–90.054 s | Declared hold samples at 2.999 m with reported vertical speed 0.00 m/s | Measured outcome supports the held-height result; it is not inferred from the ACK. |
| 93.830 s onward | Separate LAND request, descent, ON_GROUND and automatic disarm | This was a later command; takeoff completion itself did not command landing. LAND internals are outside L04. |

## Evidence, limits and rollback

[Source manifest](source-manifest.json) records each selected source path, actual symbol line, full-file SHA-256 and immutable upstream permalink for the pinned revision. Installed MAVProxy source is supplied by the [L02 dependency lock](../l02-basic-sitl-setup/requirements.lock.txt), and its takeoff command was already inspected for L03. [Execution summary](execution-summary.json) records final checks and scope.

This is static source inspection correlated with previously retained run evidence. No new runtime function trace, independent flight verification, measured scheduling/latency, code coverage or physical behavior is claimed. No software dependencies, tests, snapshots or test scaffolding were added. There was no simulator process, debugger pause or logging instrumentation to affect flight timing during L04. The source remains unchanged, including all recursive submodule pins.

Rollback requires no firmware/debug changes to remove. The unchanged L03 baseline remains available at its published commit; L04 documents can be revised locally without disturbing that baseline. No upstream update or firmware/remote resource change was made. P01 remains in progress; L05 has not started.

## Guided learner checkpoint

Completed through discussion in this chat on 2026-10-31: **Which part provides our estimate of the current height, and which part calculates the individual motor outputs?** The requested destination is supplied by `takeoff 3` and admitted by GUIDED. Current state is supplied through the estimator; individual motor demand is calculated by the motor mixer after the controllers compute the needed motion/thrust. The learner initially attributed estimation to the controller/MAVProxy, then located `Copter::read_inertia()`, the AHRS location/height reads and the motor-matrix output path. Follow-up clarified that AHRS is an internal estimator interface, not an outside sensor: sensor observations feed the estimator, its estimates feed the controllers, and motor mixing converts controller demands to individual outputs. Both estimation and control run inside native ArduPilot C++ code; the sensor measurements are inputs. This records guided understanding with clarification, not an independent examination or runtime verification.

## Publication authorization

On 2026-10-31 the user said: “let’s push this to the branch and start LO5.” This authorizes committing/pushing the completed L04 documents, source manifest and learning-progress diagram/source on `codex/l04-trace-one-command`, then starting the scoped L05 coordinate flight on a new local branch. No merge/update of `main` or L05 publication is included. Frozen Python dependencies were audited before commit; raw audit output and the actual publication/remote-SHA verification receipt remain under `.local/l04/`. Local tooling, dependencies, generated HTML and temporary receipts remain ignored.
