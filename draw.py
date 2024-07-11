#!/usr/bin/env python
"""
"""
import os
from cmd2 import Cmd

from .log import LOG

OBJECTS_DIR = os.getcwd() + "/o"


class yDrawApp(Cmd):
    """command line utilities for y processing"""

    def __init__(self):
        super().__init__()
        self.prompt = ":% "

    def do_draw(self, args):
        print(args)


if __name__ == "__main__":

    draw_app = yDrawApp()

    if len(sys.argv) > 1:
        from shlex import join as shlex_join

        sys.exit(draw_app.onecmd(shlex_join(sys.argv[1:])))

    else:
        sys.exit(draw_app.cmdloop())
