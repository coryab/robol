# Import block
from typing import List
from robol import *

class TestCode:
    def __init__(self):
        pass

    def test1(self):
        robot: Robot = Robot()
        grid: Grid = Grid(NumberExp(64, robot), NumberExp(64, robot), robot)
        start: Start = Start(NumberExp(23, robot), NumberExp(30, robot), robot)
        statements: List = []
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Step(NumberExp(15, robot), robot))
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(NumberExp(15, robot), robot))
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(ArithmeticExp(BinaryOp.PLUS,\
                NumberExp(2, robot), NumberExp(3, robot), robot), robot))
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(ArithmeticExp(BinaryOp.PLUS,\
                NumberExp(17, robot), NumberExp(20, robot), robot), robot))
        statements.append(Stop(robot))

        robot.start = start
        robot.statements = statements
        program: Program = Program(grid, robot)

        program.interpret()


if __name__ == "__main__":
    tests = TestCode()
    tests.test1()
