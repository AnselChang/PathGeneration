from abc import ABC, abstractmethod
from Hoverable import Hoverable
from SingletonState.UserInput import UserInput

"""Python "Interface" for objects that are draggable by the mouse. This adds a layer of abstraction with the mouse
able to store which object is being dragged without knowing its exact type, only that it is draggable.

This is a abstract subclass of Hoverable, meaning that all Draggable objects are Hoverable

Useful for FieldTransform, PathPoint, and Slider."""

class Draggable(Hoverable.Hoverable):

    def __init__(self):
        super().__init__()

    # Called when the object was just pressed at the start of a drag
    @abstractmethod
    def startDragging(self, userInput: UserInput):
        pass

    # Called every frame that the object is being dragged. Most likely used to update the position of the object based
    # on where the mouse is
    @abstractmethod
    def beDraggedByMouse(self, userInput: UserInput):
        pass

    # Callback when the dragged object was just released
    @abstractmethod
    def stopDragging(self):
        pass