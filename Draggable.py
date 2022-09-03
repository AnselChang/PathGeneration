from abc import ABC, abstractmethod
import PointRef

"""Python "Interface" for objects that are draggable by the mouse. This adds a layer of abstraction with the mouse
able to store which object is being dragged without knowing its exact type, only that it is draggable.

Useful for example for PathPoints and Sliders."""

class Draggable(ABC):

    # Callback when the object was just pressed at the start of a drag
    @abstractmethod
    def startDragging(self, mousePosition: PointRef.PointRef):
        pass

    # Called every frame that the object is being dragged. Most likely used to update the position of the object based
    # on where the mouse is
    @abstractmethod
    def beDraggedByMouse(self, mousePosition: PointRef.PointRef):
        pass

    # Callback when the dragged object was just released
    @abstractmethod
    def stopDragging(self):
        pass