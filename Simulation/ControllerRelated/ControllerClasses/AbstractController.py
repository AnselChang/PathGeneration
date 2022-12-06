from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from SingletonState.ReferenceFrame import PointRef
from RobotSpecs import RobotSpecs
from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState, buildControllerSliders
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics
from Sliders.Slider import Slider

from typing import Tuple

"""
An abstract class for an algorithm that follows a given path. Example subclasses are Pure Pursuit, Stanley, etc.
This takes in a list of PointRefs at initialization, and at every tick computes new inputs to the robot model (velocities)
given the robot outputs (robot position and orientation)
"""

class AbstractController(ABC):


    def __init__(self, name: str):
        self.name : str = name
        self.sliders: list[Slider] = buildControllerSliders(self.defineParameterSliders())
        
    # Any controller that implements AbstractController must return a list of sliders for the tunable parameters
    # of that controller
    @abstractmethod
    def defineParameterSliders(self) -> list[ControllerSliderState]:
        pass

    
    # Get the slider value based on the slider's string label
    # since it's O(n) it's probably a good idea to store this and cache for entire simulation
    def getSliderValue(self, label: str) -> float:
        for slider in self.sliders:
            if slider.text == label:
                return slider.getValue()
        raise Exception("Slider not found from label")

    # To be called at the start of a simulation. Sets waypoints and initial state
    def initSimulation(self, robotSpecs: RobotSpecs, waypoints: list[PointRef]):
        self.robotSpecs = robotSpecs
        self.waypoints: list[PointRef] = waypoints

        self.initController()

        
    # Do anything needed to initialize the controller at the start of the path
    @abstractmethod
    def initController(self):
        pass

    # To be implemented by each algorithm. Simulates path following at each timestep.
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    @abstractmethod
    def simulateTick(self, output: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool, HUDGraphics]:
        pass