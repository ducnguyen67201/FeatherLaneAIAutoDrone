#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PHASE=${2:-l12}
case "$PHASE" in
    l12) PROFILE=l12-baseline ;;
    l13) PROFILE=l13-observation ;;
    *) echo "Supported profiles: l12, l13" >&2; exit 2 ;;
esac
RUN_DIR=${1:-"$PROJECT_ROOT/.local/$PHASE/session"}
SITL_DIR="$RUN_DIR/sitl"
PYTHON="$PROJECT_ROOT/.local/l02/venv/bin/python"
STOCK_BINARY="$PROJECT_ROOT/.local/l08/stock-arducopter"
mkdir -p "$SITL_DIR"

# Use the exact preserved stock executable with a fresh scene-specific EEPROM.
# MAVProxy stays the operator console; no external mission state machine is added.
exec env -u DISPLAY SITL_RITW_TERMINAL=bash TMPDIR="$SITL_DIR/" \
    PATH="$PROJECT_ROOT/.local/l02/venv/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
    /usr/bin/script -q "$SITL_DIR/console.log" "$PYTHON" \
    "$PROJECT_ROOT/ardupilot/Tools/autotest/sim_vehicle.py" \
    -v ArduCopter -f gazebo-iris --model JSON -N --use-dir "$SITL_DIR" \
    --vehicle-binary "$STOCK_BINARY" \
    --add-param-file "$PROJECT_ROOT/simulation/gazebo/$PROFILE.parm" \
    --no-extra-ports --out 127.0.0.1:14550 \
    --mavproxy-args=--default-modules=log,param,mode,arm,rc,cmdlong,output
