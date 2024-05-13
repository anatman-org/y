""" house

'houses' are the different structured games
"""

import random
from functools import reduce

from . import ComplexGua, BaGua, Hexagram


class HouseException(Exception):
    """base exception for houses"""


class House:
    """foundation house class"""


class PythagoreanHouse(House):
    """pythagorean house
    squares of 3 + 4 + 5"""

    pile = None
    _score = None

    def __init__(self, seed=None):
        self._score = [None, [], [], [], None]

        if seed:
            if len(seed) != 50:
                raise HouseException("house must be seeded with 50 beads")
            self.pile = seed
        else:
            self.pile = (
                [ComplexGua(9)] * 9
                + [ComplexGua(8)] * 22
                + [ComplexGua(7)] * 16
                + [ComplexGua(6)] * 3
            )

    @property
    def score(self):
        return


class ChineseHouse(House):
    """chinese house
    this is the innovation of Knecht
    based on the I Ching"""

    pile = None
    _score = None

    def __init__(self, seed=None):
        self._score = [None, [], [], [], None]

        if seed:
            if len(seed) != 50:
                raise HouseException("house must be seeded with 50 beads")
            self.pile = seed
        else:
            self.pile = (
                [ComplexGua(9)] * 9
                + [ComplexGua(8)] * 22
                + [ComplexGua(7)] * 16
                + [ComplexGua(6)] * 3
            )

    @property
    def score(self):
        return len(self.pile) // 4, self._score

    @property
    def intent(self):
        return self._score.score[4]

    @property
    def source(self):
        return self._score[0]

    def draw_intent(self):
        self.pile = self.pile

        random.shuffle(self.pile)
        intent = self.pile.pop()
        self._score[4] = intent

    def split(self):
        length = len(self.pile)
        split = int(random.uniform(4, length - 4))

        left = self.pile[:split]
        right = self.pile[split:]

        return left, right

    def draw_wave(self):
        score = []

        left, right = self.split()
        random.shuffle(left)
        random.shuffle(right)

        # pop the wave starter
        if not self._score[0]:
            self._score[0] = right.pop()
        else:
            score += [right.pop()]

        left_remainder = len(left) % 4 or 4
        right_remainder = len(right) % 4 or 4

        left, score_left = left[:-left_remainder], left[-left_remainder:]
        right, score_right = right[:-right_remainder], right[-right_remainder:]

        self.pile = left + right

        score += score_left + score_right

        self._pile = left + right
        return score

    def play(self):
        self.draw_intent()

        self._score[1] = self.draw_wave()
        self._score[2] = self.draw_wave()
        self._score[3] = self.draw_wave()

        return self._score

    @staticmethod
    def score_trigram(score):
        trigram = [
            None,
        ] * 3

        for i in range(1, 4):
            line_score = reduce(lambda x, y: x * y, [ComplexGua(c) for c in score[i]])
            trigram[i - 1] = line_score
            # print(f"{i} {line_score.value} >>> {score[i]}")

        return str(BaGua(*trigram))

    @staticmethod
    def score_dot(score):
        dot_score = str(score[0])

        for i in range(1, 4):
            line = reduce(lambda a, b: a * b, [ComplexGua(c) for c in score[i]])

            if line.score == 6:
                dot_score = (
                    dot_score + " " * 4 * i + "".join([str(c) for c in score[i]])
                )
            else:
                dot_score = (
                    dot_score
                    + " " * (line.score - 6) * i
                    + "".join([str(c) for c in score[i]])
                )

        dot_score += " " * (49 - len(dot_score)) + str(score[4])

        return dot_score

    @staticmethod
    def score_hexagram(score):
        intent = score[0]
        resolve = score[4]

        def line_multiply(line):
            amplitude = len(line) // 4
            direction = reduce(lambda x, y: x * y, line)
            return direction

        hex_repr = ""
        gua = []
        for room in score[1:4]:
            line = line_multiply(room[0::4] + room[1::4])
            hex_repr = hex_repr + str(line) + "> " + str(room[0::4] + room[1::4]) + "\n"
            gua.append(line)

            line = line_multiply(room[2::4] + room[3::4])
            hex_repr = hex_repr + str(line) + "> " + str(room[2::4] + room[3::4]) + "\n"
            gua.append(line)

        hexagram = Hexagram(*gua)

        return f"{hexagram} == y{hexagram.yi} == w{hexagram.wen}"
