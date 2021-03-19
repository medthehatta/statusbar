#!/bin/bash
prefix="$(dirname -- "$(readlink -f "$0")")"


_cleanup () { "$prefix/stop_statusbar.sh"; }
trap _cleanup EXIT


mkdir -p "$XDG_RUNTIME_DIR/wm"
echo "$$" > "$XDG_RUNTIME_DIR/wm/loop-statusbar.pid"


while true; do
    "$prefix/statusbar.sh"
    sleep 0.1
done
