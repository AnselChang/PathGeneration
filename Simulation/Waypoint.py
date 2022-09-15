from SingletonState.ReferenceFrame import PointRef
"""
An interpolated point but with more information like curvature
Gets calculated in InterpolatedPoints.convertToWaypoints() which gets called in Simulation()
"""

class Waypoint:

    def __init__(self, position: PointRef, heading: float, curvature: float):

        self.position: PointRef = position
        self.heading = heading
        self.curvature = curvature