from Simulation.AbstractController import AbstractController
from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Sliders.Slider import Slider

from typing import Tuple

"""
A special controller, which is not user-configurable, specifically for point turns. Stored privately in Simulation.py
"""

class PointTurnController(AbstractController):
    
    # Not user-configurable, so return an empty list
    def defineParameterSliders(self) -> list[Slider]:
        return []

    # To be called at the start of a simulation. Sets waypoints and initial state
    def initSimulation(self, targetHeading: float):
        self.targetHeading: float = targetHeading

    # Simulate a point turn to self.targetHeading
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput, timestep: float) -> Tuple[RobotModelInput, bool]:
        pass