from __future__ import annotations
from typing import Dict
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
    
    def __init__(self, grid: Grid, robot: Robot):
        self.grid = grid
        self.robot = robot

    
    def interpret(self):
        self.robot.grid = self.grid
        self.robot.interpret()


class Grid(Robol):

    def __init__(self, east: Expression, north: Expression, r: Robot):
        self.east = east
        self.north = north
        self.r = r

    def interpret(self):
        self.r.stack.append(self.north)
        self.r.stack.append(self.east)


class Robot(Robol):

    def __init__(self):
        self.binding_list = None
        self.start = None
        self.statements = None
        self.grid = None
        self.stack = []
        self.bindings = {}
        self.position = {
                "east": 0,
                "north": 0
                }
        self.direction = 0


    def interpret(self):
        if self.binding_list:
            for i in self.binding_list:
                i.interpret()
        if self.start:
            self.start.interpret()
        if self.statements:
            for i in self.statements:
                i.interpret()


class Start:

    def __init__(self, east: Expression, north: Expression, r: Robot):
        self.east = east
        self.north = north
        self.r = r

    def interpret(self):
        self.east.interpret()
        self.r.position["east"] = self.r.stack.pop()
        print(f"Position East: {self.r.position['east']}")

        self.north.interpret()
        self.r.position["north"] = self.r.stack.pop()
        print(f"Position North: {self.r.position['north']}")


class Binding(Robol):

    def __init__(self, ident: Identifier, exp: Expression, r: Robot):
        self.ident = ident
        self.exp = exp
        self.r = r

    def interpret(self):
        self.ident.interpret()
        ident = self.r.stack.pop()

        self.exp.interpret()
        exp = self.r.stack.pop()

        self.r.bindings[ident] = exp


# Statement and subclasses
class Statement(Robol, ABC):
    
    @abstractmethod
    def interpret(self):
        pass


class Assignment(Statement):

    def __init__(self, identifer: Identifier, assign: Assign, r: Robot):
        self.identifier = identifier
        self.assign = assign
        self.r = r

    def interpret(self):
        self.identifier.interpret()
        ident = self.r.stack.pop()

        match self.assign:
            case Assign.INC:
                self.r.bindings[ident] += 1
            case Assign.DEC:
                self.r.bindings[ident] -= 1
            case _:
                raise Exception("Something went wrong in Assignment")


class Loop(Statement):

    def __init__(self, statements: List[Statement], condition: BoolExp):
        self.statements = statements
        self.condition = condition

    def interpret(self):
        while self.condition.interpret():
            for i in self.statements:
                i.interpret()


class Stop(Statement):

    def __init__(self, r: Robot):
        self.r = r

    def interpret(self):
        print(f"Position: ({self.r.position['east']}, {self.r.position['north']})")


class Turn(Statement):

    def __init__(self, direction: Direction, r: Robot):
        self.direction = direction
        self.r = r

    def interpret(self):
        match self.direction:
            case Direction.CLOCKWISE:
                self.r.direction = (self.r.direction + 1) % 4
            case Direction.COUNTERCLOCKWISE:
                self.r.direction = (self.r.direction - 1) % 4
        print(f"Direction: {self.r.direction}")


class Step(Statement):

    def __init__(self, exp: Expression, r: Robot):
        self.exp = exp
        self.r = r

    def interpret(self):
        self.exp.interpret()
        exp = self.r.stack.pop()
        print(f"Steps: {exp}")
        match self.r.direction:
            case 0:
                self.r.position["east"] += exp
            case 1:
                self.r.position["north"] -= exp
            case 2:
                self.r.position["east"] -= exp
            case 3:
                self.r.position["north"] += exp


# Expressions and subclasses
class Expression(ABC):

    @abstractmethod
    def interpret(self):
        pass


class ArithmeticExp(Expression):

    def __init__(self, op: BinaryOp, left: expression, right: Expression,\
            r: Robot):
        self.op = op
        self.left = left
        self.right = right
        self.r = r

    def interpret(self):
        self.left.interpret()
        left = self.r.stack.pop()

        self.right.interpret()
        right = self.r.stack.pop()

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

        self.r.stack.append(out)




class BoolExp(Expression):

    def __init__(self, op: BinaryOp, left: Expression, right: Expression,\
            r: Robot):
        self.op = op
        self.left = left
        self.right = right
        self.r = r

    def interpret(self):
        self.left.interpret()
        left = self.r.stack.pop()

        self.right.interpret()
        right = self.r.stack.pop()

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

        self.r.stack.append(out)


class NumberExp(Expression):

    def __init__(self, val: int, r: Robot):
       self.val = val
       self.r = r

    def interpret(self):
        self.r.stack.append(self.val)


class Identifier(Expression):

    def __init__(self, identifier: Identifier, r: Robot):
        self.identifier = identifier
        self.r = r

    def interpret(self):
        self.r.stack.append(self.identifier)


class Test(Robol):

    def __init__(self):
        self.stack = []

    def interpret(self):
        pass

if __name__ == "__main__":
    t = Test()
    num = NumberExp(64, t)
    ident = Identifier("l", t)
    print(t.stack)
    num.interpret()
    print(t.stack)
    ident.interpret()
    print(t.stack)
    b = BoolExp(BinaryOp.LESS, NumberExp(45, t), NumberExp(34, t), t)
    b.interpret()
    print(t.stack)
    a = ArithmeticExp(BinaryOp.PLUS, NumberExp(45, t), NumberExp(34, t), t)
    a.interpret()
    print(t.stack)
    
