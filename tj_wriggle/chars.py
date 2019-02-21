from enum import Enum


# Characters that make up the TJ-Wriggle board
class Chars(Enum):
    UP         = '^'
    DOWN       = 'v'
    LEFT       = '<'
    RIGHT      = '>'
    WALL       = 'x'
    EMPTY      = 'e'
    HEAD_UP    = 'U'
    HEAD_DOWN  = 'D'
    HEAD_LEFT  = 'L'
    HEAD_RIGHT = 'R'
