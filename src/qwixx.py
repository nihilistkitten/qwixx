"""Let's play Qwixx."""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


def triangular_of(n):
    """Get the nth triangular number."""
    # TODO: maybe a bug in scoring ?
    return sum(range(n + 1))


def one_die():
    return random.randint(1, 6)


class Qwixx:
    """A game of Qwixx."""

    def __init__(self, players):
        """Start a game."""
        self.players = []
        number = 0
        for player in players:
            self.players.append(player(number))
            number += 1

        self.boards = [Board() for _ in range(len(self.players))]
        self.locked = {
            "red": False,
            "yellow": False,
            "green": False,
            "blue": False,
        }
        self.active = 0

    def _is_over(self):
        return any(board.game_is_over() for board in self.boards)

    def _roll_for(self, color):
        if self.locked[color]:
            return None
        return one_die()

    def _roll_dice(self):
        public = (one_die(), one_die())

        # TODO: is there a less code-duplicate-y way to do this
        red = self._roll_for("red")
        yellow = self._roll_for("yellow")
        green = self._roll_for("green")
        blue = self._roll_for("blue")

        return DieRoll(public, red, yellow, green, blue)

    def play(self):
        """Play the game."""
        while not self._is_over():
            # play the game!!

            die_roll = self._roll_dice()
            # make each agent move
            for player in self.players:
                player.move(die_roll, self.boards, self.active)
            self.active = self.active + 1 % len(self.players)

        scores = [*map(lambda board: board.score(), self.boards)]
        print(scores)


class Agent(ABC):
    """An abstract player."""

    def __init__(self, number):
        """Create an agent."""
        self.number = number

    @abstractmethod
    def move(self, dice, boards, active_player):
        """Make a move."""


class Board:
    """A board."""

    def __init__(self):
        """Create a board."""
        # [2 - 12, and then lock]
        self.red = [False for _ in range(12)]
        self.yellow = [False for _ in range(12)]

        # [12 - 2, and then lock]
        self.green = [False for _ in range(12)]
        self.blue = [False for _ in range(12)]

        self.negs = 0

    def game_is_over(self):
        """Check whether the game is over."""
        num_locked = sum((self.red[-1], self.yellow[-1], self.green[-1], self.blue[-1]))
        return self.negs >= 4 or num_locked >= 2

    def score(self):
        """Determine the score."""
        red = triangular_of(sum(self.red))
        yellow = triangular_of(sum(self.yellow))
        green = triangular_of(sum(self.green))
        blue = triangular_of(sum(self.blue))

        return red + yellow + green + blue - self.negs * 5

    def row_of(self, color):
        if color in ("red", "r"):
            return self.red
        if color in ("yellow", "y"):
            return self.yellow
        if color in ("green", "g"):
            return self.green
        if color in ("blue", "b"):
            return self.blue

        raise ValueError(f"invalid color: {color}")

    def cross(self, number, color):
        row = self.row_of(color)

        # invert blue and green
        if color in ("blue", "green"):
            # ex 2 -> 12
            number = 14 - number

        # find the last number in the row
        last_cross = 1
        for i in reversed(range(len(row))):
            if row[i]:
                last_cross = i + 2
                break

        if number <= last_cross:
            raise ValueError("that is not a valid choice. do better.")

        # TODO: handle locking
        if number == 12:
            if sum(row) < 5:
                raise ValueError(f"you cannot lock {color} right now")

            row[-1] = True

        row[number - 2] = True

    @staticmethod
    def _row_to_str(row):
        ret = ""
        have_hit_x = False  # while iterating backwards
        for is_crossed in row[::-1]:
            if is_crossed:
                ret += "X"
                have_hit_x = True
            elif have_hit_x:
                ret += "-"
            else:
                ret += " "

            ret += "  "

        return ret[::-1]

    def __repr__(self):
        ret = ""
        ret += "C | 2  3  4  5  6  7  8  9  10 11 12 L\n"
        ret += "R | " + self._row_to_str(self.red) + "\n"
        ret += "Y | " + self._row_to_str(self.yellow) + "\n"
        ret += "C | 12 11 10 9  8  7  6  5  4  3  2  L\n"
        ret += "G | " + self._row_to_str(self.green) + "\n"
        ret += "B | " + self._row_to_str(self.blue) + "\n"

        ret += f"Negs: {self.negs}"

        return ret


@dataclass
class DieRoll:
    """A die roll."""

    public: tuple[int, int]
    red: Optional[int]
    yellow: Optional[int]
    green: Optional[int]
    blue: Optional[int]

    def value_of(self, color):
        if color in ("red", "r"):
            return self.red
        if color in ("yellow", "y"):
            return self.yellow
        if color in ("green", "g"):
            return self.green
        if color in ("blue", "b"):
            return self.blue

        raise ValueError(f"invalid color: {color}")

    def options_for(self, color):
        value = self.value_of(color)
        if value is None:
            raise ValueError(f"color is locked: {color}")
        return self.public[0] + value, self.public[1] + value

    def public_sum(self):
        return self.public[0] + self.public[1]
