# L15 native stop integration source walkthrough

This freezes the existing source sites that the proposed L15 integration will reuse. Firmware revision: `a00f32be2a91639c8dee1c41c09e1c5e5635d547`. The excerpts below preserve the source with trailing whitespace normalized. They describe the baseline, not an implemented L15 stop guard. The [L14 walkthrough](l14-stock-stop-source.md) covers rangefinder→proximity→AC_Avoid.

L15 proposes a native stop veto around the retained position goal: ask the stock limiter whether forward motion would be restricted, then enter stock BRAKE and report BLOCKED. Invalid/stale observations report FAILED and stop. Failed BRAKE entry or existing navigation/reference failures fall back to stock LAND. No detour or external mission state machine is proposed.


## Existing native goal setup

Source: [`ArduCopter/mode_featherlane.cpp:171`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/ArduCopter/mode_featherlane.cpp#L171), lines 171–230.

```cpp
    bool terrain_alt;
    if (!wp_nav->get_vector_NED_m(destination, destination_ned_m, terrain_alt) || terrain_alt) {
        return reject_start("conversion");
    }

#if AP_FENCE_ENABLED
    if (!copter.fence.check_destination_within_fence(destination)) {
        return reject_start("fence");
    }
#endif

    // initialise inherited controllers, then install the native owner's stored goal
    if (!ModeGuided::init(ignore_checks) || !set_destination(destination)) {
        copter.mode_guided.hold_position();
        return reject_start("destination");
    }

    // set_destination initialises speed defaults, so apply the retained limit afterwards
    ModeGuided::set_speed_NE_ms(task->speed_mps);
    _entry_home = current_home;
    Vector2f position_reset_m;
    float height_reset_m;
    _position_reset_ms = ahrs.getLastPosNorthEastReset(position_reset_m);
    _height_reset_ms = ahrs.getLastPosDownReset(height_reset_m);
    _executing = true;
    _consumed = true;
    _destination = destination;
    _arrival_radius_m = task->radius_m;
    _last_arrival_check_ms = AP_HAL::millis();
    set_task_state(TaskState::RUNNING, "start");

    GCS_SEND_TEXT(MAV_SEVERITY_INFO, "FL L10 goal=%ld,%ld alt_cm=%ld",
                  (long)destination.lat, (long)destination.lng, (long)destination.alt);
    GCS_SEND_TEXT(MAV_SEVERITY_INFO, "FL L10 speed=%.2fm/s task=%u", double(task->speed_mps), unsigned(_task_id));
    return true;
}

// the global goal is converted once; stop using it if the estimator reference resets
bool ModeFeatherLane::reference_valid()
{
    Location origin;
    if (!ahrs.get_origin(origin) || origin.lat != _entry_origin.lat || origin.lng != _entry_origin.lng ||
        fabsf(float(origin.alt) - float(_entry_origin.alt)) * CM_TO_METRES > MAX_REFERENCE_SHIFT_M) {
        return false;
    }

    const Location home = ahrs.get_home();
    if (home.get_distance(_entry_home) > MAX_REFERENCE_SHIFT_M ||
        fabsf(float(home.alt) - float(_entry_home.alt)) * CM_TO_METRES > MAX_REFERENCE_SHIFT_M) {
        return false;
    }

    Vector2f position_reset_m;
    float height_reset_m;
    return ahrs.getLastPosNorthEastReset(position_reset_m) == _position_reset_ms &&
           ahrs.getLastPosDownReset(height_reset_m) == _height_reset_ms;
}

// all bounds must remain satisfied across a continuous series of native updates
bool ModeFeatherLane::update_arrival()
```


## Existing native runtime and exit

Source: [`ArduCopter/mode_featherlane.cpp:282`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/ArduCopter/mode_featherlane.cpp#L282), lines 282–309.

```cpp
    }
    if (failure != nullptr) {
        _fallback_requested = true;
        if (_task_state == TaskState::COMPLETE) {
            // keep the completed task result; subsequent flight safety still has authority
            GCS_SEND_TEXT(MAV_SEVERITY_WARNING, "FL L11 guard r=%s", failure);
        } else {
            set_task_state(TaskState::FAILED, failure);
        }
        copter.set_mode_land_with_pause(ModeReason::FAILSAFE);
        return;
    }

    ModeGuided::run();
}

// do not alter shared controller state here: the next mode has already initialised
void ModeFeatherLane::exit()
{
    _executing = false;
    if (_task_state == TaskState::RUNNING || _task_state == TaskState::DWELLING) {
        set_task_state(_abort_requested ? TaskState::ABORTED : TaskState::INTERRUPTED,
                       _abort_requested ? "operator" : "mode_exit");
    }
    GCS_SEND_TEXT(MAV_SEVERITY_INFO, "FL L10 exit task=%u", unsigned(_task_id));
}

#endif // MODE_FEATHERLANE_ENABLED
```


## Existing range receive status and age API

Source: [`libraries/AP_RangeFinder/AP_RangeFinder_Backend.h:54`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AP_RangeFinder/AP_RangeFinder_Backend.h#L54), lines 54–84.

```cpp
    enum Rotation orientation() const { return (Rotation)params.orientation.get(); }
    float distance() const { return state.distance_m; }
    int8_t signal_quality_pct() const  WARN_IF_UNUSED { return state.signal_quality_pct; }
    uint16_t voltage_mv() const { return state.voltage_mv; }
    virtual float max_distance() const { return params.max_distance; }
    virtual float min_distance() const { return params.min_distance; }
    float ground_clearance() const { return params.ground_clearance; }
    MAV_DISTANCE_SENSOR get_mav_distance_sensor_type() const;
    RangeFinder::Status status() const;
    RangeFinder::Type type() const { return (RangeFinder::Type)params.type.get(); }

    // true if sensor is returning data
    bool has_data() const;

    // returns count of consecutive good readings
    // note that this method returning zero does not mean that the device is unhealthy:
    uint8_t range_valid_count() const { return state.range_valid_count; }

    // return a 3D vector defining the position offset of the sensor
    // in metres relative to the body frame origin
    const Vector3f &get_pos_offset() const { return params.pos_offset; }

    // return system time of last successful read from the sensor
    uint32_t last_reading_ms() const { return state.last_reading_ms; }

    // get temperature reading in C.  returns true on success and populates temp argument
    virtual bool get_temp(float &temp) const { return false; }

    // return the actual type of the rangefinder, as opposed to the
    // parameter value which may be changed at runtime.
    RangeFinder::Type allocated_type() const { return _backend_type; }
```


## Existing stock avoidance API

Source: [`libraries/AC_Avoidance/AC_Avoid.h:43`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AC_Avoidance/AC_Avoid.h#L43), lines 43–66.

```cpp

    // return true if any avoidance feature is enabled
    bool enabled() const { return _enabled != AC_AVOID_DISABLED; }

    // parameter conversion
    void convert_params();

    // Adjusts the desired velocity so that the vehicle can stop
    // before the fence/object.
    // kP, accel_cmss are for the horizontal axis
    // kP_z, accel_z_cmss are for vertical axis
    void adjust_velocity(Vector3f &desired_vel_neu_cms, bool &backing_up, float kP, float accel_cmss, float kP_z, float accel_z_cmss, float dt);
    void adjust_velocity(Vector3f &desired_vel_neu_cms, float kP, float accel_cmss, float kP_z, float accel_z_cmss, float dt) {
        bool backing_up = false;
        adjust_velocity(desired_vel_neu_cms, backing_up, kP, accel_cmss, kP_z, accel_z_cmss, dt);
    }
    void adjust_velocity_NED_m(Vector3f &desired_vel_ned_ms, float kP, float accel_mss, float kP_z, float accel_z_mss, float dt) {
        bool backing_up = false;
        Vector3f desired_vel_neu_cms{desired_vel_ned_ms.x * 100.0, desired_vel_ned_ms.y * 100.0, -desired_vel_ned_ms.z * 100.0};
        adjust_velocity(desired_vel_neu_cms, backing_up, kP, accel_mss * 100.0, kP_z, accel_z_mss * 100.0, dt);
        desired_vel_ned_ms = Vector3f{desired_vel_neu_cms.x, desired_vel_neu_cms.y, -desired_vel_neu_cms.z} * 0.01;
    }

    // This method limits velocity and calculates backaway velocity from various supported fences
```


## Existing stock BRAKE lifecycle

Source: [`ArduCopter/mode_brake.cpp:9`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/ArduCopter/mode_brake.cpp#L9), lines 9–86.

```cpp
// brake_init - initialise brake controller
bool ModeBrake::init(bool ignore_checks)
{
    // initialise pos controller speed and acceleration
    pos_control->NE_set_max_speed_accel_m(pos_control->get_vel_estimate_NED_ms().xy().length(), BRAKE_MODE_DECEL_RATE_MSS);
    pos_control->NE_set_correction_speed_accel_m(pos_control->get_vel_estimate_NED_ms().xy().length(), BRAKE_MODE_DECEL_RATE_MSS);

    // initialise position controller
    pos_control->NE_init_controller();

    // set vertical speed and acceleration limits
    pos_control->D_set_max_speed_accel_m(BRAKE_MODE_SPEED_Z_MS, BRAKE_MODE_SPEED_Z_MS, BRAKE_MODE_DECEL_RATE_MSS);
    pos_control->D_set_correction_speed_accel_m(BRAKE_MODE_SPEED_Z_MS, BRAKE_MODE_SPEED_Z_MS, BRAKE_MODE_DECEL_RATE_MSS);

    // initialise the vertical position controller
    if (!pos_control->D_is_active()) {
        pos_control->D_init_controller();
    }

    _timeout_ms = 0;

    return true;
}

// brake_run - runs the brake controller
// should be called at 100hz or more
void ModeBrake::run()
{
    // if not armed set throttle to zero and exit immediately
    if (is_disarmed_or_landed()) {
        make_safe_ground_handling();
        pos_control->D_relax_controller(0.0f);
        return;
    }

    // set motors to full range
    motors->set_desired_spool_state(AP_Motors::DesiredSpoolState::THROTTLE_UNLIMITED);

    // relax stop target if we might be landed
    if (copter.ap.land_complete_maybe) {
        pos_control->NE_soften_for_landing();
    }

    // use position controller to stop
    Vector2f vel_ne_zero;
    Vector2f accel_ne_zero;
    pos_control->input_vel_accel_NE_m(vel_ne_zero, accel_ne_zero);
    pos_control->NE_update_controller();

    // call attitude controller
    attitude_control->input_thrust_vector_rate_heading_rads(pos_control->get_thrust_vector(), 0.0f);

    pos_control->D_set_pos_target_from_climb_rate_ms(0.0f);
    pos_control->D_update_controller();

    // MAV_CMD_SOLO_BTN_PAUSE_CLICK (Solo only) is used to set the timeout.
    if (_timeout_ms != 0 && millis()-_timeout_start >= _timeout_ms) {
        if (!copter.set_mode(Mode::Number::LOITER, ModeReason::BRAKE_TIMEOUT)) {
            copter.set_mode(Mode::Number::ALT_HOLD, ModeReason::BRAKE_TIMEOUT);
        }
    }
}

/**
 * Set a timeout for the brake mode
 *
 * @param timeout_ms [in] timeout in milliseconds
 *
 * @note MAV_CMD_SOLO_BTN_PAUSE_CLICK (Solo only) is used to set the timeout.
 * If the timeout is reached, the mode will switch to loiter or alt hold depending on the current mode.
 * If timeout_ms is 0, the timeout is disabled.
 *
*/
void ModeBrake::timeout_to_loiter_ms(uint32_t timeout_ms)
{
    _timeout_start = millis();
    _timeout_ms = timeout_ms;
}
```

## L15 implemented native integration (local)

The following excerpt is frozen from firmware `77df25587413ab6d0183c6583c92b3cf4ba7bcab`, after the proposal above was shown and before the simulator comparison. It adds a stock-avoidance veto, observation freshness and explicit BRAKE handoff; the adjusted probe is never installed as a flight target. See [the L15 evidence](../evidence/l15-native-obstacle-stop/README.md) for actual observations and limits.

```cpp
// use the qualified stock limiter as a veto; it does not replace goal tracking
ModeFeatherLane::AvoidanceResult ModeFeatherLane::check_avoidance()
{
    _avoidance_failure = "avoidance_disabled";
#if AP_AVOIDANCE_ENABLED && HAL_PROXIMITY_ENABLED && AP_RANGEFINDER_ENABLED && \
    AP_PROXIMITY_RANGEFINDER_ENABLED && AP_RANGEFINDER_MAVLINK_ENABLED
    const AP_Proximity *proximity = AP::proximity();
    const auto *sensor = copter.rangefinder.get_backend(0);
    _avoidance_failure = "sensor_profile";
    if (sensor == nullptr || copter.rangefinder.num_sensors() != 1 ||
        sensor->allocated_type() != RangeFinder::Type::MAVLink ||
        sensor->type() != RangeFinder::Type::MAVLink || sensor->orientation() != ROTATION_NONE ||
        !is_equal(sensor->min_distance(), FRONT_RANGE_MIN_M) ||
        !is_equal(sensor->max_distance(), FRONT_RANGE_MAX_M) ||
        proximity == nullptr || proximity->num_sensors() != 1 ||
        proximity->get_type(0) != AP_Proximity::Type::RangeFinder ||
        !copter.avoid.proximity_avoidance_enabled() || !is_zero(copter.avoid.get_min_alt())) {
        return AvoidanceResult::INVALID;
    }

    // age the actual backend receive time, not the simulator's wire timestamp
    _avoidance_failure = "observation";
    const uint32_t last_reading_ms = sensor->last_reading_ms();
    const uint32_t age_ms = AP_HAL::millis() - last_reading_ms;
    if (last_reading_ms == 0 || age_ms > MAX_OBSERVATION_AGE_MS ||
        proximity->get_instance_status(0) != AP_Proximity::Status::Good ||
        (sensor->status() != RangeFinder::Status::Good &&
         sensor->status() != RangeFinder::Status::OutOfRangeHigh) || !isfinite(sensor->distance())) {
        GCS_SEND_TEXT(MAV_SEVERITY_WARNING, "FL L15 observation age_ms=%lu", (unsigned long)age_ms);
        return AvoidanceResult::INVALID;
    }

    // no-return remains unknown; only this prequalified narrow corridor is supported
    _avoidance_failure = "coverage";
    if (!isfinite(ahrs.get_roll_rad()) || !isfinite(ahrs.get_pitch_rad()) || !isfinite(ahrs.get_yaw_rad()) ||
        fabsf(ahrs.get_roll_rad()) > radians(MAX_SENSOR_TILT_DEG) ||
        fabsf(ahrs.get_pitch_rad()) > radians(MAX_SENSOR_TILT_DEG)) {
        return AvoidanceResult::INVALID;
    }

    Location current_location;
    _avoidance_failure = "measurement";
    if (!ahrs.get_location(current_location)) {
        return AvoidanceResult::INVALID;
    }
    const Vector2f goal_offset_ne_m = current_location.get_distance_NE(_destination);
    const float distance_m = goal_offset_ne_m.length();
    if (!isfinite(distance_m)) {
        return AvoidanceResult::INVALID;
    }
    if (distance_m <= MIN_GOAL_DIRECTION_DISTANCE_M) {
        return AvoidanceResult::CLEAR;
    }

    _avoidance_failure = "coverage";
    const Vector2f goal_offset_body_m = ahrs.earth_to_body2D(goal_offset_ne_m);
    if (fabsf(atan2f(goal_offset_body_m.y, goal_offset_body_m.x)) > radians(MAX_FRONT_PATH_ANGLE_DEG)) {
        return AvoidanceResult::INVALID;
    }

    const Vector3f requested_velocity_ned_ms{goal_offset_ne_m.x * _speed_limit_mps / distance_m,
                                           goal_offset_ne_m.y * _speed_limit_mps / distance_m, 0.0f};
    Vector3f limited_velocity_ned_ms = requested_velocity_ned_ms;
    copter.avoid.adjust_velocity_NED_m(limited_velocity_ned_ms,
                                     pos_control->NE_get_pos_p().kP(), pos_control->NE_get_max_accel_mss(),
                                     pos_control->D_get_pos_p().kP(), pos_control->D_get_max_accel_mss(), G_Dt);
    _avoidance_failure = nullptr;
    return (limited_velocity_ned_ms - requested_velocity_ned_ms).length() > MIN_AVOIDANCE_CHANGE_MPS ?
        AvoidanceResult::BLOCKED : AvoidanceResult::CLEAR;
#else
    return AvoidanceResult::INVALID;
#endif
}

// only successful stock mode entry records the requested blocked/failed result
void ModeFeatherLane::stop_task(TaskState state, const char *reason)
{
#if MODE_BRAKE_ENABLED
    _stop_state = state;
    _stop_reason = reason;
    _stop_requested = true;
    const bool changed_mode = copter.set_mode(Number::BRAKE, ModeReason::FAILSAFE);
    _stop_requested = false;
    if (changed_mode) {
        GCS_SEND_TEXT(MAV_SEVERITY_WARNING, "FL L15 handoff r=%s ms=%lu",
                      reason, (unsigned long)AP_HAL::millis());
        return;
    }
#endif
    fail_task("brake_entry");
}

void ModeFeatherLane::fail_task(const char *reason)
{
    _fallback_requested = true;
    if (_task_state == TaskState::COMPLETE) {
        // completed task state and subsequent flight safety remain separate
        GCS_SEND_TEXT(MAV_SEVERITY_WARNING, "FL L11 guard r=%s", reason);
    } else {
        set_task_state(TaskState::FAILED, reason);
    }
    copter.set_mode_land_with_pause(ModeReason::FAILSAFE);
}

void ModeFeatherLane::run()
{
    // latch a failed execution's fallback even if an estimator flag later recovers
    if (_fallback_requested) {
        copter.set_mode_land_with_pause(ModeReason::FAILSAFE);
        return;
    }

    if (!navigation_valid()) {
        fail_task("navigation");
        return;
    }
    if (!reference_valid()) {
        fail_task("reference");
        return;
    }

    const AvoidanceResult avoidance = check_avoidance();
    if (avoidance == AvoidanceResult::INVALID) {
        stop_task(TaskState::FAILED, _avoidance_failure);
        return;
    }
    if (avoidance == AvoidanceResult::BLOCKED) {
        stop_task(TaskState::BLOCKED, "obstacle");
        return;
    }
    if (_task_state != TaskState::COMPLETE &&
        AP_HAL::millis() - _execution_start_ms >= MAX_TASK_EXECUTION_MS) {
        stop_task(TaskState::FAILED, "timeout");
        return;
    }
    if (!update_arrival()) {
        fail_task("measurement");
        return;
    }

    ModeGuided::run();
}

// do not alter shared controller state here: the next mode has already initialised
void ModeFeatherLane::exit()
{
    _executing = false;
    if (_task_state == TaskState::RUNNING || _task_state == TaskState::DWELLING) {
        if (_stop_requested) {
            set_task_state(_stop_state, _stop_reason);
        } else {
            set_task_state(_abort_requested ? TaskState::ABORTED : TaskState::INTERRUPTED,
                           _abort_requested ? "operator" : "mode_exit");
        }
    }
    GCS_SEND_TEXT(MAV_SEVERITY_INFO, "FL L10 exit task=%u", unsigned(_task_id));
}

#endif // MODE_FEATHERLANE_ENABLED
```
