#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PHASE=${2:-l12}
case "$PHASE" in
    l12) WORLD=l12-baseline ;;
    l13) WORLD=l13-observation ;;
    l14) WORLD=l14-stock-stop ;;
    *) echo "Supported scenes: l12, l13, l14" >&2; exit 2 ;;
esac
RUN_DIR=${1:-"$PROJECT_ROOT/.local/$PHASE/session"}
GZ_PREFIX="$PROJECT_ROOT/.local/l12/gazebo-env"
PLUGIN_SOURCE="$PROJECT_ROOT/.local/l12/src/ardupilot_gazebo"
MICROMAMBA="$PROJECT_ROOT/.local/l12/micromamba/bin/micromamba"
mkdir -p "$RUN_DIR"

# Scope discovery, plugins and resources to this local simulator session.
export MAMBA_ROOT_PREFIX="$PROJECT_ROOT/.local/l12/mamba-root"
export GZ_PARTITION="featherlane_$PHASE"
export GZ_IP=127.0.0.1
export GZ_SIM_SYSTEM_PLUGIN_PATH="$PROJECT_ROOT/.local/l12/plugin-build:$GZ_PREFIX/lib/gz-sim-8/plugins"
export GZ_SIM_RESOURCE_PATH="$PLUGIN_SOURCE/models:$PROJECT_ROOT/simulation/gazebo/worlds"
exec "$MICROMAMBA" --no-rc run -p "$GZ_PREFIX" gz sim -s -r -v 4 \
    --record-path "$RUN_DIR/gazebo-record" \
    "$PROJECT_ROOT/simulation/gazebo/worlds/$WORLD.sdf"
