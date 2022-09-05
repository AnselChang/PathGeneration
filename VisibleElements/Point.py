from Draggable import Draggable
from SingletonState.UserInput import UserInput
from SingletonState.ReferenceFrame import Ref, PointRef
import Utility, pygame

"""
Abstract class defined as a draggable point drawn on the screen
Implemented by PathPoint and ControlPoint
"""
class Point(Draggable):


    def __init__(self, hoverRadius: int, circleColor: tuple, drawRadius: int, drawRadiusBig: int):

        self.CIRCLE_COLOR = circleColor
        self.HOVER_RADIUS = hoverRadius
        self.DRAW_RADIUS = drawRadius
        self.DRAW_RADIUS_BIG = drawRadiusBig

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
    def draw(self, screen: pygame.Surface, position: tuple):

        # Draw PathPoint
        if self.isHovering:
            radius = self.DRAW_RADIUS_BIG
            color = Utility.scaleTuple(self.CIRCLE_COLOR, 0.85)
        else:
            radius = self.DRAW_RADIUS
            color = self.CIRCLE_COLOR
        Utility.drawCircle(screen, *position, color, radius)