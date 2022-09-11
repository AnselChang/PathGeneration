from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Simulation.Waypoints import Waypoints
from Sliders.Slider import Slider

from typing import Tuple

"""
An abstract class for an algorithm that follows a given path. Example subclasses are Pure Pursuit, Stanley, etc.
This takes in a Waypoints object at initiailization, and at every tick computes new inputs to the robot model (velocities)
given the robot outputs (robot position and orientation)
"""

class AbstractController(ABC):

    def __init__(self):
        self.sliders = self.defineParameterSliders()


    # Any controller that implements AbstractController must return a list of sliders for the tunable parameters
    # of that controller
    @abstractmethod
    def defineParameterSliders(self) -> list[Slider]:
        pass
        

    # To be called at the start of a simulation. Sets waypoints and initial state
    def initSimulation(self, waypoints: list[PointRef]):
        self.waypoints: list[PointRef] = waypoints

    # To be implemented by each algorithm. Simulates path following at each timestep.
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    @abstractmethod
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        pass