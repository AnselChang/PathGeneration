from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Simulation.Waypoints import Waypoints
from RobotSpecs import RobotSpecs
from Sliders.Slider import Slider

from typing import Tuple

"""
An abstract class for an algorithm that follows a given path. Example subclasses are Pure Pursuit, Stanley, etc.
This takes in a Waypoints object at initiailization, and at every tick computes new inputs to the robot model (velocities)
given the robot outputs (robot position and orientation)
"""

class AbstractController(ABC):

    def __init__(self, name: str):
        self.name: str = name
        self.simulationSliders: list[Slider] = self.defineParameterSliders() # sliders for tuning the simulation robot
        self.robotSliders: list[Slider] = self.defineParameterSliders() # sliders for tuning the actual robot


    # Any controller that implements AbstractController must return a list of sliders for the tunable parameters
    # of that controller
    @abstractmethod
    def defineParameterSliders(self) -> list[Slider]:
        pass
        

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
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        pass