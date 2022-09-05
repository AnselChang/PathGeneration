from enum import Enum
from SingletonState.ReferenceFrame import PointRef, Ref
from VisibleElements.Point import Point
from SingletonState.UserInput import UserInput
from VisibleElements.ControlPoint import ControlPoint
import Utility, pygame

"""PathPoint objects are user-controllable points that consist of a main control point that is on the path, and 
two "control" points not on  the actual path, in order to specify angle.

In this implementation, a PathPoint is the owner of two control points, and the position of two control points are
defined relative to the location of the PathPoint.
A PathPoint can be toggled to either SMOOTH or SHARP, with SHARP implying a point turn at that point instead
of following a continouous beizer curve. When SMOOTH, the two control points are linked as two opposite vectors relative
from PathPoint.
The location of the PathPoint itself and the two control points are stored as PointRefs. But, moving the PathPoint
by some delta will also shift the control points the same amount.
"""

class Shape(Enum):
    SMOOTH = 1
    SHARP = 2


class PathPoint(Point):

    def __init__(self, spawnPosition: PointRef):
        self.position = spawnPosition
        self.transform = spawnPosition.transform
        self.controlA: ControlPoint = ControlPoint(self.transform, self, 5, 5)
        self.controlB: ControlPoint = ControlPoint(self.transform, self, -5, -5)

        # By default, self.controlPositionA and self.controlPositionB are linked and the curve is continuous
        self.shape = Shape.SMOOTH

        self.DRAW_RADIUS = 10 # in pixels
        self.DRAW_RADIUS_HOVER_MUTLIPLIER = 1.15
        super().__init__(hoverRadius = 20)

    # Given one of the points, return the other one. Useful when called from one of the control points
    def other(self, control: ControlPoint) -> ControlPoint:
        if control is self.controlA:
            return self.controlB
        elif control is self.controlB:
            return self.controlA
        raise Exception("Given ControlPoint object not found in PathPoint")

    # Implementing Hoverable
    # Check whether the mouse is hovering over object
    def checkIfHovering(self, userInput: UserInput) -> bool:

        return (userInput.mousePosition - self.position).magnitude(Ref.SCREEN) <= self.HOVER_RADIUS

    # Implementing Draggable interface
    def beDraggedByMouse(self, userInput: UserInput):

        if userInput.isMouseOnField:
            self.position = userInput.mousePosition.copy()


    def draw(self, screen: pygame.Surface, index: int):

        # Draw PathPoint
        color = Utility.GREEN
        if self.isHovering:
            radius = self.DRAW_RADIUS_HOVER_MUTLIPLIER * self.DRAW_RADIUS 
            color = Utility.scaleTuple(Utility.GREEN, 0.85)
        else:
            radius = self.DRAW_RADIUS
            color = Utility.GREEN
        position = self.position.screenRef
        Utility.drawCircle(screen, *position, color, radius)
        Utility.drawText(screen, Utility.FONT20, str(index), Utility.BLACK, *position)

        self.controlA.draw(screen)
        self.controlB.draw(screen)

    def __str__(self):
        return "PathPoint with position {}".format(self.position)