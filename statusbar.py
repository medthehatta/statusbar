#!/usr/bin/env python


import re
import datetime
import subprocess
from time import sleep


icon_dir = "/home/med/deploy/statusbar/icons"


def sh(cmd):
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
    return output.decode("utf-8").strip()


def format_output(outputs):
    sep = "  |  "
    left_pad = ""
    right_pad = "  "
    return left_pad + sep.join(outputs) + right_pad


def with_color(color):
    def _with_color(val):
        return f"^fg(color){val}^fg()"

    return _with_color


class Color:

    default = lambda x: x
    black = with_color("black")
    white = with_color("white")
    red = with_color("red")
    yellow = with_color("yellow")
    green = with_color("green")
    blue = with_color("blue")


def loop_process(*cmds, wait=10):
    counter = 0
    max_duration = 1 + sum(c.sleep for c in cmds)

    while True:
        outputs = [
            (c.run() if counter % c.sleep // wait == 0 else c.last) for c in cmds
        ]
        print(format_output(outputs), flush=True)
        sleep(wait)
        counter = (counter + 1) % max_duration


class ParsedCmd:

    cmd = ""
    sleep = 60
    icon = None
    last = ""

    @classmethod
    def i(cls):
        return f"^i({icon_dir}/{cls.icon}.xbm)"

    @classmethod
    def run_cmd(cls):
        return sh(cls.cmd)

    @classmethod
    def run(cls):
        result = cls.format(cls.run_cmd())
        cls.last = result
        return result

    @classmethod
    def format(cls, output):
        raise NotImplementedError


class DateCmd(ParsedCmd):

    cmd = "date +'%d %b (%a) %l:%M %p'"
    sleep = 10

    @classmethod
    def format(cls, output):
        return output


class PrayerCmd(ParsedCmd):

    cmd = "ipraytime --brief"
    sleep = 120
    icon = "clock"

    @classmethod
    def format(cls, output):
        prayers = ["Fajr", "Shorooq", "Zuhr", "Asr", "Maghrib", "Isha"]
        times = re.findall(r"((\d{1,2}):(\d{2}))", output)
        now = datetime.datetime.now()
        minutes_from_midnight = 60 * now.hour + now.minute
        prayer_minutes_from_midnight = [
            60 * int(t[1]) + int(t[2])
            for t in times
        ]
        prayer_minutes_until = [
            pmm - minutes_from_midnight for pmm in prayer_minutes_from_midnight
        ]
        prayer_times = zip(prayers, times, prayer_minutes_until)
        next_prayer = next(
            ((p, t, m) for (p, t, m) in prayer_times if m >= 0), None
        )

        if not next_prayer:
            return cls.i()

        (prayer, time, minutes_until) = next_prayer

        if minutes_until < 15:
            color = Color.red
        elif minutes_until < 45:
            color = Color.yellow
        elif minutes_until < 60:
            color = Color.blue
        else:
            color = Color.default

        return color(f"{cls.i()} {prayer} - {time[0]} ({minutes_until}m)")


def main():
    """Entry point."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", "--wait", type=int, default=10)
    parsed = parser.parse_args()
    loop_process(PrayerCmd, DateCmd, wait=parsed.interval)


if __name__ == "__main__":
    main()
