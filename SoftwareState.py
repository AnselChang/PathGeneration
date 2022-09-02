from enum import Enum

from Draggable import Draggable

class Mode(Enum):
    EDIT = 1
    SIMULATION = 2

class SoftwareState:

    def __init__(self):
        self.mode = Mode.EDIT
        self.objectDragged: Draggable = None

    

