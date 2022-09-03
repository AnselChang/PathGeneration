
import PathPoint, PointRef, Utility, pygame


"""Store the full path of the robot. This consists of a list of PathPoint objects, as well as the interpolatedPoint objects
that would be generated as a bezier curve through all the PathPoints. The interpolatedPoints array will be recalculated at each
PathPoint change."""

class Segment:
    def __init__(self, index: int):
        self.index = index

class FullPath:

    def __init__(self):
        self.pathPoints: list[PathPoint.PathPoint] = [] # The user-defined points
        self.interpolatedPoints: list[PointRef.PointRef] = [] # the beizer-interpolated points generated from the user-defined points

        self.hoveringSegment = None

        self.SEGMENT_THICKNESS = 3
        self.SEGMENT_HITBOX_THICKNESS = 10

    # Return the PathPoint object that the mouse is hovering on, simply by iterating through the array asking each object
    # if it is being hovered. Return None if no such object exists
    def getMouseHoveringPoint(self, mousePosition: PointRef.PointRef) -> PathPoint.PathPoint:

        for pathPoint in self.pathPoints:
            if pathPoint.checkMouseHovering(mousePosition):
                return pathPoint
        return None

    # Return the Segment object that the mouse is hovering on, which is just a thin wrapper for the segment index
    def getMouseHoveringSegment(self, mousePosition: PointRef.PointRef) -> Segment:

        # No segments for paths with under two points
        if (len(self.pathPoints) < 2):
            return None

        index = 0
        positionA = self.pathPoints[0].position.screenRef
        for point in self.pathPoints[1:]:
            positionB = point.position.screenRef

            # Check for mouse intersection with segment
            if Utility.pointTouchingLine(*mousePosition.screenRef, *positionA, *positionB, self.SEGMENT_HITBOX_THICKNESS):
                self.hoveringSegment = Segment(index)
                return self.hoveringSegment

            positionA = positionB
            index += 1

        # no segment found
        self.hoveringSegment = None
        return None

    # Append a PathPoint at the end of the path at the specified position
    def createPathPoint(self, position: PointRef.PointRef):
        self.pathPoints.append(PathPoint.PathPoint(position.copy()))

    # Draw a segment from each path to the next. This will be drawn under the points themselves
    def drawPathSegments(self, screen: pygame.Surface):
        
        # No segments for paths with under two points
        if len(self.pathPoints) < 2:
            return
        
        index = 0
        positionA = self.pathPoints[0].position.screenRef
        for point in self.pathPoints[1:]:
            positionB = point.position.screenRef

            # Line becomes thicker and darker if hovered
            if self.hoveringSegment is not None and index == self.hoveringSegment.index:
                color = Utility.LINEDARKGREY
            else:
                color = Utility.LINEGREY

            # Draw line from position A to B
            Utility.drawLine(screen, color, *positionA, *positionB, self.SEGMENT_THICKNESS)

            index += 1
            positionA = positionB

    # Iterate through each PathPoint and draw it
    def drawPathPoints(self, screen: pygame.Surface):
        index = 0
        for pathPoint in self.pathPoints:
            pathPoint.draw(screen, index)
            index += 1

    # Draw the path on the screen, including the user-defined points, interpolated points, and segments
    def draw(self, screen: pygame.Surface):
        self.drawPathSegments(screen)
        self.drawPathPoints(screen)
    