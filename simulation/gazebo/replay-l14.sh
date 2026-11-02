#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ACTION=${1:-}
CASE=${2:-blocked}
case "$CASE" in
    clear|blocked) ;;
    *) echo "Recorded cases: clear, blocked" >&2; exit 2 ;;
esac
PREFIX="$PROJECT_ROOT/.local/l12/gazebo-env"
MICROMAMBA="$PROJECT_ROOT/.local/l12/micromamba/bin/micromamba"
RECORD_DIR="$PROJECT_ROOT/.local/l14/$CASE-final/gazebo-record"
export MAMBA_ROOT_PREFIX="$PROJECT_ROOT/.local/l12/mamba-root"
export GZ_PARTITION=featherlane_l14_playback
export GZ_IP=127.0.0.1
export GZ_SIM_SYSTEM_PLUGIN_PATH="$PROJECT_ROOT/.local/l12/plugin-build:$PREFIX/lib/gz-sim-8/plugins"
export GZ_SIM_RESOURCE_PATH="$PROJECT_ROOT/.local/l12/src/ardupilot_gazebo/models:$PROJECT_ROOT/simulation/gazebo/worlds"

# macOS requires separate server and GUI terminals. Playback starts paused;
# no autopilot, observation adapter or flight commands are involved.
case "$ACTION" in
    server)
        test -f "$RECORD_DIR/state.tlog"
        exec "$MICROMAMBA" --no-rc run -p "$PREFIX" gz sim -s -v 4 --playback "$RECORD_DIR"
        ;;
    gui)
        GUI_CONFIG="$PROJECT_ROOT/.local/l14/playback-$CASE-gui.config"
        mkdir -p "$PROJECT_ROOT/.local/l14"
        sed "s/L14 — actual/L14 $CASE — actual/" \
            "$PROJECT_ROOT/simulation/gazebo/l14-playback-gui.config" > "$GUI_CONFIG"
        exec "$MICROMAMBA" --no-rc run -p "$PREFIX" gz sim -g -v 4 \
            --gui-config "$GUI_CONFIG"
        ;;
    cue) REQUEST='pause: true seek {sec: 55 nsec: 0}' ;;
    play) REQUEST='pause: false' ;;
    pause) REQUEST='pause: true' ;;
    *) echo "Usage: replay-l14.sh server|gui|cue|play|pause [clear|blocked]" >&2; exit 2 ;;
esac
exec "$MICROMAMBA" --no-rc run -p "$PREFIX" gz service \
    -s /world/default/playback/control --reqtype gz.msgs.LogPlaybackControl \
    --reptype gz.msgs.Boolean --timeout 3000 --req "$REQUEST"
