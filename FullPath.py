
import PathPoint, PointRef


"""Store the full path of the robot. This consists of a list of PathPoint objects, as well as the interpolatedPoint objects
that would be generated as a bezier curve through all the PathPoints. The interpolatedPoints array will be recalculated at each
PathPoint change."""

class FullPath:

    def __init__(self):
        self.pathPoints: list[PathPoint.PathPoint] = [] # The user-defined points
        self.interpolatedPoints: list[PointRef.PointRef] = [] # the beizer-interpolated points generated from the user-defined points

    # Return the PathPoint object that the mouse is hovering on, simply by iterating through the array asking each object
    # if it is being hovered. Return None if no such object exists
    def getMouseHoveringPoint(self, mousePosition: PointRef.PointRef) -> PathPoint.PathPoint:

        for pathPoint in self.pathPoints:
            if pathPoint.checkMouseHovering(mousePosition):
                return pathPoint
        return None

    