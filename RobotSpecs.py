"""
Specs for both the simulated and actual robot.
Some attributes are specifically for robot kinematics simulation only; some will be used by the controller as well.
"""

class RobotSpecs:

    def __init__(self):

        # Used by both kinematics simulation and path following controllers
        self.trackWidth = 10 # in inches
        self.maximumVelocity = 20 # linear velocity of a wheel / robot, inches per second
        self.timestep = 0.05 # the duration of each timestep in seconds

        # Used only for robot simulation
        self.maximumAcceleration = 1 # maximum change in velocity in inches/sec per second
        self.mesialFriction = 1 # coefficient of friction along heading of robot
        self.lateralFriction = 0.2 # coefficient of friction perpendicular to heading of robot