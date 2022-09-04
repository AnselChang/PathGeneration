import SingletonState.FieldTransform as FieldTransform, VisibleElements.PathPoint as PathPoint, SingletonState.ReferenceFrame as ReferenceFrame
import Draggable, Utility, pygame

"""
A control point is associated with a PathPoint and determines the beizer curve shape about that point
Each PathPoint contains a reference to the two controlPoints. If the shape is set to smooth, the two control
points are linked.
"""

class ControlPoint(Draggable.Draggable):

    # delta x and delta y from PathPoint in inches
    def __init__(self, pathTransform: FieldTransform.FieldTransform, parent: PathPoint.PathPoint, deltaX: float, deltaY: float):
        self.transform = pathTransform
        self.parent: PathPoint.PathPoint = parent
        self.vector = ReferenceFrame.VectorRef(self.transform, ReferenceFrame.Ref.FIELD, (deltaX, deltaY))
        
        self.DRAW_RADIUS = 5

    # When the location of this control point has moved, update the other control point also associated with the PathPoint
    # pathPoint.controlA = 0 - pathPoint.controlB (opposite sides of pathPoint)
    def updateOtherVector(self):
        self.parent.other(self).vector.fieldRef = Utility.subtractTuples((0,0), self.vector.fieldRef)

    def draw(self, screen: pygame.Surface):
        absolutePosition = (self.parent.position + self.vector).screenRef
        Utility.drawCircle(screen, *absolutePosition, Utility.BLUE, self.DRAW_RADIUS)