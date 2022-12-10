from MouseInterfaces.Draggable import Draggable
from SingletonState.UserInput import UserInput
from SingletonState.ReferenceFrame import Ref, PointRef
import Utility, pygame, Graphics
from enum import Enum


"""
Abstract class defined as a draggable point drawn on the screen
Implemented by PathPoint and ControlPoint
"""
class Point(Draggable):


    def __init__(self, sectionIndex: int, hoverRadius: int, drawRadius: int, drawRadiusBig: int):

        self.HOVER_RADIUS = hoverRadius
        self.DRAW_RADIUS = drawRadius
        self.DRAW_RADIUS_BIG = drawRadiusBig

        self.section: int = sectionIndex

        super().__init__()

    # Implementing Hoverable
    # Check whether the mouse is hovering over object
    def checkIfHovering(self, mousePosition: PointRef, myPosition: PointRef) -> bool:
        return (mousePosition - myPosition).magnitude(Ref.SCREEN) <= self.HOVER_RADIUS

    # Implementing Draggable interface
    # This function should only be called when the mouse is hovering over this object and the mouse was just pressed
    def startDragging(self, userInput: UserInput):
        pass

    # Implementing Draggable interface
    # Called when the mouse has released the object
    def stopDragging(self):
        pass

    # Draw circle
    def draw(self, screen: pygame.Surface, position: tuple, color: tuple):

        if self.isHovering:
            radius = self.DRAW_RADIUS_BIG
            color = Utility.scaleTuple(color, 0.7 if self.isDragging else 0.85)
        else:
            radius = self.DRAW_RADIUS
        Graphics.drawCircle(screen, *position, color, radius)