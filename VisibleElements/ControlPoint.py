from re import U
from SingletonState.FieldTransform import FieldTransform
from SingletonState.UserInput import UserInput
from VisibleElements.Point import Point
from SingletonState.ReferenceFrame import VectorRef, Ref
import Utility, pygame

"""
A control point is associated with a PathPoint and determines the beizer curve shape about that point
Each PathPoint contains a reference to the two controlPoints. If the shape is set to smooth, the two control
points are linked.
"""

class ControlPoint(Point):

    # delta x and delta y from PathPoint in inches
    def __init__(self, pathTransform: FieldTransform, parent, deltaX: float, deltaY: float):
        self.transform = pathTransform
        self.parent = parent
        self.vector = VectorRef(self.transform, Ref.FIELD, (deltaX, deltaY))
        
        self.DRAW_RADIUS = 5
        super().__init__(hoverRadius = 10, circleColor = Utility.BLUE, drawRadius = 5, drawRadiusBig = 6)

    # When the location of this control point has moved, update the other control point also associated with the PathPoint
    # pathPoint.controlA = 0 - pathPoint.controlB (opposite sides of pathPoint)
    def updateOtherVector(self):
        self.parent.other(self).vector.fieldRef = Utility.subtractTuples((0,0), self.vector.fieldRef)

    # Implementing Hoverable
    # Check whether the mouse is hovering over object
    def checkIfHovering(self, userInput: UserInput) -> bool:

        return (userInput.mousePosition - (self.parent.position+self.vector)).magnitude(Ref.SCREEN) <= self.HOVER_RADIUS

    # Implementing Draggable interface
    # Set position to be vector going from the parent point to the mouse
    def beDraggedByMouse(self, userInput: UserInput):
        if userInput.isMouseOnField:
            self.vector = (userInput.mousePosition - self.parent.position)

    def drawOwnershipLine(self, screen: pygame.Surface):

        # store position as an instance variable to be access by self.draw() after PathPoint is drawn
        self.cachePosition = (self.parent.position + self.vector).screenRef

        # Draw line to parent to show ownership
        Utility.drawThinLine(screen, self.CIRCLE_COLOR, *self.cachePosition, *self.parent.position.screenRef)

    def draw(self, screen: pygame.Surface):
        
        # Draw circle
        super().draw(screen, self.cachePosition)

    def __str__(self):
        return "Control Point, {}".format(self.isHovering)