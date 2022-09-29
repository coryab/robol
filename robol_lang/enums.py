from enum import Enum, unique


@unique
class Direction(Enum):
    """ Signifies the direction Turn should turn."""

    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


@unique
class BinaryOp(Enum):
    """ Signifies the binary operation to be used in ArithmeticExp."""
    PLUS = 1
    MINUS = 2
    MULT = 3
    LESS = 4
    GREATER = 5
    EQUALS = 6


@unique
class Assign(Enum):
    """ Signifies if Assignment should increment or decrement."""
    INC = 1
    DEC = 2
