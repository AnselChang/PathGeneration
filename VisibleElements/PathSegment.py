
from VisibleElements.PathPoint import PathPoint
from SingletonState.UserInput import UserInput
from SingletonState.ReferenceFrame import PointRef, Ref
from MouseInterfaces.Hoverable import Hoverable
import Utility, colors, Graphics, pygame

""" A class containing references to two PathPoint objects. The class stores hovered and dragging state, and handles
mouse detection and drawing the segment.
"""
class PathSegment(Hoverable):

    def __init__(self, pointA: PathPoint, pointB: PathPoint, section):

        super().__init__()

        self.pointA: PathPoint.PathPoint = pointA
        self.pointB: PathPoint.PathPoint = pointB

        self.SEGMENT_THICKNESS = 3
        self.SEGMENT_HITBOX_THICKNESS = 10

        self.section = section

    # Check whether mouse is near the segment using a little math
    def checkIfHovering(self, userInput: UserInput) -> bool:
        a = self.pointA.position.screenRef
        b = self.pointB.position.screenRef
        return Utility.pointTouchingLine(*userInput.mousePosition.screenRef, *a, *b, self.SEGMENT_HITBOX_THICKNESS)

    def draw(self, screen: pygame.Surface):
        # Line becomes thicker and darker if hovered
        color = colors.LINEDARKGREY if self.isHovering else colors.LINEGREY

        # Draw line from position A to B
        Graphics.drawLine(screen, color, *self.pointA.position.screenRef, *self.pointB.position.screenRef, self.SEGMENT_THICKNESS)
