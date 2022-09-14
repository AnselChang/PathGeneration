from SingletonState.ReferenceFrame import PointRef, Ref
from VisibleElements.Point import Point, Shape
from SingletonState.UserInput import UserInput
from VisibleElements.ControlPoint import ControlPoint
import Utility, Graphics, colors, pygame

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

class PathPoint(Point):

    def __init__(self, spawnPosition: PointRef, spawnVector: tuple):
        self.position = spawnPosition
        self.transform = spawnPosition.transform
        self.controlA: ControlPoint = ControlPoint(self.transform, self, *spawnVector)
        self.controlB: ControlPoint = ControlPoint(self.transform, self, 0, 0)
        self.controlA.updateOtherVector()

        # By default, self.controlPositionA and self.controlPositionB are linked and the curve is continuous
        self.shape = Shape.SMOOTH

        super().__init__(hoverRadius = 20, drawRadius = 10, drawRadiusBig = 12)

    # Given one of the points, return the other one. Useful when called from one of the control points
    def other(self, control: ControlPoint) -> ControlPoint:
        if control is self.controlA:
            return self.controlB
        elif control is self.controlB:
            return self.controlA
        raise Exception("Given ControlPoint object not found in PathPoint")

    # Toggle the shape of the point (whether control points and synced and whether to point turn or curve)
    def toggleShape(self):
        if self.shape == Shape.SMOOTH:
            self.shape = Shape.SHARP
        else:
            self.shape = Shape.SMOOTH
            self.controlA.updateOtherVector()

    # Implementing Hoverable
    # Check whether the mouse is hovering over object
    def checkIfHovering(self, userInput: UserInput) -> bool:
        return super().checkIfHovering(userInput.mousePosition, self.position)

    # Implementing Draggable interface
    # Return if the point was actually moved
    def beDraggedByMouse(self, userInput: UserInput) -> bool:

        if userInput.isMouseOnField:
            self.position = userInput.mousePosition.copy()
            return True
        return False


    def draw(self, screen: pygame.Surface, index: int):

        position = self.position.screenRef
        color: tuple = colors.ORANGE if self.shape == Shape.SHARP else colors.GREEN
        super().draw(screen, position, color) # draw circle
        Graphics.drawText(screen, Graphics.FONT20, str(index), colors.BLACK, *position)


    def __str__(self):
        return "PathPoint with position {}".format(self.position)
