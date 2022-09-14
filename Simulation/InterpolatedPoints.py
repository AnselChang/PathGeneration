from SingletonState.ReferenceFrame import PointRef
from Simulation.Waypoint import Waypoint

"""
Essentially a glorified list of list of PointRefs.
The list of PointRefs are a set of waypoints that are calculated by PointRefs
Between each set of waypoints is a point turn
"""

class InterpolatedPoints:

    def __init__(self):
        self.reset()

    # Clear the entire list of waypoints
    def reset(self):
        self.points: list[list[PointRef]] = [[]]
        self.size = 0

    # get the index of the waypoint, "unboxing" the 2d list
    def get(self, index: int) -> PointRef:
        listIndex = 0

         # while the index exceeds the size of the current list, go on to the next list
        while len(self.points[listIndex]) <= index and index >= 0:
            index -= len(self.points[listIndex])
            listIndex += 1

        if index < 0:
            return None
        else:
            return self.points[listIndex][index]


    # Whenever a new interpolated point is calculated, append it to the last set of waypoints
    def addPoint(self, waypoint: PointRef):
        self.points[-1].append(waypoint)
        self.size += 1

    # This happens when we reach a "Sharp" PathPoint. In this case, we want a point turn to happen
    # We store this by adding a new element to interpolatedPOints
    # The actual amount to turn is calculated later
    def addPointTurn(self):
        self.points.append([])

    # Return an iterator through every single point
    def iterator(self):

        for segment in self.points:
            for waypoint in segment:
                yield waypoint

        # Weird python quirk to return empty iterator if self.points is empty
        return
        yield

    # Preprocess points with more information for simulation. Returns a list of list of waypoints
    def convertToWaypoints(self) -> list[list[Waypoint]]:
        #TODO
        pass