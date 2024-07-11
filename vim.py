import sys
from pathlib import Path
from datetime import datetime, timezone
from random import choice
from uuid import uuid4
from shlex import split as sh_split

import vim

sys.path.append(str(Path.cwd()))

from y import YSequence
from y.chinese import ChineseHouse, Hexagram

NOW = datetime.now


def insert_timestamp():
    row, col = vim.current.window.cursor
    current_line = vim.current.buffer[row - 1]
    new_line = (
        current_line[:col]
        + NOW(timezone.utc).astimezone().isoformat()
        + current_line[col:]
    )
    vim.current.buffer[row - 1] = new_line


def insert_uuid():
    row, col = vim.current.window.cursor
    current_line = vim.current.buffer[row - 1]
    new_line = current_line[:col] + str(uuid4()) + current_line[col:]
    vim.current.buffer[row - 1] = new_line


def parse_yi(start, end, raw_args=""):

    args = sh_split(raw_args)
    start = int(start) - 1
    end = int(end) - 1

    for n, line in [
        (i, line) if start <= i <= end else (False, False)
        for i, line in enumerate(vim.current.buffer)
    ]:
        if not n or not line:
            continue

        try:
            house = ChineseHouse([YSequence(x) for x in line[:50].split()])

            output = f"{house.composition}"

            if "-w" in args:
                w_real = Hexagram(house.major.real).wen
                w_imag = Hexagram(house.major.imag).wen
                output += f" w{w_real}>{w_imag} "

            if "-x" in args:
                x_real = Hexagram(house.major.real)
                x_imag = Hexagram(house.major.imag)
                output += f" {x_real}>{x_imag} "

            if "-y" in args:
                y_real = house.major.real
                y_imag = house.major.imag
                output += f" y{y_real:02o}>{y_imag:02o} "

            if not "-z" in args:
                output += f"{line[50:].rstrip()}"

            vim.current.buffer[n] = output

        except:
            vim.current.buffer[n] = line.rstrip()


def case_random(start, end):
    start = int(start) - 1
    end = int(end) - 1

    for n, line in [
        (i, line) if start <= i <= end else (False, False)
        for i, line in enumerate(vim.current.buffer)
    ]:
        if not n or not line:
            continue

        line = "".join([choice([a.lower(), a.upper()]) for a in line])
        vim.current.buffer[n] = line


def case_cloud(start, end):

    start = int(start) - 1
    end = int(end) - 1

    for n, line in [
        (i, line) if start <= i <= end else (False, False)
        for i, line in enumerate(vim.current.buffer)
    ]:

        if not n or not line:
            continue

        line = line[0:50].lower() + line[50:].upper()
        vim.current.buffer[n] = line


def grab(url, start, end):

    message_dialog(
        title="Example dialog window",
        text="Do you want to continue?\nPress ENTER to quit.",
    ).run()

    vim.current.line = f"{url} {start} {end}"
