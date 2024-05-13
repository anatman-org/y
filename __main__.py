#!/usr/bin/env python
"""
this is meant to be called as

  `python -my [arguments ...]`

and is a set of random tools
"""


import os
import sys
from .log import LOG

OBJECTS_DIR = os.getcwd() + "/o"


def _print():

    from fitz import fitz

    out = fitz.open("index.pdf")

    with open("play.log") as play_log:

        for p in reversed(play_log.readlines()):
            print(p.rstrip())


def _play():
    from y.chinese import ChineseHouse, Hexagram

    rooms = ChineseHouse.play()
    house = ChineseHouse(rooms)

    x_real = Hexagram(house.major.real)
    x_imag = Hexagram(house.major.imag)
    print(house.composition)


def _fmt():
    for line in sys.stdin.readlines():
        try:
            reading = line[:51]
            extra = line[51:]

            rooms = [YSequence(r) for r in reading.split()]
            house = ChineseHouse(rooms)

            x_real = Hexagram(house.major.real)
            x_imag = Hexagram(house.major.imag)
            print(
                house.composition,
                extra.rstrip(),
            )
        except:
            print(line.rstrip(), file=sys.stderr)


def _commit():
    import subprocess

    from y.chinese import ChineseHouse

    house = ChineseHouse(ChineseHouse.play())
    composition = house.composition

    with open("play.log", "a") as play_log:
        play_log.write(composition + "\n")

    subprocess.run(("git", "add", "-f", "play.log", "index.*"))

    subprocess.run(("git", "commit", "-q", "-m", composition))


def _download():
    import subprocess

    # import yt_dlp

    _YDL_OPTS = {
        "format": "mp4",
        "write-info-json": True,
        "write-sub": True,
        "sub-lang": "en",
    }

    for url in sys.argv[2:]:

        target_dir = OBJECTS_DIR

        if "youtube" in url or "youtu.be" in url:
            target_dir = target_dir + "/yt"

        target = target_dir + "/%(id)s.%(ext)s"

        LOG.info(f"download {url} to {target}")
        subprocess.run(
            (
                "yt-dlp",
                "-f",
                "mp4",
                "--write-info-json",
                "--write-sub",
                "--sub-lang",
                "en",
                "-o",
                target,
                url,
            )
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:

        match sys.argv[1]:

            case "print":
                _print()

            case "play":
                _play()

            case "commit":
                _commit()

            case "download":
                _download()

            case _:
                _fmt()

    else:
        _fmt()
