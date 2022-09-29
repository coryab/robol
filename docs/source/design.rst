Design
======


Robot
-----
This class contains the position, direction, bindings, and statements of the robot.

In addition, it contains something called stack. The stack is available to push values into, so that other classes may retrieve those values in the lifetime of the program. 
A good example is when an ArithmeticExp interprets a NumberExp, the NumberExp pushes its value to the stack, and then ArithmeticExp pops the stack in order to retrieve that value and use it.

Instead of dividing up bindings, start and statements into separate lists, I decided to put them all into a list called Interpretables (Couldn't come up with a better name), as this makes it easier to create the tests, and there is essentially no difference in how they are handled by the robot.


References to Robot
-------------------
most of the classes in robol need a reference to the Robot instance inside the program. 
The earliest prototype of the language took the robot as a parameter when creating an instance of a class that needed said reference.
This created a lot of headaches when it came to making the test programs, so I decided to take away the responsibility from the user by creating a private method in each class that contained class instances that needed references of the robot, and add it to them.
This made it a lot more user friendly, and also made it less likely to make mistakes when creating the tests.


Statements
----------
Statements usually modify the state of the robot, whether it's incrementing/decrementing a binding, turning the robot, or moving the robot. They behave about the same in the sense that they evaluate expressions, and then they modify the state of the robot.
Most of the classes here are built the same way, except for Loop, and Stop.
Stop just prints out the current position of the robot, but Loop is a bit more interesting.


Loop
----
Loop was pretty interesting to make, as you can think of it being like a small program inside the program. Although it doesn't have its own stack and bindings, it does have its own list of statements that work pretty much the same way as the statements list of robot.
Where this design lacks a little, is that if you declare any bindings inside the loop, they will be inserted into the robot's bindings dictionary, aka. it will be a global binding, instead of only living in the scope of the loop.

The reason I chose that Loop should have its own list of statements, is because it makes it more organized, so that you don't need to jump back a certain amount of statements of the robot's statements list for each iteration of the loop. This also makes nested loops possible.


Expression
----------
All expressions work the same. They interpet the expression given, and push the result up to the stack.
NumberExp and Identifier directly push the value given to the stack, while ArithmeticExp interprets the left and right side of the equation before performing the operation. Interpreting the left and right side before performing an operation makes NumberExp naturally recursive in nature, so you can nest multiple ArithmeticExp instances inside each other.


Enums
-----
There are parts of the code where there are comparissons, for example what binary operation is used in an arithmetic expression, and it's natural to express the different choices with enums to make the implementations of other classes more readable.

