from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState
from RobotSpecs import RobotSpecs
from Sliders.Slider import Slider
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics

from typing import Tuple

"""
A special controller, which is not user-configurable and not part of the ControllerManager list, 
specifically for point turns. Stored privately in Simulation.py
"""

class PointTurnController(AbstractController):

    def __init__(self):
        super().__init__("Point Turns")
    
    # Not user-configurable, so return an empty list
    def defineParameterSliders(self) -> list[ControllerSliderState]:
        return []

    # To be called at the start of a simulation. Sets waypoints and initial state
    def initSimulation(self, robotSpecs: RobotSpecs, targetHeading: float):
        self.robotSpecs = robotSpecs
        self.targetHeading: float = 0#targetHeading

    # nothing else needed to init
    def initController(self):
        pass

    # Simulate a point turn to self.targetHeading
    # Simple non-blocking P control to desired heading
    def simulateTick(self, output: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool, HUDGraphics]:
          
        K_p = 5

        error = (output.heading - self.targetHeading) * K_p
        return RobotModelInput(error, -error), abs(error) < 0.03, HUDGraphics() # in radians, roughly 3 degrees of tolerance