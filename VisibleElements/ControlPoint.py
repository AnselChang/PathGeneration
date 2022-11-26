from re import U
from SingletonState.FieldTransform import FieldTransform
from SingletonState.UserInput import UserInput
from VisibleElements.Point import Point
from SingletonState.ReferenceFrame import VectorRef, Ref
import Utility, colors, pygame, Graphics

"""
A control point is associated with a PathPoint and determines the beizer curve shape about that point
Each PathPoint contains a reference to the two controlPoints. If the shape is set to smooth, the two control
points are linked.
"""

class ControlPoint(Point):

    # delta x and delta y from PathPoint in inches
    def __init__(self, parent, deltaX: float, deltaY: float):
        self.parent = parent
        self.vector = VectorRef(Ref.FIELD, (deltaX, deltaY))
        
        self.DRAW_RADIUS = 5
        super().__init__(parent.section, hoverRadius = 10, drawRadius = 5, drawRadiusBig = 6)

    # When the location of this control point has moved, update the other control point also associated with the PathPoint
    # pathPoint.controlA = 0 - pathPoint.controlB (opposite sides of pathPoint)
    def updateOtherVector(self):
        self.parent.other(self).vector.fieldRef = Utility.subtractTuples((0,0), self.vector.fieldRef)

    # Implementing Hoverable
    # Check whether the mouse is hovering over object
    def checkIfHovering(self, userInput: UserInput) -> bool:

        return super().checkIfHovering(userInput.mousePosition, self.parent.position + self.vector)

    # Implementing Draggable interface
    # Set position to be vector going from the parent point to the mouse
    # Return whether it has been moved
    def beDraggedByMouse(self, userInput: UserInput) -> bool:
        if userInput.isMouseOnField:
            self.vector: VectorRef = (userInput.mousePosition - self.parent.position)

            # Prevent vector from being too small (div by 0 errors) by mandating minimum magnitude
            MIN_MAGNITUDE = 1 # mininum magnitude of vector in inches
            mag = self.vector.magnitude(Ref.FIELD)
            if mag == 0:
                self.vector.fieldRef = (MIN_MAGNITUDE,0) # default vector is pointing to right
            elif mag < MIN_MAGNITUDE:
                self.vector *= (MIN_MAGNITUDE / mag) # scale self.vector magnitude to MIN_MAGNITUDE

            # If we're in continuous mode, we need to keep both control points opposite one another
            if True:
                self.updateOtherVector()

            return True

        return False

    # Draw a line from the ControlPoint to the PathPoint as a visual indication of what PathPoint the ControlPoint belongs to
    def drawOwnershipLine(self, screen: pygame.Surface):

        # store position as an instance variable to be access by self.draw() after PathPoint is drawn
        self.cachePosition = (self.parent.position + self.vector).screenRef

        # Draw line to parent to show ownership
        Graphics.drawThinLine(screen, colors.BLUE, *self.cachePosition, *self.parent.position.screenRef)

    def draw(self, screen: pygame.Surface):
        
        # Draw circle
        super().draw(screen, self.cachePosition, colors.BLUE)

    def __str__(self):
        return "Control Point, {}".format(self.isHovering)