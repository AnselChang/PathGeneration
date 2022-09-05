from Draggable import Draggable
from SingletonState.UserInput import UserInput
from SingletonState.ReferenceFrame import Ref
import Utility

"""
Abstract class defined as a draggable point drawn on the screen
Implemented by PathPoint and ControlPoint
"""
class Point(Draggable):


    def __init__(self, hoverRadius: int):
        self.HOVER_RADIUS = hoverRadius
        super().__init__()

    # Implementing Draggable interface
    # This function should only be called when the mouse is hovering over this object and the mouse was just pressed
    def startDragging(self, userInput: UserInput):
        pass

    # Implementing Draggable interface
    # Called when the mouse has released the object
    def stopDragging(self):
        pass

