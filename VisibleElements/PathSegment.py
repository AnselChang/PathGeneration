
from VisibleElements.PathPoint import PathPoint
from SingletonState.UserInput import UserInput
from SingletonState.ReferenceFrame import PointRef, Ref
from Hoverable import Hoverable
import Utility, pygame

""" A class containing references to two PathPoint objects. The class stores hovered and dragging state, and handles
mouse detection and drawing the segment.
"""
class PathSegment(Hoverable):

    def __init__(self, pointA: PathPoint, pointB: PathPoint):

        super().__init__()

        self.pointA: PathPoint.PathPoint = pointA
        self.pointB: PathPoint.PathPoint = pointB

        self.SEGMENT_THICKNESS = 3
        self.SEGMENT_HITBOX_THICKNESS = 10

    def checkIfHovering(self, userInput: UserInput) -> bool:
        a = self.pointA.position.screenRef
        b = self.pointB.position.screenRef
        return Utility.pointTouchingLine(*userInput.mousePosition.screenRef, *a, *b, self.SEGMENT_HITBOX_THICKNESS)

    def draw(self, screen: pygame.Surface):
        # Line becomes thicker and darker if hovered
        color = Utility.LINEDARKGREY if self.isHovering else Utility.LINEGREY

        # Draw line from position A to B
        Utility.drawLine(screen, color, *self.pointA.position.screenRef, *self.pointB.position.screenRef, self.SEGMENT_THICKNESS)
