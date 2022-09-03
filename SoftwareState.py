from enum import Enum

from Draggable import Draggable


""" A class representing global state of the software."""

class Mode(Enum):
    EDIT = 1 # Modfying the path
    SIMULATION = 2 # Simulating the path with some path following algorithm with a virtual robot

class SoftwareState:

    def __init__(self):
        self.mode: Mode = Mode.EDIT # edit or simulation mode
        self.objectHovering: object = None # object the mouse is currently hovering over
        self.objectDragged: Draggable = None # object the mouse is currently dragging

    

