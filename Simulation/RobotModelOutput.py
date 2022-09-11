from SingletonState.ReferenceFrame import PointRef

"""
The output of the robot model at each tick, and the input to the next Controller tick.
Stores the physical state of the robot at some timestep.
Simulation stores a list of RobotModelOutputs, which fully describe the robot's simulated path

Stores position (as a PointRef), heading, maybe velocity if controllers use them?

Everything is stored relative to the field
"""

class RobotModelOutput:

    def __init__(self, position: PointRef, headingRadians: float):
        self.position = position
        self.heading = headingRadians
