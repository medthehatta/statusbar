#!/bin/bash -e
prefix="$(dirname -- "$(readlink -f "$0")")"


_kill_if_pidfile () {
    local path="$1"
    local failmsg="$2"
    if [ -e "$path" ]; then
        kill "$(cat "$path")"
        rm "$path"
    else
        echo "$failmsg" >&2
        exit 1
    fi
}


if [ "$1" == "-l" ] || [ "$1" == "-f" ]; then
    _kill_if_pidfile \
        "$XDG_RUNTIME_DIR/wm/loop-statusbar.pid" \
        "Unable to kill loop, no statusbar watchdog running!"
else
    _kill_if_pidfile \
        "$XDG_RUNTIME_DIR/wm/statusbar.pid" \
        "Unable to kill statusbar, none seems to be running!"
fi
