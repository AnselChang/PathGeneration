from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from RobotSpecs import RobotSpecs
import math, Utility

"""
Inaccurate kinematic model of robot that adheres to physics. We simulate the robot's position and velocity over time, given
left and right wheel velocities at each tick. We assume no drift tangent to driving direction but a configurable
amount of drift horizontally across the robot.
"""

class SimpleRobotModel(AbstractRobotModel):

    def __init__(self, robotSpecs: RobotSpecs, start: RobotModelOutput):

        # initialize robot sepcs and start pose in superclass
        super().__init__(robotSpecs, start)

        self.deltaX, self.deltaY = 0,0

    # In the simple robot model, we assume no slipping.
    def simulateTick(self, input: RobotModelInput) -> RobotModelOutput:

        # Clamp velocities within realistic range
        input.leftVelocity = Utility.clamp(input.leftVelocity, -self.robotSpecs.maximumVelocity, self.robotSpecs.maximumVelocity)
        input.rightVelocity = Utility.clamp(input.rightVelocity, -self.robotSpecs.maximumVelocity, self.robotSpecs.maximumVelocity)

        oldDeltaX, oldDeltaY = self.deltaX, self.deltaY

        # the distance the wheels travelled this tick
        leftDistance = input.leftVelocity * self.robotSpecs.timestep
        rightDistance = input.rightVelocity * self.robotSpecs.timestep

        deltaTheta = (rightDistance - leftDistance) / self.robotSpecs.trackWidth
        deltaDistance = (rightDistance + leftDistance) / 2

        self.deltaX = deltaDistance * math.cos(self.heading + deltaTheta/2)
        self.deltaY = deltaDistance * math.sin(self.heading + deltaTheta/2)
        
        # the left and right velocities are relative to heading, and with no drift, set the velocity in that direction
        self.xPosition += self.deltaX
        self.yPosition += self.deltaY
        self.heading += deltaTheta

        return RobotModelOutput(self.xPosition, self.yPosition, self.heading)
