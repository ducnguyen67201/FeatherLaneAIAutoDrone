#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PHASE=${2:-l12}
case "$PHASE" in
    l12) PROFILE=l12-baseline ;;
    l13) PROFILE=l13-observation ;;
    l14) PROFILE=l14-stock-stop ;;
    l15) PROFILE=l15-native-stop ;;
    *) echo "Supported profiles: l12, l13, l14, l15" >&2; exit 2 ;;
esac
RUN_DIR=${1:-"$PROJECT_ROOT/.local/$PHASE/session"}
SITL_DIR="$RUN_DIR/sitl"
PYTHON="$PROJECT_ROOT/.local/l02/venv/bin/python"
VEHICLE_BINARY="$PROJECT_ROOT/.local/l08/stock-arducopter"
if [ "$PHASE" = l15 ]; then
    VEHICLE_BINARY="$PROJECT_ROOT/.local/l15/build/sitl/bin/arducopter"
fi
mkdir -p "$SITL_DIR"

# L12–L14 retain the preserved stock executable; L15 selects the native build.
# Give every manually operated case its own fresh scene-specific EEPROM.
# MAVProxy stays the operator console; no external mission state machine is added.
exec env -u DISPLAY SITL_RITW_TERMINAL=bash TMPDIR="$SITL_DIR/" \
    PATH="$PROJECT_ROOT/.local/l02/venv/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
    /usr/bin/script -q "$SITL_DIR/console.log" "$PYTHON" \
    "$PROJECT_ROOT/ardupilot/Tools/autotest/sim_vehicle.py" \
    -v ArduCopter -f gazebo-iris --model JSON -N --use-dir "$SITL_DIR" \
    --vehicle-binary "$VEHICLE_BINARY" \
    --add-param-file "$PROJECT_ROOT/simulation/gazebo/$PROFILE.parm" \
    --no-extra-ports --out 127.0.0.1:14550 \
    --mavproxy-args=--default-modules=log,param,mode,arm,rc,cmdlong,output
