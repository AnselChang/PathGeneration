
import VisibleElements.PathPoint as PathPoint, SingletonState.ReferenceFrame as ReferenceFrame, Draggable, Utility, pygame

""" A class containing references to two PathPoint objects. The class stores hovered and dragging state, and handles
mouse detection and drawing the segment.
"""
class PathSegment(Draggable.Draggable):

    def __init__(self, pointA: PathPoint.PathPoint, pointB: PathPoint.PathPoint):
        self.pointA: PathPoint.PathPoint = pointA
        self.pointB: PathPoint.PathPoint = pointB

        self.SEGMENT_THICKNESS = 3
        self.SEGMENT_HITBOX_THICKNESS = 10

    def isTouchingMouse(self, mousePosition: ReferenceFrame.PointRef):
        a = self.pointA.position.screenRef
        b = self.pointB.position.screenRef
        return Utility.pointTouchingLine(*mousePosition.screenRef, *a, *b, self.SEGMENT_HITBOX_THICKNESS)

    def draw(self, screen: pygame.Surface):
        # Line becomes thicker and darker if hovered
        if self.hoveringSegment is not None and index == self.hoveringSegment.index:
            color = Utility.LINEDARKGREY
        else:
            color = Utility.LINEGREY

        # Draw line from position A to B
        Utility.drawLine(screen, color, *self.pointA.position.screenRef, *self.pointB.position.screenRef, self.SEGMENT_THICKNESS)
