# Import block
from typing import List
import sys

from robol_lang import *


class TestCode:
    def __init__(self):
        pass

    def test1(self):


        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        p.add_statement(Start(NumberExp(23), NumberExp(30)))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Step(NumberExp(15)))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(NumberExp(15)))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(2), NumberExp(3))))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(ArithmeticExp(BinaryOp.PLUS, NumberExp(17), NumberExp(20))))
        p.add_statement(Stop())


        p.interpret()


    def test2(self):

        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        p.add_statement(Binding(Identifier("i"), NumberExp(5)))
        p.add_statement(Binding(Identifier("j"), NumberExp(3)))
        p.add_statement(Start(NumberExp(23), NumberExp(6)))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(ArithmeticExp(BinaryOp.MULT, NumberExp(3), Identifier("i"))))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Step(NumberExp(15)))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Step(
            ArithmeticExp(
                BinaryOp.MINUS,
                ArithmeticExp(BinaryOp.MINUS, NumberExp(12), Identifier("i")),
                Identifier("j")
                )
            )
        )
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Step(
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
        p.add_statement(Stop())
        
        p.interpret()


    def test3(self):
        
        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        p.add_statement(Binding(Identifier("i"), NumberExp(5)))
        p.add_statement(Binding(Identifier("j"), NumberExp(3)))
        p.add_statement(Start(NumberExp(23), NumberExp(6)))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(
            ArithmeticExp(
                BinaryOp.MULT, 
                NumberExp(3),
                Identifier("i"),
            )
        ))
        p.add_statement(Turn(Direction.COUNTERCLOCKWISE))
        p.add_statement(Step(NumberExp(15)))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Turn(Direction.CLOCKWISE))
        p.add_statement(Step(NumberExp(4)))
        p.add_statement(Turn(Direction.CLOCKWISE))

        loop = Loop()
        loop.add_statement(Step(Identifier("j")))
        loop.add_statement(Assignment(Identifier("j"), Assign.DEC))
        loop.condition = BoolExp(ArithmeticExp(BinaryOp.GREATER, Identifier("j"), NumberExp(1)))
        p.add_statement(loop)

        p.add_statement(Stop())
        
        p.interpret()


    def test4(self):

        p: Program = Program(Grid(NumberExp(64), NumberExp(64)), Robot())

        p.add_statement(Binding(Identifier("i"), NumberExp(8)))
        p.add_statement(Start(NumberExp(1), NumberExp(1)))

        loop = Loop()
        loop.add_statement(Step(Identifier("i")))
        loop.condition = BoolExp(ArithmeticExp(BinaryOp.LESS, Identifier("i"), NumberExp(100)))
        p.add_statement(loop)
        p.add_statement(Stop())

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

