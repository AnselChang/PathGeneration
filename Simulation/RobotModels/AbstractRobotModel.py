from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from RobotSpecs import RobotSpecs
from abc import ABC, abstractmethod

"""
An interface for a kinematic model of robot that adheres to physics.
Each implementation should simulate the robot's position and velocity over time, given
left and right wheel velocities at each tick. Implementations may have varying levels
of accuracy.
"""

class AbstractRobotModel(ABC):

    def __init__(self, robotSpecs: RobotSpecs, start: RobotModelOutput):

        # Set initial conditions
        self.xPosition, self.yPosition = start.position.fieldRef
        self.heading = start.heading

        # Set robot specifications
        self.robotSpecs = robotSpecs

    # Implemntations must simulate robot physics given wheel speeds
    # velocities given in inch/sec
    @abstractmethod
    def simulateTick(self, input: RobotModelInput) -> RobotModelOutput:
        pass
