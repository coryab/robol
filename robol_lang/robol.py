from __future__ import annotations
from typing import Dict, List, Union, TYPE_CHECKING
from abc import ABC, abstractmethod
from enum import Enum, unique

from robol_lang.interfaces import Robol
from robol_lang.expressions import Identifier

if TYPE_CHECKING:
    from robol_lang.interfaces import Statement, Expression


class Program(Robol):
    """ Class that contains all components necessary to run.

    Attributes:
        grid (Grid): The grid that the robot will move on.
        
        robot (Robot): The robot itself.
    """

    def __init__(self, grid: Grid, robot: Robot) -> None:
        """ Sets attributes and references."""

        self.grid: Grid = grid 
        self.robot: Robot = robot 

    def interpret(self) -> None:
        """ Calls the interpret method of the robot.

        Returns:
            None
        """

        self._add_references()

        self.robot.interpret()

    def _add_references(self) -> None:
        """ Adds references to the grid and robot.

        The robot needs a reference to the program, and the grid needs a
        reference to the robot.

        Returns:
            None
        """

        self.grid.robot = self.robot
        self.robot.p = self

    def add_statement(self, s: Union[Binding, Start, Statement]):
        s.robot = self.robot
        self.robot.statements.append(s)


class Robot(Robol):
    """ Class that interprets statements and executes them.

    """

    def __init__(self):
        """ Sets attributes and references."""

        self.position = {
                "east": 0,
                "north": 0
                }
        self.direction = 0
        self.bindings = {}
        self.statements = []
        self.stack = []
        self.p = None


    def _add_references(self) -> None:
        """ Adds a reference of the robot to each statement.

        Each statement needs a reference to the robot, so to make it easier
        for a user to input statements, this method handles the references.

        Returns:
            None
        """

        for statement in self.statements:
            statement.robot = self


    def interpret(self) -> None:
        """ Interprets each statement in statements

        Returns:
            None
        """

        self._add_references()

        for statement in self.statements:
            statement.interpret()


class Grid(Robol):
    """ Class that contains the dimensions of the grid.

    Grid contains the dimensions of the grid taht the robot can move around on.

    Attributes:
        east (Expression): How far east the grid goes.

        north (Expression): How far north the grid goes.
    """

    def __init__(self, east: Expression, north: Expression) -> None:
        """ Sets attributes and references."""

        self.east = east
        self.north = north
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to the east and west expressions
        
        Returns:
            None
        """

        self.east.robot = self.robot
        self.north.robot = self.robot

    def interpret(self) -> None:
        """ Interpret both expressions.

        The result of the interpretation of the expression will be put on the
        stack and the class that called this interpret method will then be
        able to retrieve them by popping the stack.

        Returns:
            None
        """

        self._add_references()

        self.east.interpret()
        self.north.interpret()


class Start(Robol):
    """ Class that contains the starting point of the robot.

    Attributes:
        east (Expression): How far east the robot should start.
        north (Expression): How far north the robot should start.
    """

    def __init__(self, east: Expression, north: Expression):
        """ Sets attributes and references."""

        self.east = east
        self.north = north
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to the east and west expressions
        
        Returns:
            None
        """

        self.east.robot = self.robot
        self.north.robot = self.robot

    def interpret(self) -> None:
        """ Interprets east and west.

        This interprets east and west, and inserts the result into the position
        dictionary of the robot.

        Returns:
            None
        """

        self._add_references()

        self.east.interpret()
        if type(self.east) is Identifier:
            self.robot.position["east"] =\
                    self.robot.bindings[self.robot.stack.pop()]
        else:
            self.robot.position["east"] = self.robot.stack.pop()

        self.north.interpret()
        if type(self.north) is Identifier:
            self.robot.position["north"] =\
                    self.robot.bindings[self.robot.stack.pop()]
        else:
            self.robot.position["north"] = self.robot.stack.pop()
        print(f"Start position: ({self.robot.position['east']}, {self.robot.position['north']})")


class Binding(Robol):
    """ Class that contains a binding and the expression to bind.

    Attributes:
        ident (Identifier): The identifier of the binding
        exp (Expression): The expression that will be bound to the identifier.
    """

    def __init__(self, ident: Identifier, exp: Expression) -> None:
        """ Sets attributes and references."""

        self.ident = ident
        self.exp = exp
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to ident and exp.
        
        Returns:
            None
        """

        self.ident.robot = self.robot
        self.exp.robot = self.robot

    def interpret(self):
        """ Interprets ident and exp, and then binds them.

        This interprets ident and exp, and inserts the result into the bindings
        dictionary of the robot.

        Returns:
            None
        """

        self._add_references()

        self.ident.interpret()
        ident = self.robot.stack.pop()

        self.exp.interpret()
        exp = self.robot.stack.pop()

        self.robot.bindings[ident] = exp

