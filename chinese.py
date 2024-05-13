""" Chinese House rules

this is based on the original rules conceived
by Magister Ludi Knecht who based them heavily
on the I Ching.
"""

from typing import Any, Tuple, List
from random import shuffle, uniform


from . import YSequence, YHouse, Yin, Yang, OldYin, OldYang


class Trigram(YSequence):
    """Trigram sequence"""

    # two key indexes, first by value then unicode
    _U = "☰☱☲☳☴☵☶☷"
    _V = "0123456789abcdefghijklmnopqrstuvwxyz%ABCDEFGHIJKLMNOPQRSTUVWXYZ="
    _Y = "☷☳☵☱☶☲☴☰"

    _SEQUENCE_MAP = {
        "y": _Y,  # standard Yi sequence
        "fuxi": "☰☴☵☶☷☳☲☱",  # the Fuxi sequence
        "wen": "☲☷☱☰☵☶☳☴",  # the tradional Wen sequence
        "desig": "☷☳☵☴☰☶☲☱",  # the Designori-Campbell sequence
    }


class Hexagram(YSequence):
    """yijing hexagram"""

    # two key indexes, first by value then unicode
    _Y = "䷁䷗䷆䷒䷎䷣䷭䷊䷏䷲䷧䷵䷽䷶䷟䷡䷇䷂䷜䷻䷦䷾䷯䷄䷬䷐䷮䷹䷞䷰䷛䷪䷖䷚䷃䷨䷳䷕䷑䷙䷢䷔䷿䷥䷷䷝䷱䷍䷓䷩䷺䷼䷴䷤䷸䷈䷋䷘䷅䷉䷠䷌䷫䷀"
    _U = "䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿"

    _seq = {
        "y": _Y,
        "wen": _U,
        "fuxi": "䷀䷪䷍䷡䷈䷄䷙䷊䷉䷹䷥䷵䷼䷻䷨䷒䷌䷰䷝䷶䷤䷾䷕䷣䷘䷐䷔䷲䷩䷂䷚䷗䷫䷛䷱䷟䷸䷯䷑䷭䷅䷮䷿䷧䷺䷜䷃䷆䷠䷞䷷䷽䷴䷦䷳䷎䷋䷬䷢䷏䷓䷇䷖䷁",
        "mawangdui": "䷀䷋䷠䷉䷅䷌䷘䷫䷳䷙䷖䷨䷃䷕䷚䷑䷜䷄䷇䷦䷻䷾䷂䷯䷲䷡䷏䷽䷵䷧䷶䷟䷁䷊䷎䷒䷆䷣䷗䷭䷹䷪䷬䷞䷮䷰䷐䷛䷝䷍䷢䷷䷥䷿䷔䷱䷸䷈䷓䷴䷼䷺䷤䷩",
        "jingfang": "䷀䷫䷠䷋䷓䷖䷢䷍䷲䷏䷧䷟䷭䷯䷛䷐䷜䷻䷂䷾䷰䷶䷣䷆䷳䷕䷙䷨䷥䷉䷼䷴䷁䷗䷒䷊䷡䷪䷄䷇䷸䷈䷤䷩䷘䷔䷚䷑䷝䷷䷱䷿䷃䷺䷅䷌䷹䷮䷬䷞䷦䷎䷽䷵",
        "shaoyong": "䷁䷖䷇䷓䷏䷢䷬䷋䷎䷳䷦䷴䷽䷷䷞䷠䷆䷃䷜䷺䷧䷿䷮䷅䷭䷑䷯䷸䷟䷱䷛䷫䷗䷚䷂䷩䷲䷔䷐䷘䷣䷕䷾䷤䷶䷝䷰䷌䷒䷨䷻䷼䷵䷥䷹䷉䷊䷙䷄䷈䷡䷍䷪䷀",
        "siu": "䷀䷫䷌䷉䷈䷍䷪䷠䷘䷼䷙䷡䷅䷤䷥䷄䷸䷝䷹䷱䷰䷛䷋䷩䷨䷊䷺䷕䷵䷴䷔䷻䷑䷶䷷䷐䷟䷞䷮䷯䷾䷿䷓䷚䷒䷃䷣䷳䷲䷢䷂䷭䷽䷬䷜䷦䷧䷗䷆䷎䷏䷇䷖䷁",
    }

    def __init__(self, value):
        self._value = value

    @property
    def wen(self):
        return self._seq["wen"].index(self._Y[self._value]) + 1

    def __str__(self):
        return self._Y[self._value]


class ChineseHouse(YHouse):
    def __init__(self, rooms: List[YSequence]):
        super().__init__(rooms)

        # special case of all sixes
        if len(self.rooms) == 4 and len(self.rooms[3]) == 9:
            last = self._rooms[3]
            self._rooms[3] = last[:-1]
            self._rooms.append(last[-1])

    @property
    def composition(self):
        result = str(self.rooms[0])
        for i, room in enumerate(self.rooms[1:4]):
            offset = 0

            if room.product == Yang:
                offset = 1
            elif room.product == Yin:
                offset = 2
            elif room.product == OldYang:
                offset = 3
            elif room.product == OldYin:
                offset = 4

            result += " " * offset * (i + 1) + str(room)

        result += " " * (49 - len(result)) + str(self.rooms[4])
        return result

    @property
    def major(self):
        lines = []

        for room in self.rooms[1:4]:
            lines.append(room[0::4] + room[1::4])
            lines.append(room[2::4] + room[3::4])

        return YSequence([l.product for l in lines])

    def line_length(self):
        return 12 - (len(self.rooms[1]) + len(self.rooms[2]) + len(self.rooms[3])) // 4

    @staticmethod
    def play() -> List[YSequence]:
        # first assemble a pile
        pile = [Yin] * 22 + [Yang] * 16 + [OldYang] * 9 + [OldYin] * 3

        # shuffle
        shuffle(pile)

        # pull the intent
        intent = pile.pop()

        # plan scores and start
        start = None
        rooms = [None, None, None]

        for r, _ in enumerate(rooms):
            shuffle(pile)
            score = []

            length = len(pile)
            split = int(uniform(4, length - 4))

            left = pile[:split]
            right = pile[split:]

            shuffle(left)
            shuffle(right)

            # pop the wave starter
            if not start:
                start = right.pop()
            else:
                score += [right.pop()]

            left_remainder = len(left) % 4 or 4
            right_remainder = len(right) % 4 or 4

            left, score_left = left[:-left_remainder], left[-left_remainder:]
            right, score_right = right[:-right_remainder], right[-right_remainder:]

            pile = left + right

            score += score_left + score_right
            rooms[r] = score

        return [YSequence(start), *[YSequence(r) for r in rooms], YSequence(intent)]


class Translate(YSequence):
    def __call__(self, value):
        if value.startswith("y"):
            return self.from_y(value)

        # test if hexagram (x)

        elif value.startswith("w"):
            return self.from_w(value)

        # test if "vimcode" from core (v)

        # test if unicode (u)

        # test if dot-notation (t)

    def from_y(self, value):
        return value

    def from_w(self, value):
        return value
