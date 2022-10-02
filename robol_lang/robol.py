from __future__ import annotations
from typing import Dict, List, Union, TYPE_CHECKING
from abc import ABC, abstractmethod
from enum import Enum, unique

from robol_lang.interfaces import Robol
from robol_lang.expressions import Identifier
from robol_lang.enums import Orientation

if TYPE_CHECKING:
    from robol_lang.interfaces import Statement, Expression


class Program(Robol):
    """ Class that contains all components necessary to run.

    This is the starting point of a robol program, and is necessary in order
    for a program to work.

    Attributes:
        grid (Grid): The grid that the robot will move on.
        
        robot (Robot): The robot itself.
    """

    def __init__(self, grid: Grid, robot: Robot) -> None:
        """ Sets attributes."""

        self.grid: Grid = grid 
        self.robot: Robot = robot 

    def _add_references(self) -> None:
        """ Adds references to the grid and robot.

        The robot needs a reference to the program, and the grid needs a
        reference to the robot.

        Returns:
            None
        """

        self.grid.robot = self.robot
        self.robot.program = self

    def interpret(self) -> None:
        """ Calls the interpret method of the robot.

        Before calling the interpret method of the robot, the method adds a
        reference of the program to the robot, and a reference of the robot
        to the grid.

        Returns:
            None
        """

        self._add_references()

        self.robot.interpret()


class Robot(Robol):
    """ Class that interprets interpretables and moves around the grid.

    This is the heart of the program. The Robot class holds almost all the
    information of the program and moves on the grid according to what the
    interpretables interpret.
    
    Attributes:
        position (Dict): The current position of the robot.
        
        orientation (Orientation): The current orientation of the robot.
        
        bindings (Dict): The bindings of the robot.
        
        interpretables (List): A list of interpretable instances.
        
        stack (List): The robot's stack to push and pop values.
        
        program (Program): A reference to the program.
    """

    def __init__(self):
        """ Sets attributes and references."""

        self.position = {
                "east": 0,
                "north": 0
                }
        self.orientation = Orientation.EAST
        self.bindings = {}
        self.interpretables = []
        self.stack = []
        self.program = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to each statement.

        Each statement needs a reference to the robot, so to make it easier
        for a user to input statements, this method handles the references.

        Returns:
            None
        """

        for interpretable in self.interpretables:
            interpretable.robot = self

    def interpret(self) -> None:
        """ Interprets each interpretable in interpretables.

        Returns:
            None
        """

        self._add_references()

        for interpretable in self.interpretables:
            interpretable.interpret()


class Grid(Robol):
    """ Class that contains the dimensions of the grid.

    This defines the space that the robot is allowed to travel on.

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
    """ Class that contains an identifier and the expression to bind to it.

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
        """ Binds a value to an identifier.

        Interprets ident and exp, and inserts the expression into the bindings
        dictionary of the robot with the identifier as the key.

        Returns:
            None
        """

        self._add_references()

        self.ident.interpret()
        ident = self.robot.stack.pop()

        self.exp.interpret()
        exp = self.robot.stack.pop()

        self.robot.bindings[ident] = exp

