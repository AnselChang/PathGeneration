from abc import ABC, abstractmethod
import PointRef

class Draggable(ABC):

    # Every draggable object must implement this to be able to be dragged by (have their position affected by) the mouse
    @abstractmethod
    def beDraggedByMouse(self, mousePosition: PointRef.PointRef):
        pass
