from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Simulation.Waypoints import Waypoints
import pygame

"""
An abstract class for an algorithm that follows a given path. Example subclasses are Pure Pursuit, Stanley, etc.
This takes in a Waypoints object at initiailization, and at every tick computes new inputs to the robot model (velocities)
given the robot outputs (robot position and orientation)
"""

class AbstractController(ABC):

    def __init__(self, waypoints: Waypoints):

        self.waypoints = waypoints

    # To be implemented by each algorithm. Simulates path following at each timestep.
    # Returns the list of RobotStates at each timestep
    @abstractmethod
    def simulateTick(self, output: RobotModelOutput) -> RobotModelInput:
        pass