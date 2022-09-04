import SingletonState.FieldTransform as FieldTransform, VisibleElements.PathPoint as PathPoint, SingletonState.ReferenceFrame as ReferenceFrame, Draggable

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

    # When the location of this control point has moved, update the other control point also associated with the PathPoint
    def updateOtherVector(self):
        other: ControlPoint = self.parent.other