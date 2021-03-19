#!/bin/bash -e
prefix="$(dirname -- "$(readlink -f "$0")")"

if [ "$1" == "-l" ] || [ "$1" == "-f" ]; then
    kill "$(cat "$XDG_RUNTIME_DIR/wm/loop-statusbar.pid")"
else
    kill "$(cat "$XDG_RUNTIME_DIR/wm/statusbar.pid")"
fi
