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


    def test2(self):
        robot: Robot = Robot()
        grid: Grid = Grid(NumberExp(64, robot), NumberExp(64, robot), robot) 
        bindings = []
        bindings.append(Binding(Identifier("i", robot), NumberExp(5, robot),\
                robot))
        bindings.append(Binding(Identifier("j", robot), NumberExp(3, robot),\
                robot))
        start: Start = Start(NumberExp(23, robot), NumberExp(6, robot), robot)
        statements = []
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(
            ArithmeticExp(
                BinaryOp.MULT, 
                NumberExp(3, robot),
                Identifier("i", robot),
                robot), robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Step(NumberExp(15, robot), robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Step(
            ArithmeticExp(
                BinaryOp.MINUS,
                ArithmeticExp(
                    BinaryOp.MINUS,
                    NumberExp(12, robot),
                    Identifier("i", robot),
                    robot
                    ),
                Identifier("j", robot),
                robot
                ),
            robot
            )
        )
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Step(
            ArithmeticExp(
                BinaryOp.PLUS,
                ArithmeticExp(
                    BinaryOp.MULT,
                    NumberExp(2, robot),
                    Identifier("i", robot),
                    robot
                    ),
                ArithmeticExp(
                    BinaryOp.PLUS,
                    ArithmeticExp(
                        BinaryOp.MULT,
                        NumberExp(3, robot),
                        Identifier("j", robot),
                        robot
                        ),
                    NumberExp(1, robot),
                    robot
                    ),
                robot
                ),
            robot
            )
        )
        statements.append(Stop(robot))
        
        robot.binding_list = bindings
        robot.start = start
        robot.statements = statements

        program: Program = Program(grid, robot)
        program.interpret()


    def test3(self):
        
        robot: Robot = Robot()
        grid: Grid = Grid(NumberExp(64, robot), NumberExp(64, robot), robot) 
        bindings = []
        bindings.append(Binding(Identifier("i", robot), NumberExp(5, robot),\
                robot))
        bindings.append(Binding(Identifier("j", robot), NumberExp(3, robot),\
                robot))
        start: Start = Start(NumberExp(23, robot), NumberExp(6, robot), robot)
        statements = []
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(
            ArithmeticExp(
                BinaryOp.MULT, 
                NumberExp(3, robot),
                Identifier("i", robot),
                robot), robot))
        statements.append(Turn(Direction.COUNTERCLOCKWISE, robot))
        statements.append(Step(NumberExp(15, robot), robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Step(NumberExp(4, robot), robot))
        statements.append(Turn(Direction.CLOCKWISE, robot))
        statements.append(Loop(
                [
                    Step(Identifier("j", robot), robot),
                    Assignment(Identifier("j", robot), Assign.DEC, robot)
                ],
                BoolExp(
                    BinaryOp.GREATER,
                    Identifier("j", robot),
                    NumberExp(1, robot),
                    robot
                ),
                robot
            )
        )
        statements.append(Stop(robot))
        
        robot.binding_list = bindings
        robot.start = start
        robot.statements = statements

        program: Program = Program(grid, robot)
        program.interpret()


    def test4(self):

        robot: Robot = Robot()
        grid: Grid = Grid(NumberExp(64, robot), NumberExp(64, robot), robot) 
        bindings = []
        bindings.append(Binding(Identifier("i", robot), NumberExp(8, robot),\
                robot))
        start: Start = Start(NumberExp(1, robot), NumberExp(1, robot), robot)
        statements = []
        statements.append(Loop(
                [
                    Step(Identifier("i", robot), robot),
                ],
                BoolExp(
                    BinaryOp.LESS,
                    Identifier("i", robot),
                    NumberExp(100, robot),
                    robot
                ),
                robot
            )
        )
        statements.append(Stop(robot))

        robot.binding_list = bindings
        robot.start = start
        robot.statements = statements

        program: Program = Program(grid, robot)
        program.interpret()


    def test_all(self):
        self.test1()
        self.test2()
        self.test3()
        self.test4()




if __name__ == "__main__":
    tests = TestCode()
    #tests.test1()
    #tests.test2()
    #tests.test3()
    #tests.test4()
    tests.test_all()
