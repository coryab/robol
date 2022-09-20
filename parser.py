from robol import *

import sys

def build_exp(arr, robot):
    def helper(arr):
        if " " in arr[0]:
            arr = arr[0].split() + arr[1:]

        if arr[0] in "*-+":
            bin_op = None
            match arr[0]:
                case "*":
                    bin_op = BinaryOp.MULT
                case "-":
                    bin_op = BinaryOp.MINUS
                case "+":
                    bin_op = BinaryOp.PLUS

            left, rest_arr = helper(arr[1:])
            right, rest = helper(rest_arr)
            return ArithmeticExp(bin_op, left, right, robot), rest
        elif arr[0] in "<>=":
            bin_op = None
            match arr[0]:
                case "<":
                    bin_op = BinaryOp.LESS
                case ">":
                    bin_op = BinaryOp.GREATER
                case "=":
                    bin_op = BinaryOp.EQUALS
            
            left, rest_arr = helper(arr[1:])
            right, rest = helper(rest_arr)
            return BoolExp(bin_op, left, right, robot), rest
       
        else:
            n = arr[0]
            res = None
            try:
                n = int(n)
                res = NumberExp(n, robot)
            except:
                res = Identifier(n, robot)

            return res, arr[1:]

    return helper(arr)

       


if __name__ == "__main__":

    robot = Robot()
    grid = None

    statements = robot.statements

    with open(sys.argv[1], "r") as f:
        string = f.read()

        cursor = 0
        buffer = ""
        tokens = []
        while cursor < len(string):
            if string[cursor] in ", \n" and buffer != "":
                tokens.append(buffer)
                buffer = ""
            elif string[cursor] in "(":
                if buffer.strip() != "":
                    tokens.append(buffer)
                buffer = ""
                cur = cursor + 1
                while string[cur] not in ")":
                    cur += 1

                tokens.append(string[cursor+1:cur])
                cursor = cur + 1
            else:
                buffer += string[cursor]
            cursor += 1
        if buffer != "":
            tokens.append(buffer)
            
        tokens = [i.strip() for i in tokens]
        tokens = list(filter(lambda x: x != "", tokens))

        print(tokens)
        while tokens:
            # Match
            # print(tokens)
            current = tokens.pop(0)
            match current:
                case "size":
                    dims = tokens.pop(0).split("*")
                    grid = Grid(NumberExp(dims[0], robot),
                            NumberExp(dims[1], robot),
                            robot)
                case "let":
                    binder = tokens.pop(0)
                    tokens.pop(0)
                    val = tokens.pop(0)
                    robot.binding_list.append(
                            Binding(
                                Identifier(binder, robot),
                                NumberExp(val, robot),
                                robot
                            )
                    )
                case "start":
                    nums = tokens.pop(0).split(",")
                    robot.start = Start(NumberExp(nums[0], robot),
                            NumberExp(nums[1], robot), robot)
                case "turn":
                    d = Direction.CLOCKWISE if tokens.pop(0) == "clockwise" else\
                            Direction.COUNTERCLOCKWISE
                    statements.append(Turn(d, robot))
                case "step":
                    exp, arr = build_exp(tokens, robot)
                    statements.append(Step(exp, robot))
                    tokens = arr
                case "do":
                    statements = []
                case "}":
                    tokens.pop(0)
                    exp, arr = build_exp(tokens, robot)
                    robot.statements.append(Loop(statements, exp, robot))
                    tokens = arr
                    statements = robot.statements
                case s if "--" in s or "++" in s:
                    assign = Assign.INC if "++" in s else Assign.DEC
                    statements.append(Assignment(
                        Identifier(s[0], robot),
                        assign,
                        robot))
                case "stop":
                    statements.append(Stop(robot))


        program = Program(grid, robot)
        program.interpret()

        # n, arr = build_exp(["+", "*", "2", "i", "+", "*", "3", "j", "i"], robot)
        # print(n.left)
        # print(n.right)
        # print(n.left.left)
        # print(n.left.right)
        # print(n.right.left)
        # print(n.right.right)
        # print(n.right.left.left)
        # print(n.right.left.right)


    print(robot)

        
