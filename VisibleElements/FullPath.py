from SingletonState.ReferenceFrame import PointRef, Ref
from SingletonState.SoftwareState import SoftwareState, Mode
from VisibleElements.PathPoint import PathPoint
from VisibleElements.PathSection import PathSection
from VisibleElements.PathSegment import PathSegment
import BezierCurves, Utility, colors, pygame, Graphics
from typing import Tuple


"""Store the full path of the robot. This consists of a list of PathPoint objects, as well as the interpolatedPoint objects
that would be generated as a bezier curve through all the PathPoints. The interpolatedPoints array will be recalculated at each
PathPoint change."""


class FullPath:

    def __init__(self):
        self.sections: list[PathSection] = []

        self.currentSection = 0

    def isEmptyInterpolated(self) -> bool:
        if len(self.sections) == 0:
            return True
        for section in self.sections:
            if len(section.waypoints) < 2:
                return True
        return False

    def getSegmentIndex(self, segment: PathSegment) -> Tuple[int, int]:
        for i in range(len(self.sections)):
            for j in range(len(self.sections[i].segments)):
                if self.sections[i].segments[j] is segment:
                    return i, j
                
    def getPathPointIndex(self, pathPoint: PathPoint) -> Tuple[int, int]:
        for i in range(len(self.sections)):
            for j in range(len(self.sections[i].pathPoints)):
                if self.sections[i].pathPoints[j] is pathPoint:
                    return i, j

    def createPathPoint(self, position: PointRef, sectionIndex: int, index: int = -1):
        self.sections[sectionIndex].createPathPoint(position, index)
        

    def createSection(self, position: PointRef):
        self.currentSection = len(self.sections)
        self.sections.append(PathSection(self.currentSection))
        self.createPathPoint(position, self.currentSection)
        
    # Delete a path point given the point object. Finds and deletes the segment as well
    def deletePathPoint(self, point: PathPoint):
        sectionIndex, pathPointIndex = self.getPathPointIndex(point)
        isDeleteSection: bool = self.sections[sectionIndex].deletePathPoint(point)
        if isDeleteSection:

            del self.sections[sectionIndex]
            for i in range(sectionIndex, len(self.sections)):
                self.sections[i].sectionIndex -= 1
            self.currentSection = len(self.sections) - 1
        else:
            self.sections[sectionIndex].calculateInterpolatedPoints()


    # Draw a segment from each path to the next. This will be drawn under the points themselves
    def drawPathSegments(self, screen: pygame.Surface):
        
        for section in self.sections:
            section.drawPathSegments(screen)

    # Iterate through each PathPoint and draw it
    def drawPathPoints(self, screen: pygame.Surface, drawControl: bool):
        for section in self.sections:
            section.drawPathPoints(screen, drawControl)

    # Draw all the interpolated points that have been calculated from PathPoint and ControlPoints
    def drawInterpolatedPoints(self, screen: pygame.Surface):

        for section in self.sections:
            section.drawInterpolatedPoints(screen)

    # Draw the path on the screen, including the user-defined points, interpolated points, and segments
    def draw(self, screen: pygame.Surface, state: SoftwareState):
        
        # Draw ControlPoints only in Edit mode
        drawControl = (state.mode == Mode.EDIT)

        # Pointless for segments to be shown in PLAY mode, so draw only in Edit mode
        if drawControl:
            self.drawPathSegments(screen)
        
        self.drawInterpolatedPoints(screen)
        self.drawPathPoints(screen, drawControl)
    