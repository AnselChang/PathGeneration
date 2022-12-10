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
        self.maximumAcceleration = 0.5 # maximum change in velocity in inches/sec per second
        
        # THIS ONE IS IRRELEVANT FOR NOW
        self.mesialFriction = 1 # coefficient of friction along heading of robot (Between 0 and 1 only)
        
        
        self.lateralFriction = 0.1 # coefficient of friction perpendicular to heading of robot (Between 0 and 1)