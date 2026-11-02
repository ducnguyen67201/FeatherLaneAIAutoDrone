# L14 stock stopping source walkthrough

This is a read-only source trace for the proposed L14 configuration, not execution evidence. Firmware revision: `a00f32be2a91639c8dee1c41c09e1c5e5635d547`; stock source base: `fb773567896014da007bca58358704d4a0d8516f`. No firmware is changed. The excerpts below are copied from that pinned checkout with trailing whitespace normalized.

The proposed data path is external sensor observation → existing rangefinder → existing proximity boundary → stock velocity limiter used by LOITER. The operator supplies forward input through MAVProxy. Full aircraft/controller/physics ownership remains in the [core architecture](../architecture/README.md).


## Rangefinder receives the measurement

Source: [`libraries/AP_RangeFinder/AP_RangeFinder_MAVLink.cpp:31`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AP_RangeFinder/AP_RangeFinder_MAVLink.cpp#L31), lines31–53.

```cpp
    if (packet.orientation == orientation()) {
        state.last_reading_ms = AP_HAL::millis();
        distance = packet.current_distance * 0.01;
        _max_distance = packet.max_distance * 0.01;
        _min_distance = packet.min_distance * 0.01;
        sensor_type = (MAV_DISTANCE_SENSOR)packet.type;
        signal_quality = packet.signal_quality;
        if (signal_quality == 0) {
            // MAVLink's 0 means invalid/unset, so we map it to -1
            signal_quality = RangeFinder::SIGNAL_QUALITY_UNKNOWN;
        } else if (signal_quality == 1) {
            // Map 1 to 0 as that is what ardupilot uses as the worst signal quality
            signal_quality = RangeFinder::SIGNAL_QUALITY_MIN;
        }
    }
}

float AP_RangeFinder_MAVLink::max_distance() const
{
    const auto baseclass_max_distance = AP_RangeFinder_Backend::max_distance();

    if (is_zero(_max_distance) && is_zero(_min_distance)) {
        // we assume if both of these are zero that we ignore both
```


## Rangefinder feeds a proximity boundary

Source: [`libraries/AP_Proximity/AP_Proximity_RangeFinder.cpp:29`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AP_Proximity/AP_Proximity_RangeFinder.cpp#L29), lines29–64.

```cpp
void AP_Proximity_RangeFinder::update(void)
{
    // exit immediately if no rangefinder object
    const RangeFinder *rngfnd = AP::rangefinder();
    if (rngfnd == nullptr) {
        set_status(AP_Proximity::Status::NoData);
        return;
    }

    uint32_t now = AP_HAL::millis();

    // look through all rangefinders
    for (uint8_t i=0; i < rngfnd->num_sensors(); i++) {
        AP_RangeFinder_Backend *sensor = rngfnd->get_backend(i);
        if (sensor == nullptr) {
            continue;
        }
        if (sensor->has_data()) {
            // check for horizontal range finders
            if (sensor->orientation() <= ROTATION_YAW_315) {
                const uint8_t sector = (uint8_t)sensor->orientation();
                const float angle = sector * 45;
                const AP_Proximity_Boundary_3D::Face face = frontend.boundary.get_face(angle);
                // distance in meters
                const float distance = sensor->distance();
                _distance_min = sensor->min_distance();
                _distance_max = sensor->max_distance();
                if ((distance <= _distance_max) && (distance >= _distance_min) && !ignore_reading(angle, distance, false)) {
                    frontend.boundary.set_face_attributes(face, angle, distance, state.instance);
                    // update OA database
                    database_push(angle, distance);
                } else {
                    frontend.boundary.reset_face(face, state.instance);
                }
                _last_update_ms = now;
            }
```


## Proximity adjusts desired velocity

Source: [`libraries/AC_Avoidance/AC_Avoid.cpp:1233`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AC_Avoidance/AC_Avoid.cpp#L1233), lines1233–1299.

```cpp
void AC_Avoid::adjust_velocity_proximity(float kP, float accel_cmss, Vector3f &desired_vel_neu_cms, Vector3f &backup_vel_neu_cms, float kP_z, float accel_u_cmss, float dt)
{
#if HAL_PROXIMITY_ENABLED
    // exit immediately if proximity sensor is not present
    AP_Proximity *proximity = AP::proximity();
    if (!proximity) {
        return;
    }

    AP_Proximity &_proximity = *proximity;
    // get total number of obstacles
    const uint8_t obstacle_num = _proximity.get_obstacle_count();
    if (obstacle_num == 0) {
        // no obstacles
        return;
    }

    const AP_AHRS &_ahrs = AP::ahrs();

    // for backing away
    Vector2f quad_1_back_vel_ne_cms, quad_2_back_vel_ne_cms, quad_3_back_vel_ne_cms, quad_4_back_vel_ne_cms;
    float max_back_vel_u_cms = 0.0f;
    float min_back_vel_u_cms = 0.0f;

    // rotate velocity vector from earth frame to body-frame since obstacles are in body-frame
    const Vector2f desired_vel_body_ne_cms = _ahrs.earth_to_body2D(Vector2f{desired_vel_neu_cms.x, desired_vel_neu_cms.y});

    // safe_vel_ne_cms will be adjusted to stay away from Proximity Obstacles
    Vector3f safe_vel_neu_cms = Vector3f{desired_vel_body_ne_cms.x, desired_vel_body_ne_cms.y, desired_vel_neu_cms.z};
    const Vector3f safe_vel_orig_neu_cms = safe_vel_neu_cms;

    // calc margin in cm
    const float margin_cm = MAX(_margin_m * 100.0f, 0.0f);
    Vector3f stopping_point_plus_margin_neu_cm;
    if (!desired_vel_neu_cms.is_zero()) {
        // only used for "stop mode". Pre-calculating the stopping point here makes sure we do not need to repeat the calculations under iterations.
        const float speed_cms = safe_vel_neu_cms.length();
        stopping_point_plus_margin_neu_cm = safe_vel_neu_cms * ((2.0f + margin_cm + get_stopping_distance(kP, accel_cmss, speed_cms)) / speed_cms);
    }

    for (uint8_t i = 0; i<obstacle_num; i++) {
        // get obstacle from proximity library
        Vector3f vector_to_obstacle_neu;
        if (!_proximity.get_obstacle(i, vector_to_obstacle_neu)) {
            // this one is not valid
            continue;
        }

        const float dist_to_boundary_cm = vector_to_obstacle_neu.length();
        if (is_zero(dist_to_boundary_cm)) {
            continue;
        }

        // back away if vehicle has breached margin
        if (is_negative(dist_to_boundary_cm - margin_cm)) {
            const float breach_dist_cm = margin_cm - dist_to_boundary_cm;
            // add a deadzone so that the vehicle doesn't backup and go forward again and again
            const float deadzone_cm = MAX(0.0f, _backup_deadzone_m) * 100.0f;
            if (breach_dist_cm > deadzone_cm) {
                // this vector will help us decide how much we have to back away horizontally and vertically
                const Vector3f margin_vector_neu_cm = vector_to_obstacle_neu.normalized() * breach_dist_cm;
                const float xy_back_dist = margin_vector_neu_cm.xy().length();
                const float z_back_dist = margin_vector_neu_cm.z;
                calc_backup_velocity_3D(kP, accel_cmss, quad_1_back_vel_ne_cms, quad_2_back_vel_ne_cms, quad_3_back_vel_ne_cms, quad_4_back_vel_ne_cms, xy_back_dist, vector_to_obstacle_neu, kP_z, accel_u_cmss, z_back_dist, min_back_vel_u_cms, max_back_vel_u_cms, dt);
            }
        }

```


## LOITER applies the stock limiter

Source: [`libraries/AC_WPNav/AC_Loiter.cpp:379`](https://github.com/ducnguyen67201/FeatherLaneArduPilot/blob/a00f32be2a91639c8dee1c41c09e1c5e5635d547/libraries/AC_WPNav/AC_Loiter.cpp#L379), lines379–397.

```cpp
#if AP_AVOIDANCE_ENABLED && !APM_BUILD_TYPE(APM_BUILD_ArduPlane)
    if (avoidance_on) {
        // Apply fence/obstacle avoidance adjustments (velocity only)
        // TODO: We need to also limit the _desired_accel_ne_mss
        AC_Avoid *_avoid = AP::ac_avoid();
        if (_avoid != nullptr) {
            Vector3f avoidance_vel_ned_cms{desired_vel_ne_ms.x * 100.0, desired_vel_ne_ms.y * 100.0, 0.0f};
            _avoid->adjust_velocity(avoidance_vel_ned_cms, _pos_control.NE_get_pos_p().kP(), _accel_max_ne_mss * 100.0, _pos_control.D_get_pos_p().kP(), _pos_control.D_get_max_accel_mss() * 100.0, dt_s);
            desired_vel_ne_ms = avoidance_vel_ned_cms.xy() * 0.01;
        }
    }
#endif // !APM_BUILD_ArduPlane

    // Retrieve current desired position
    Vector2p desired_pos_ned_m = _pos_control.get_pos_desired_NED_m().xy();

    // Integrate velocity to update desired position
    desired_pos_ned_m += (desired_vel_ne_ms * dt_s).topostype();

```


The proposed L14 profile selects PRX1_TYPE4 (rangefinder), AVOID_ENABLE2 (proximity), AVOID_BEHAVE1 (Stop), AVOID_MARGIN2m, backup speed0 and LOIT_SPEED_MS0.5. No-return is not clearance; the front fan and simulator body/collision limits remain. These settings and the clear/blocked result must be observed before the phase is called qualified.
