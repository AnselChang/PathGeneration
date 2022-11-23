from abc import ABC, abstractmethod
from MouseInterfaces.Hoverable import Hoverable
from SingletonState.UserInput import UserInput

"""Python "Interface" for objects that are draggable by the mouse. This adds a layer of abstraction with the mouse
able to store which object is being dragged without knowing its exact type, only that it is draggable.

This is a abstract subclass of Hoverable, meaning that all Draggable objects are Hoverable

Useful for FieldTransform, PathPoint, and Slider."""

class Draggable(Hoverable):

    def __init__(self):
        super().__init__()
        self.isDragging = False

    # Call the implemented startDragging method, but first set the isDragging state
    def _startDragging(self, userInput: UserInput):
        self.isDragging = True
        self.startDragging(userInput)

    # Called when the object was just pressed at the start of a drag
    @abstractmethod
    def startDragging(self, userInput: UserInput):
        pass

    # Called every frame that the object is being dragged. Most likely used to update the position of the object based
    # on where the mouse is
    @abstractmethod
    def beDraggedByMouse(self, userInput: UserInput):
        pass

    # Call the implemented startDragging method, but first set the isDragging state
    def _stopDragging(self):
        self.isDragging = False
        self.stopDragging()

    # Callback when the dragged object was just released
    @abstractmethod
    def stopDragging(self):
        pass