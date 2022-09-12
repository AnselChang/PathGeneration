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

    # Initialize transform reference at the creation of simulation object
    transform: FieldTransform = None

    # xPosition and yPosition in inches
    def __init__(self, xPosition: float, yPosition: float, headingRadians: float):
        self.position = PointRef(self.transform, Ref.FIELD, (xPosition, yPosition))
        self.heading = headingRadians
