# Import block
from typing import List

class TestCode:
    def __init__(self):
        pass

    def test1():
        grid: Grid = Grid(NumberExp(64), NumberExp(64))
        start: Start = Start(NumberExp(23), NumberExp(30))
        statements: List = []
        statements.append(Turn(Direction.clockwise))
        statements.append(Turn(Direction.clockwise))
        statements.append(Step(NumberExp(15)))
        statements.append(Turn(Direction.counterclockwise))
        statements.append(Step(NumberExp(15)))
        statements.append(Turn(Direction.counterclockwise))
        statements.append(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(2), NumberExp(3))))
        statements.append(Turn(Direction.counterclockwise))
        statements.append(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(17), NumberExp(20))))

        program: Program = Program(grid, )

        program.interpret()
