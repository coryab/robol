from __future__ import annotations
from typing import Dict, List
from abc import ABC, abstractmethod
from enum import Enum, unique

@unique
class Direction(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


@unique
class BinaryOp(Enum):
    PLUS = 1
    MINUS = 2
    MULT = 3
    LESS = 4
    GREATER = 5
    EQUALS = 6


@unique
class Assign(Enum):
    INC = 1
    DEC = 2


class Robol(ABC):

    @abstractmethod
    def interpret(self):
        raise NotImplementedError("interpret method is not implemented")


class Program(Robol):
    
    def __init__(self):
        self.stack = []
        self.statements = []
        self.grid = None
        self.bindings = {}
        self.robot = None

    
    def interpret(self):
        for i in self.statements:
            i.interpret()


    def add_robot(self, r: Robot):
        r.p = self
        self.robot = r


    def add_grid(self, grid: Grid):
        grid.p = self
        self.grid = grid


    def add_statement(self, s: Statement):
        s.p = self
        self.statements.append(s)



class Robot(Robol):

    def __init__(self):
        self.position = {
                "east": 0,
                "north": 0
                }
        self.direction = 0
        self.p = None


    def interpret(self):
        pass


class Grid(Robol):

    def __init__(self, east: Expression, north: Expression):
        self.east = east
        self.north = north
        self.p = None

    def interpret(self):
        self.east.p = self.p
        self.north.p = self.p
        self.east.interpret()
        # self.p.stack.append(self.p.stack.pop())
        self.north.interpret()
        # self.p.stack.append(self.p.stack.pop())


class Start(Robol):

    def __init__(self, east: Expression, north: Expression):
        self.east = east
        self.north = north
        self.p = None

    def interpret(self):
        self.east.p = self.p
        self.north.p = self.p
        self.east.interpret()
        self.p.robot.position["east"] = self.p.stack.pop()

        self.north.interpret()
        self.p.robot.position["north"] = self.p.stack.pop()
        print(f"Start position: ({self.p.robot.position['east']}, {self.p.robot.position['north']})")


class Binding(Robol):

    def __init__(self, ident: Identifier, exp: Expression):
        self.ident = ident
        self.exp = exp
        self.p = None

    def interpret(self):
        self.ident.p = self.p
        self.exp.p = self.p
        self.ident.interpret()
        ident = self.p.stack.pop()

        self.exp.interpret()
        exp = self.p.stack.pop()

        self.p.bindings[ident] = exp


# Statement and subclasses
class Statement(Robol):
    
    @abstractmethod
    def interpret(self):
        pass


class Assignment(Statement):

    def __init__(self, identifier: Identifier, assign: Assign):
        self.identifier = identifier
        self.assign = assign
        self.p = None

    def interpret(self):
        self.identifier.p = self.p
        self.identifier.interpret()
        ident = self.p.stack.pop()

        match self.assign:
            case Assign.INC:
                self.p.bindings[ident] += 1
            case Assign.DEC:
                self.p.bindings[ident] -= 1
            case _:
                raise Exception("Something went wrong in Assignment")


class Loop(Statement):

    def __init__(self):
        self.statements = []
        self.condition = None
        self.p = None

    def interpret(self):
        self.condition.p = self.p
        for i in self.statements:
            i.p = self.p
        while True:
            for i in self.statements:
                i.interpret()

            self.condition.interpret()
            bool_val = self.p.stack.pop()
            if bool_val == 0:
                break

    def add_statement(self, s: Statement):
        self.statements.append(s)


class Stop(Statement):

    def __init__(self):
        self.p = None

    def interpret(self):
        print(f"End position: ({self.p.robot.position['east']}, {self.p.robot.position['north']})\n\n")


class Turn(Statement):

    def __init__(self, direction: Direction):
        self.direction = direction
        self.p = None

    def interpret(self):
        match self.direction:
            case Direction.CLOCKWISE:
                self.p.robot.direction = (self.p.robot.direction + 1) % 4
            case Direction.COUNTERCLOCKWISE:
                self.p.robot.direction = (self.p.robot.direction - 1) % 4
        print(f"Direction: {self.p.robot.direction}")


class Step(Statement):

    def __init__(self, exp: Expression):
        self.exp = exp
        self.p = None

    def interpret(self):
        self.exp.p = self.p
        self.exp.interpret()
        exp = self.p.stack.pop()
        if type(self.exp) is Identifier:
            exp = self.p.bindings[exp]

        self.p.grid.interpret()
        grid_east = self.p.stack.pop()
        grid_north = self.p.stack.pop()

        print(f"Steps: {exp}")
        match self.p.robot.direction:
            case 0:
                if self.p.robot.position["east"] + exp > grid_east:
                    raise Exception("The bounds of the grid have been overstepped")
                self.p.robot.position["east"] += exp
            case 1:
                if self.p.robot.position["north"] - exp < 0:
                    raise Exception("The bounds of the grid have been overstepped")
                self.p.robot.position["north"] -= exp
            case 2:
                if self.p.robot.position["east"] - exp < 0:
                    raise Exception("The bounds of the grid have been overstepped")
                self.p.robot.position["east"] -= exp
            case 3:
                if self.p.robot.position["north"] + exp > grid_north:
                    raise Exception("The bounds of the grid have been overstepped")
                self.p.robot.position["north"] += exp


# Expressions and subclasses
class Expression(Robol):

    @abstractmethod
    def interpret(self):
        pass


class ArithmeticExp(Expression):

    def __init__(self, op: BinaryOp, left: Expression, right: Expression):
        self.op = op
        self.left = left
        self.right = right
        self.p = None

    def interpret(self):
        self.left.p = self.p
        self.right.p = self.p
        self.left.interpret()
        left = self.p.stack.pop()
        if type(self.left) is Identifier:
            left = self.p.bindings[left]

        self.right.interpret()
        right = self.p.stack.pop()
        if type(self.right) is Identifier:
            right = self.p.bindings[right]

        out = None
        match self.op:
            case BinaryOp.PLUS:
                out = left + right
            case BinaryOp.MINUS:
                out = left - right
            case BinaryOp.MULT:
                out = left * right
            case _:
                raise Exception("Something went wrong in ArithmeticExp.")

        self.p.stack.append(out)


class BoolExp(Expression):

    def __init__(self, op: BinaryOp, left: Expression, right: Expression):
        self.op = op
        self.left = left
        self.right = right
        self.p = None

    def interpret(self):
        self.left.p = self.p
        self.right.p = self.p
        self.left.interpret()
        left = self.p.stack.pop()
        if type(self.left) is Identifier:
            left = self.p.bindings[left]

        self.right.interpret()
        right = self.p.stack.pop()
        if type(self.right) is Identifier:
            right = self.p.bindings[right]

        out = None
        match self.op:
            case BinaryOp.LESS:
                out = (left < right)*1
            case BinaryOp.GREATER:
                out = (left > right)*1
            case BinaryOp.EQUALS:
                out = (left == right)*1
            case _:
                raise Exception("Something went wrong in BoolExp.")

        self.p.stack.append(out)


class NumberExp(Expression):

    def __init__(self, val: int):
       self.val = int(val)
       self.p = None

    def interpret(self):
        self.p.stack.append(self.val)


class Identifier(Expression):

    def __init__(self, identifier: Identifier):
        self.identifier = identifier
        self.p = None

    def interpret(self):
        self.p.stack.append(self.identifier)

