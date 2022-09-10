from SingletonState.ReferenceFrame import PointRef

"""
Stores all the state of a robot's physics at a specific timestep. Useful when generating and playing back path following
simulations.

Stores position (as a PointRef), heading, velocity (at robot heading; we simplify drift as nonexistent but this may change)

Everything is stored relative to the field
"""

class RobotState:

    def __init__(self, position: PointRef, headingRadians: float, inchesPerSecond: float):
        self.position = position
        self.heading = headingRadians
        self.velocity = inchesPerSecond
