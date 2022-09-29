from abc import ABC, abstractmethod

class Robol(ABC):
    """ This is the interface that most classes inherit from."""

    @abstractmethod
    def interpret(self):
        raise NotImplementedError("interpret method is not implemented")


class Statement(Robol):
    """ An interface for Statements."""
    
    @abstractmethod
    def interpret(self):
        pass



class Expression(Robol):
    """ An interface for expressions."""

    @abstractmethod
    def interpret(self):
        pass
