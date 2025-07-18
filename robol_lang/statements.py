from __future__ import annotations
from typing import TYPE_CHECKING

from robol_lang.interfaces import Statement
from robol_lang.enums import Assign, Direction, Orientation
from robol_lang.expressions import Identifier

if TYPE_CHECKING:
    from robol_lang.interfaces import Expression
    from robol_lang.robol import Robot


class Assignment(Statement):
    """ Class that will increment or decrement a binding by 1.

    Attributes:
        identifier (Identifier): The identifier to increment/decrement.
        
        assign (Assign): The enum that decides if the identifier should
        increment or decrement.
    """

    def __init__(self, identifier: Identifier, assign: Assign) -> None:
        """ Sets attributes and references"""

        self.identifier = identifier
        self.assign = assign
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to identifier.
        
        Returns:
            None
        """

        self.identifier.robot = self.robot

    def interpret(self) -> None:
        """ Interprets the identifier and increments/decrements the binding.

        Returns:
            None
        """

        self._add_references()

        self.identifier.interpret()
        ident = self.robot.stack.pop()

        match self.assign:
            case Assign.INC:
                self.robot.bindings[ident] += 1
            case Assign.DEC:
                self.robot.bindings[ident] -= 1
            case _:
                raise Exception("Something went wrong in Assignment")


class Loop(Statement):
    """ Class that will loop a set of statements until a condition is false

    Attributes:
        statements (Statements): The set of statements inside the loop.
        
        condition (BoolExp): The condition for the loop to continue looping.
    """

    def __init__(self) -> None:
        """ Sets attributes and references"""

        self.interpretables = []
        self.condition = None
        self.robot: Robot = None
   
    def _add_references(self) -> None:
        """ Adds a reference of the robot to condition, and each statement.
        
        Returns:
            None
        """
   
        self.condition.robot = self.robot

        for interpretable in self.interpretables:
            interpretable.robot = self.robot

    def interpret(self) -> None:
        """ Interprets the statements in the loop.

        This interprets the statements of the loop over and over again until
        the condition is false.

        Returns:
            None
        """

        self._add_references()

        while True:
            for interpretable in self.interpretables:
                interpretable.interpret()

            self.condition.interpret()
            bool_val = self.robot.stack.pop()
            if not bool_val:
                break


class Stop(Statement):
    """ Class that signals that the program is done."""

    def __init__(self) -> None:
        """ Sets robot to be None."""
        self.robot = None

    def interpret(self) -> None:
        """ Prints out the current position of the robot.

        Returns:
            None
        """

        print(f"End position: ({self.robot.position['east']}, {self.robot.position['north']})\n\n")


class Turn(Statement):
    """ Class that turns the robot clockwise/counterclockwise.

    Attributes:
        direction (Direction): Which direction to turn.
    """

    def __init__(self, direction: Direction) -> None:
        """ Sets attributes."""

        self.direction = direction
        self.robot: Robot = None

    def interpret(self) -> None:
        """ Sets the new orientation of the robot.

        Returns:
            None
        """

        match self.direction:
            case Direction.CLOCKWISE:
                self.robot.orientation = self.robot.orientation.succ()
            case Direction.COUNTERCLOCKWISE:
                self.robot.orientation = self.robot.orientation.pred()
        print(f"Direction: {self.robot.orientation}")


class Step(Statement):
    """ Class that moves the robot a certain amount of steps.

    Attributes:
        exp (Expression): The expression that evaluates how many steps should
        be taken.
    """

    def __init__(self, exp: Expression) -> None:
        """ Sets attributes and references."""

        self.exp = exp
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to condition, and each statement.
        
        Returns:
            None
        """
   
        self.exp.robot = self.robot

    def interpret(self) -> None:
        """ Interprets the expression and moves the robot.

        First it evaluates the expression, then it checks if the amount of
        steps would put the robot out of bounds, and if it does, then it raises
        an exception, otherwise it will move.

        Returns:
            None
        """

        self._add_references()

        self.exp.interpret()
        exp = self.robot.stack.pop()
        if type(self.exp) is Identifier:
            exp = self.robot.bindings[exp]

        self.robot.program.grid.interpret()
        grid_east = self.robot.stack.pop()
        grid_north = self.robot.stack.pop()

        print(f"Steps: {exp}")

        match self.robot.orientation:
            case Orientation.EAST:
                if self.robot.position["east"] + exp > grid_east:
                    raise Exception("The bounds of the grid have been overstepped")
                self.robot.position["east"] += exp
            case Orientation.SOUTH:
                if self.robot.position["north"] - exp < 0:
                    raise Exception("The bounds of the grid have been overstepped")
                self.robot.position["north"] -= exp
            case Orientation.WEST:
                if self.robot.position["east"] - exp < 0:
                    raise Exception("The bounds of the grid have been overstepped")
                self.robot.position["east"] -= exp
            case Orientation.NORTH:
                if self.robot.position["north"] + exp > grid_north:
                    raise Exception("The bounds of the grid have been overstepped")
                self.robot.position["north"] += exp

