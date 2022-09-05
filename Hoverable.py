from abc import ABC, abstractmethod
from SingletonState.UserInput import UserInput

"""
Python "interface" for all hoverable objects. These are objects in which, when the mouse is "hovered" over it, has some
change in state, which could be expressed in a visual change, or even the ability to drag the object around (Draggable)

To manage all Hoverable objects, they will be stored in a list (not in this file) and collectively parsed.
"""
class Hoverable(ABC):

    def __init__(self):
        self.isHovering = False

    # Called at the beginning of each frame to reset the isHovering attribute
    def resetHoverableObject(self):
        self.isHovering = False
    
    # Called when a hovered object has been found
    def setHoveringObject(self):
        self.isHovering = True

    # Called to determine if the mouse is touching this object (and if is the first object touched, would be considered hovered)
    @abstractmethod
    def checkIfHovering(self, userInput: UserInput) -> bool:
        pass