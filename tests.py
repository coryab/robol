# Import block
from typing import List
import sys

from robol_lang import *


class TestCode:
    def __init__(self):
        pass

    def test1(self):


        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        interpretables =  []

        interpretables.append(Start(NumberExp(23), NumberExp(30)))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Step(NumberExp(15)))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(NumberExp(15)))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(2), NumberExp(3))))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(17), NumberExp(20))))
        interpretables.append(Stop())
        
        p.robot.interpretables = interpretables

        p.interpret()


    def test2(self):

        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        interpretables = []

        interpretables.append(Binding(Identifier("i"), NumberExp(5)))
        interpretables.append(Binding(Identifier("j"), NumberExp(3)))
        interpretables.append(Start(NumberExp(23), NumberExp(6)))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(ArithmeticExp(BinaryOp.MULT, NumberExp(3), Identifier("i"))))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Step(NumberExp(15)))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Step(
            ArithmeticExp(
                BinaryOp.MINUS,
                ArithmeticExp(BinaryOp.MINUS, NumberExp(12), Identifier("i")),
                Identifier("j")
                )
            )
        )
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Step(
            ArithmeticExp(
                BinaryOp.PLUS,
                ArithmeticExp(
                    BinaryOp.MULT,
                    NumberExp(2),
                    Identifier("i")
                ),
                ArithmeticExp(
                    BinaryOp.PLUS,
                    ArithmeticExp(
                        BinaryOp.MULT,
                        NumberExp(3),
                        Identifier("j")
                    ),
                    NumberExp(1),
                ),
            ),
        ))
        interpretables.append(Stop())
        
        p.robot.interpretables = interpretables

        p.interpret()


    def test3(self):
        
        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        interpretables = []

        interpretables.append(Binding(Identifier("i"), NumberExp(5)))
        interpretables.append(Binding(Identifier("j"), NumberExp(3)))
        interpretables.append(Start(NumberExp(23), NumberExp(6)))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(
            ArithmeticExp(
                BinaryOp.MULT, 
                NumberExp(3),
                Identifier("i"),
            )
        ))
        interpretables.append(Turn(Direction.COUNTERCLOCKWISE))
        interpretables.append(Step(NumberExp(15)))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Turn(Direction.CLOCKWISE))
        interpretables.append(Step(NumberExp(4)))
        interpretables.append(Turn(Direction.CLOCKWISE))

        loop = Loop()
        loop.interpretables.append(Step(Identifier("j")))
        loop.interpretables.append(Assignment(Identifier("j"), Assign.DEC))
        loop.condition = BoolExp(ArithmeticExp(BinaryOp.GREATER, Identifier("j"), NumberExp(1)))
        interpretables.append(loop)

        interpretables.append(Stop())
        
        p.interpret()


    def test4(self):

        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        interpretables = []

        interpretables.append(Binding(Identifier("i"), NumberExp(8)))
        interpretables.append(Start(NumberExp(1), NumberExp(1)))

        loop = Loop()
        loop.interpretables.append(Step(Identifier("i")))
        loop.condition = BoolExp(ArithmeticExp(BinaryOp.LESS, Identifier("i"), NumberExp(100)))
        interpretables.append(loop)
        interpretables.append(Stop())

        p.robot.interpretables = interpretables 

        p.interpret()


    def test_all(self):
        self.test1()
        self.test2()
        self.test3()
        self.test4()




if __name__ == "__main__":
    n = sys.argv[1]

    tests = TestCode()

    match n:
        case "1":
            tests.test1()
        case "2":
            tests.test2()
        case "3":
            tests.test3()
        case "4":
            tests.test4()
        case "all":
            tests.test_all()
        case _:
            raise Exception("Invalid test")

