from SingletonState.ReferenceFrame import PointRef

"""
Essentially a glorified list of list of PointRefs.
The list of PointRefs are a set of waypoints that are calculated by PointRefs
Between each set of waypoints is a point turn
"""

class Waypoints:

    def __init__(self):
        self.reset()

    # Clear the entire list of waypoints
    def reset(self):
        self.waypoints: list[list[PointRef]] = [[]]
        self.size = 0

    # get the index of the waypoint, "unboxing" the 2d list
    def get(self, index: int) -> PointRef:
        listIndex = 0

         # while the index exceeds the size of the current list, go on to the next list
        while len(self.waypoints[listIndex]) <= index and index >= 0:
            index -= len(self.waypoints[listIndex])
            listIndex += 1

        if index < 0:
            return None
        else:
            return self.waypoints[listIndex][index]


    # Whenever a new waypoint is calculated, append it to the last set of waypoints
    def addWaypoint(self, waypoint: PointRef):
        self.waypoints[-1].append(waypoint)
        self.size += 1

    # This happens when we reach a "Sharp" PathPoint. In this case, we want a point turn to happen
    # We store this by adding a new element to waypoints
    # The actual amount to turn is calculated later
    def addPointTurn(self):
        self.waypoints.append([])

    # Return an iterator through every single waypoint
    def iterator(self):

        for segment in self.waypoints:
            for waypoint in segment:
                yield waypoint

        # Weird python quirk to return empty iterator if self.waypoints is empty
        return
        yield