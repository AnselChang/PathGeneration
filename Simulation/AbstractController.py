from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
from Simulation.RobotState import RobotState
from Simulation.Waypoints import Waypoints
import pygame

"""
An abstract class for an algorithm that follows a given path. Example subclasses are Pure Pursuit, Stanley, etc.
This takes in a Waypoints object, and then calculates and stores an array of RobotStates, with position,
velocity, heading, etc. at each timestep.

This class also handles drawing the simulated path line, and retrieving the RobotState at each timestep
during simulation

Everything is stored relative to the field. This is converted to screenRef only when drawing everything
"""

class AbstractController(ABC):

    def __init__(self, waypoints: Waypoints, initialPosition: PointRef):

        self._simulation: list[RobotState] = self.simulateAlgorithm(waypoints, initialPosition)

    # To be implemented by each algorithm. Simulates path following at each timestep.
    # Returns the list of RobotStates at each timestep
    @abstractmethod
    def simulateAlgorithm(self, waypoints: Waypoints) -> list[RobotState]:
        pass

    # Get the RobotState at the specified timestep
    def getTimestep(self, timestep: int) -> RobotState:
        return self._simulation[timestep]

    # Draw the line the robot takes when following the path on the field
    def drawSimulatedPathLine(self, screen: pygame.Surface):
        # TODO
        pass