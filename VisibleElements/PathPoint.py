from SingletonState.ReferenceFrame import PointRef, Ref
from VisibleElements.Point import Point
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

    def __init__(self, spawnPosition: PointRef, spawnVector: tuple, section):

        super().__init__(section, hoverRadius = 20, drawRadius = 10, drawRadiusBig = 12)

        self.position = spawnPosition
        self.controlA: ControlPoint = ControlPoint(self, *spawnVector)
        self.controlB: ControlPoint = ControlPoint(self, 0, 0)
        self.controlA.updateOtherVector()


        

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
        return super().checkIfHovering(userInput.mousePosition, self.position)

    # Implementing Draggable interface
    # Return if the point was actually moved
    def beDraggedByMouse(self, userInput: UserInput) -> bool:

        if userInput.isMouseOnField:
            self.position = userInput.mousePosition.copy()
            return True
        return False


    def draw(self, screen: pygame.Surface, label = None):

        position = self.position.screenRef
        super().draw(screen, position, colors.GREEN) # draw circle
        if label is not None:
            Graphics.drawText(screen, Graphics.FONT20, str(label), colors.BLACK, *position)


    def __str__(self):
        return "PathPoint with position {}".format(self.position)
