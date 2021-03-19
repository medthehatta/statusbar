#!/bin/bash -e
prefix="$(dirname -- "$(readlink -f "$0")")"


echo "$$" > "$XDG_RUNTIME_DIR/wm/statusbar.pid"


_cleanup () {
    kill "$(cat "$XDG_RUNTIME_DIR/wm/dlog.pid")"
    rm "$XDG_RUNTIME_DIR/wm/dlog.pid"
    kill "$(cat "$XDG_RUNTIME_DIR/wm/status.pid")"
    rm "$XDG_RUNTIME_DIR/wm/status.pid"
}


trap _cleanup EXIT


connected_screens="$(xrandr | grep -P '\bconnected\b' | wc -l)"


if [ "$connected_screens" == 1 ]; then
    dlog_pos="$(on_screen <<< 'screen0 50x0 top_left')"
    status_pos="$(on_screen <<< 'screen0 50x0 top_right')"
elif [ "$connected_screens" == 2 ]; then
    dlog_pos="$(on_screen <<< 'screen0 100x0 top_left')"
    status_pos="$(on_screen <<< 'screen1 100x0 top_right')"
else
    # Put it all on one screen; we don't know what's going on with this many
    # screens
    dlog_pos="$(on_screen <<< 'screen0 50x0 top_left')"
    status_pos="$(on_screen <<< 'screen0 50x0 top_right')"
fi


tail -f "$XDG_RUNTIME_DIR/wm/dynamiclog" | dzen2 -p -ta l -dock $dlog_pos &
echo "$!" > "$XDG_RUNTIME_DIR/wm/dlog.pid"

python3 "$prefix/statusbar.py" | dzen2 -p -ta r -dock $status_pos &
echo "$!" > "$XDG_RUNTIME_DIR/wm/status.pid"

wait
