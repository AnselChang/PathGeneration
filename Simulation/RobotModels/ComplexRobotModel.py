from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from RobotSpecs import RobotSpecs
import math

"""
Accurate kinematic model of robot that adheres to physics. We simulate the robot's position and velocity over time, given
left and right wheel velocities at each tick. We account for drift in both mesial and lateral directions specified by robotSpec
"""

class ComplexRobotModel(AbstractRobotModel):

    def __init__(self, robotSpecs: RobotSpecs, start: RobotModelOutput):

        # initialize robot sepcs and start pose in superclass
        super().__init__(robotSpecs, start)

        self.deltaX, self.deltaY = 0,0

    # We account for slipping from self.robotSpecs friction coefficients
    def simulateTick(self, input: RobotModelInput) -> RobotModelOutput:

        # TODO @Kohmei
        pass
