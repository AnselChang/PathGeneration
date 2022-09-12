from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
import math

"""
Kinematic model of robot that adheres to physics. We simulate the robot's position and velocity over time, given
left and right wheel velocities at each tick. We assume no drift tangent to driving direction but a configurable
amount of drift horizontally across the robot.
"""

class RobotModel:

    def __init__(self, start: RobotModelOutput):

        self.xPosition, self.yPosition = start.position.fieldRef
        self.deltaX, self.deltaY = 0,0
        self.heading = 0

        self.trackWidth = 10 # inches
        self.driftFriction = 1 # in inches per second^2

    # Simulate robot physics given wheel speeds, and assuming no accelerational limits for wheels
    # velocities given in inch/sec
    def simulateTick(self, input: RobotModelInput, timestep: float) -> RobotModelOutput:

        #TODO Kohmei, this code is probably wrong. It's up to you to write this
        """

        oldDeltaX, oldDeltaY = self.deltaX, self.deltaY

        # the distance the wheels travelled this tick
        leftDistance = input.leftVelocity * self.timestep
        rightDistance = input.rightVelocity * self.timestep

        deltaTheta = (rightDistance - leftDistance) / self.trackWidth
        deltaDistance = (rightDistance + leftDistance) / 2

        self.deltaX = deltaDistance * math.cos(self.heading + deltaTheta/2)
        self.deltaY = deltaDistance * math.sin(self.heading + deltaTheta/2)
        
        # the left and right velocities are relative to heading, and with no drift, set the velocity in that direction
        self.xPosition += self.deltaX
        self.yPosition += self.deltaY
        self.heading += deltaTheta

        # Calculate drift from previous frame
        
        """
