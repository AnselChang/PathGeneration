from enum import Enum

from MouseInterfaces.Hoverable import Hoverable
from MouseInterfaces.Draggable import Draggable


""" A class representing global state of the software."""

class Mode(Enum):
    EDIT = 1 # Modfying the path
    SIMULATE = 2 # Simulating the path with some path following algorithm with a virtual robot
    ROBOT = 3 # Configure path following parameters and export to robot; import recorded run to program
    ODOM = 4 # Real-time view of the robot's position through odometry from serial

class SoftwareState:

    def __init__(self):
        self.mode: Mode = Mode.EDIT # edit or simulation mode
        self.objectHovering: Hoverable = None # object the mouse is currently hovering over
        self.objectDragged: Draggable = None # object the mouse is currently dragging

        self.recomputeInterpolation = False # Whether to recompute bezier interpolation from modifying path

    def __str__(self):
        return "Software State:\nHovering: {}\nDragged: {}".format(self.objectHovering, self.objectDragged)

    

