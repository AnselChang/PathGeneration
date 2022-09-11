from Simulation.AbstractController import AbstractController
from Simulation.Waypoints import Waypoints
from Simulation.RobotState import RobotState

"""
The ideal controller that simply is equal to a waypoint at each timestep. Completely unrealistic but useful to
animate the generated path itself.
"""

class IdealController(AbstractController):

    # Map each waypoint to a new timestep
    def simulateAlgorithm(self, waypoints: Waypoints) -> list[RobotState]:

        pass