from SingletonState.ReferenceFrame import PointRef, Ref
from SingletonState.FieldTransform import FieldTransform

"""
The output of the robot model at each tick, and the input to the next Controller tick.
Stores the physical state of the robot at some timestep.
Simulation stores a list of RobotModelOutputs, which fully describe the robot's simulated path

Stores position (as a PointRef), heading, maybe velocity if controllers use them?

Everything is stored relative to the field
"""

class RobotModelOutput:


    # xPosition and yPosition in inches
    def __init__(self, xPosition: float, yPosition: float, headingRadians: float, clampedLeftVelocity: float, clampedRightVelocity: float, xVelocity: float = 0, yVelocity: float = 0, angularVelocity: float = 0):
        self.position = PointRef(Ref.FIELD, (xPosition, yPosition))
        self.leftVelocity = clampedLeftVelocity
        self.rightVelocity = clampedRightVelocity
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.angularVelocity = angularVelocity
        self.heading = headingRadians

    def __str__(self):
        return str(self.position)
