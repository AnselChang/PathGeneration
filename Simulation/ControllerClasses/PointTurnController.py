from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from RobotSpecs import RobotSpecs
from Sliders.Slider import Slider

from typing import Tuple

"""
A special controller, which is not user-configurable and not part of the ControllerManager list, 
specifically for point turns. Stored privately in Simulation.py
"""

class PointTurnController(AbstractController):

    def __init__(self):
        super().__init__("Point Turns")
    
    # Not user-configurable, so return an empty list
    def defineParameterSliders(self) -> list[Slider]:
        return []

    # To be called at the start of a simulation. Sets waypoints and initial state
    def initSimulation(self, robotSpecs: RobotSpecs, targetHeading: float):
        self.robotSpecs = robotSpecs
        self.targetHeading: float = targetHeading

    # nothing else needed to init
    def initController(self):
        pass

    # Simulate a point turn to self.targetHeading
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        pass