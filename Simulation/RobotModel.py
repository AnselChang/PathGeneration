import math

"""
Kinematic model of robot that adheres to physics. The left and right wheel are controllable, and this robot's position
and velocity are simulated over time. We assume no drift tangent to driving direction but a configurable amount of drift
horizontally across the robot.
"""

class SimulatedRobot:

    def __init__(self, startPosition: tuple):

        self.xPosition, self.yPosition = startPositions
        self.deltaX, self.deltaY = 0,0
        self.heading = 0

        self.trackWidth = 10 # inches
        self.driftFriction = 1 # in inches per second^2
        self.timestep = 0.05 # how long each tick lasts in seconds

    # Simulate robot physics given wheel speeds, and assuming no accelerational limits for wheels
    # velocities given in inch/sec
    def simulateTick(self, leftVelocity: float, rightVelocity: float):

        oldDeltaX, oldDeltaY = self.deltaX, self.deltaY

        # the distance the wheels travelled this tick
        leftDistance = leftVelocity * self.timestep
        rightDistance = rightVelocity * self.timestep

        deltaTheta = (rightDistance - leftDistance) / self.trackWidth
        deltaDistance = (rightDistance + leftDistance) / 2

        self.deltaX = deltaDistance * math.cos(self.heading + deltaTheta/2)
        self.deltaY = deltaDistance * math.sin(self.heading + deltaTheta/2)
        
        # the left and right velocities are relative to heading, and with no drift, set the velocity in that direction
        self.xPosition += self.deltaX
        self.yPosition += self.deltaY
        self.heading += deltaTheta

        # Calculate drift from previous frame
        

