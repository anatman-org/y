#!/usr/bin/env python
"""
this is meant to be called as

  `python -my [arguments ...]`

and is a set of random tools
"""


import os
import sys

from cmd2 import Cmd

from .log import LOG

OBJECTS_DIR = os.getcwd() + "/o"


class yApp(Cmd):
    """command line utilities for y processing"""

    def __init__(self):
        super().__init__()
        self.prompt = ":> "

    def do_fmt(self, args):
        from .chinese import ChineseHouse, Hexagram
        from . import YSequence

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

        return 0

    def do_play(self, args):
        from y.chinese import ChineseHouse, Hexagram

        rooms = ChineseHouse.play()
        house = ChineseHouse(rooms)
        print(house.composition)

        return 0

    def do_commit(self, args):
        import subprocess
        from y.chinese import ChineseHouse

        house = ChineseHouse(ChineseHouse.play())
        composition = house.composition


        def check_modified():
            proc = subprocess.Popen(['git','status'],stdout=subprocess.PIPE)
            while True:
                line = proc.stdout.readline()
                if not line:
                  return False
                
                if line.startswith(b'\tmodified:   '):
                  return True

            return False

        if not check_modified():
            return 1

        house = ChineseHouse(ChineseHouse.play())
        composition = house.composition

        with open("play.log", "a") as play_log:
            play_log.write(composition + "\n")

        # subprocess.run(("git", "add", "-f", "play.log", "index.*"))

        subprocess.run(("git", "commit", "-a", "-q", "-m", composition))

        return 0

    def do_draw(self, args):
        from .draw import yDrawApp

        draw_app = yDrawApp()                                  
        sys.exit(draw_app.cmdloop())  

    def do_download(self, args):
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

            print(f"downloaded {target}")

        return 0


if __name__ == "__main__":

    app = yApp()

    if len(sys.argv) > 1:
        from shlex import join as shlex_join

        sys.exit(app.onecmd(shlex_join(sys.argv[1:])))

    else:
        sys.exit(app.cmdloop())
