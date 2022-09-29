from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from robol_lang.interfaces import Expression
from robol_lang.enums import BinaryOp

if TYPE_CHECKING:
    from robol_lang.robol import Robot


class ArithmeticExp(Expression):
    """ Class that evaluates arithmetic expressions

    From the assignment, I have interpretted that relational operators are also
    part of the operators used in arithmetic expressions.

    Attributes:
        op (BinaryOp): The binary operation of the expression.
        left (Expression): The left side of the expression.
        right (Expression): The right side of the expression.
    """

    def __init__(self, op: BinaryOp, left: Expression, right: Expression)\
            -> None:
        """ Sets attributes and references."""

        self.op = op
        self.left = left
        self.right = right
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to left and right expressions.
        
        Returns:
            None
        """
   
        self.left.robot = self.robot
        self.right.robot = self.robot

    def interpret(self) -> None:
        """ Interprets left and right and evaluates the expression.

        After interpreting the left and right expression, the method matches
        the binary operation and performs it with left and right.

        Returns:
            None
        """

        self._add_references()

        self.left.interpret()
        left = self.robot.stack.pop()
        if type(self.left) is Identifier:
            left = self.robot.bindings[left]

        self.right.interpret()
        right = self.robot.stack.pop()
        if type(self.right) is Identifier:
            right = self.robot.bindings[right]

        out = None
        match self.op:
            case BinaryOp.PLUS:
                out = left + right
            case BinaryOp.MINUS:
                out = left - right
            case BinaryOp.MULT:
                out = left * right
            case BinaryOp.LESS:
                out = (left < right)*1
            case BinaryOp.GREATER:
                out = (left > right)*1
            case BinaryOp.EQUALS:
                out = (left == right)*1
            case _:
                raise Exception("Something went wrong in ArithmeticExp.")

        self.robot.stack.append(out)


class BoolExp(Expression):
    """ Class that evaluates if an arithmetic expression is true or false.

    Attributes:
        a_exp (ArithmeticExp): The arithmetic expression to evaluate.
    """

    def __init__(self, a_exp: ArithmeticExp) -> None:
        """ Sets attributes and references."""
        self.a_exp = a_exp
        self.robot: Robot = None

    def _add_references(self) -> None:
        """ Adds a reference of the robot to a_exp.
        
        Returns:
            None
        """
   
        self.a_exp.robot = self.robot
    
    def interpret(self) -> None:
        """ Evaluates the expression to be true or false.
        
        If the arithmetic expression is 0, then the boolean expression is false,
        otherwise, it's true. It reminds me of how Scheme evaluates if something
        is true or false.

        Returns:
            None
        """ 

        self._add_references()

        self.a_exp.interpret()
        ans = self.robot.stack.pop()

        if ans == 0:
            self.robot.stack.append(False)
        else:
            self.robot.stack.append(True)


class NumberExp(Expression):
    """ Class that represents a number.

    Attributes:
        val (int): The value of the number.
    """

    def __init__(self, val: int) -> None:
        """ Sets attribute."""

        self.val = int(val)
        self.robot = None

    def interpret(self) -> None:
        """ Appends the value to the stack of the robot.

        Returns:
            None
        """

        self.robot.stack.append(self.val)


class Identifier(Expression):
    """ Class that represents an identifier.

    Attributes:
        identifier (Identifier): The value of the identifier.
    """

    def __init__(self, identifier: str) -> None:
        """ Sets Attribute."""

        self.identifier = identifier
        self.robot = None

    def interpret(self) -> None:
        """ Appends the value to the stack of the robot.

        Returns:
            None
        """

        self.robot.stack.append(self.identifier)

