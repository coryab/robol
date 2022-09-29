from abc import ABC, abstractmethod

class Robol(ABC):
    """ This is the interface that most classes inherit from.

    All the classes that implement neither a Statement nor an Expression,
    implement Robol.
    """

    @abstractmethod
    def interpret(self):
        pass


class Statement(Robol):
    """ An interface for Statements.

    Classes that implement the Statement interface, usually modify the state
    of a Robot instance.
    """
    
    @abstractmethod
    def interpret(self):
        pass


class Expression(Robol):
    """ An interface for expressions.

    Classes that implement the Expression interface, usually evaluate an
    expression, and then push that value to the stack of a Robot instance.
    """

    @abstractmethod
    def interpret(self):
        pass
