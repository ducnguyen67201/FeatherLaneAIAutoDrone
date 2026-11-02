#!/bin/zsh
set -eu
PROJECT_ROOT=/Users/ducng/Desktop/workspace/FeatherLaneAIAutoDrone
RUN_DIR="$PROJECT_ROOT/.local/l11/nominal"
exec env -u DISPLAY SITL_RITW_TERMINAL=bash TMPDIR="$RUN_DIR/"  PATH="$PROJECT_ROOT/.local/l02/venv/bin:/usr/bin:/bin:/usr/sbin:/sbin"  /usr/bin/script -q "$RUN_DIR/console.log"  "$PROJECT_ROOT/.local/l02/venv/bin/python"  "$PROJECT_ROOT/ardupilot/Tools/autotest/sim_vehicle.py"  -v ArduCopter -f quad -N --use-dir "$RUN_DIR"  --vehicle-binary "/Users/ducng/Desktop/workspace/FeatherLaneAIAutoDrone/.local/l11/build/sitl/bin/arducopter"  --no-extra-ports --out 127.0.0.1:14550  --mavproxy-args=--default-modules=log,param,mode,arm,rc,cmdlong,output
