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


class Robol(ABC):

    @abstractmethod
    def interpret(self):
        raise NotImplementedError("interpret method is not implemented")


class Program(Robol):
    
    def __init__(self, grid: Grid, robot: Robot):
        self.grid = grid
        self.robot = robot

    
    def interpret(self):
        pass


class Grid(Robol):

    def __init__(self, x: Expression, y: Expression):
        self.x = x
        self.y = y

    def interpret(self):
        pass


class Robot(Robol):

    def __init__(self, bindings: Dict[Binding], start: Start,\
            statements: List[Statement], grid: Grid):
        self.bindings = bindings
        self.start = start
        self.statements = statements
        self.grid = grid
        self.stack = []
        self.bindings = {}

    def interpret(self):
        pass


class Start:

    def __init__(self, x: Expression, y: Expression):
        self.x = x
        self.y = y

    def interpret():
        pass


class Binding(Robol):

    def __init__(self, ident: Identifier, exp: Expression):
        self.ident = ident
        self.exp = exp

    def interpret(self):
        pass


# Statement and subclasses
class Statement(Robol, ABC):
    
    @abstractmethod
    def interpret(self):
        pass


class Assignment(Statement):

    def interpret(self):
        pass


class Loop(Statement):

    def __init__(self, statements: List[Statement], condition: BoolExp):
        self.statements = statements
        self.condition = condition

    def interpret(self):
        while self.condition.interpret():
            for i in self.statements:
                i.interpret()


class Stop(Statement):
    def interpret(self):
        pass


class Turn(Statement):

    def __init__(self, direction: Direction):
        self.direction = direction

    def interpret(self):
        pass


class Step(Statement):

    def __init__(self, exp: Expression):
        self.exp = exp

    def interpret(self):
        pass



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
    
