from enum import Enum
import PointRef, FieldTransform, Utility, Draggable, pygame

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

# Specifying which of the three points in a PathPoint object. Used only internally in this module
class _Type(Enum):
    PATH_POINT = 1
    CONTROL_A = 2
    CONTROL_B = 3
    NONE = 4

class PathPoint(Draggable.Draggable):

    def __init__(self, spawnPosition: PointRef.PointRef):
        self.position = spawnPosition
        self.transform = spawnPosition.transform
        self.controlPositionA = PointRef.translateByVector(spawnPosition, (5,5), PointRef.Ref.FIELD)
        self.controlPositionB = None
        self._syncControlBFromA()

        # By default, self.controlPositionA and self.controlPositionB are linked and the curve is continuous
        self.shape = Shape.SMOOTH

        self.pointHovered = None # either PathPoint, controlA, or controlB being hovered over
        self.pointDragged = _Type.NONE # either PathPoint, controlA, or controlB being dragged

        self.DRAW_RADIUS = 10 # in pixels
        self.HOVER_RADIUS = 13 # in pixels

    #def draw(self, screen)

    # Check whether the mouse is hovering over one of the three points in this object
    # Additionally, store internal state as to which point it is hovering
    def checkMouseHovering(self, mousePosition: PointRef.PointRef) -> bool:

        def closeToMouse(position: PointRef.PointRef):
            return Utility.distanceTuple(mousePosition.subtract(position, PointRef.Ref.SCREEN)) <= self.HOVER_RADIUS # in pixels

        if closeToMouse(self.position):
             # hovering over PathPoint
            self.pointHovered = _Type.PATH_POINT
            return True
        elif closeToMouse(self.controlPositionA):
            # hovering over control A
            self.pointHovered = _Type.CONTROL_A
            return True
        elif closeToMouse(self.controlPositionB):
             # hovering over control B
             self.pointHovered = _Type.CONTROL_B
             return True
        else:
            self.pointHovered = None
            return False

    # Implementing Draggable interface
    # Now that the object is being dragged, specify that point being dragged
    # This function should only be called when the mouse is hovering over this object and the mouse was just pressed
    def startDragging(self, mousePosition: PointRef.PointRef):
        if self.pointHovered is None:
            raise Exception("Error: trying to drag an nonexistent object.")

        # At the moment, the object will simply "snap" to the mouse when dragging it. If we want to drag the object
        # relative to where the mouse clicked the object, we'd need to store the starting mouse position here
        self.pointDragged = self.pointHovered


    # Implementing Draggable interface
    # Called when the mouse has released the object
    def stopDragging(self):
        self.pointDragged = None

    # Implementing Draggable interface
    # Check which of the three points in the object is being dragged, and change its position accordingly
    def beDraggedByMouse(self, mousePosition: PointRef.PointRef):

        if self.pointDragged == _Type.NONE:
            # At this point, SoftwareState is indicating this object is being dragged, but this object disagrees.
            # This should be impossible; it is guaranteed a bug exists somewhere...
            raise Exception("Error: unsure if object is being dragged.")
        
        # Clamp position to within the bounds of the field
        newPos = Utility.clamp2D(mousePosition.fieldRef, 0, 0, Utility.FIELD_SIZE_IN_INCHES, Utility.FIELD_SIZE_IN_INCHES)
        newPoint = PointRef.PointRef(self.transform, PointRef.Ref.FIELD, newPos)
        
        if self.pointDragged == _Type.PATH_POINT:

            # Move PathPoint, controlA, and controlB at the same time since controlA and controlB are attached to PathPoint
            delta = newPoint.subtract(self.position, PointRef.Ref.FIELD) # get how much PathPoint will move
            self.position = newPoint
            self.controlPositionA.addInPlace(delta, PointRef.Ref.FIELD)
            self.controlPositionB.addInPlace(delta, PointRef.Ref.FIELD)

        elif self.pointDragged == _Type.CONTROL_A:

            # If shape is smooth, dragging control A also affects B. Otherwise, it affects only control A
            self.controlPositionA = newPoint
            if self.shape == Shape.SMOOTH:
                self._syncControlBFromA()

        else: # self.pointDragged == _Type.CONTROL_B

            # If shape is smooth, dragging control B also affects A. Otherwise, it affects only control B
            self.controlPositionB = newPoint
            if self.shape == Shape.SMOOTH:
                self._syncControlAFromB()

    # Given an updated control position B, update control position A to be directly opposite across self.position
    def _syncControlAFromB(self):
        # Perform all actions under field reference frame, though it's aribtrary which one to use
        bx, by = self.controlPositionB.fieldRef
        px, py = self.position.fieldRef
        newAPosition = px - (bx - px), py - (by - py)
        self.controlPositionB = PointRef.PointRef(self.transform, PointRef.Ref.FIELD, newAPosition)

    # Given an updated control position A, update control position B to be directly opposite across self.position
    def _syncControlBFromA(self):
        # Perform all actions under field reference frame, though it's aribtrary which one to use
        ax, ay = self.controlPositionA.fieldRef
        px, py = self.position.fieldRef
        newBPosition = px - (ax - px), py - (ay - py)
        self.controlPositionB = PointRef.PointRef(self.transform, PointRef.Ref.FIELD, newBPosition)

    def draw(self, screen: pygame.Surface):
        Utility.drawCircle(screen, *self.position.screenRef, Utility.GREEN, self.DRAW_RADIUS)

    def __str__(self):
        return "PathPoint with position {}".format(self.position)