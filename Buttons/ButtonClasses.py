from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.AbstractButton import Button, ToggleButton
from VisibleElements.Tooltip import Tooltip
import Utility

# Button on panel to select edit mode
class EditButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Edit path")

        position = (Utility.SCREEN_SIZE + 20, 30)
        super().__init__(position, "Images/Buttons/edit.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.EDIT

    # Implementing Clickable function
    # When clicked, set to edit mode
    def click(self):
        self.softwareState.mode = Mode.EDIT


# Button on panel to select simulate mode
class SimulateButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Tune parameters for path following on the virtual", "robot, and simulate path following algorithms")

        position = (Utility.SCREEN_SIZE + 90, 30)
        super().__init__(position, "Images/Buttons/simulate.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.SIMULATE

    # Implementing Clickable function
    # When clicked, set to play mode
    def click(self):
        self.softwareState.mode = Mode.SIMULATE

# Button on panel to select robot mode
class RobotButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Export the path to the VEX robot and import a", "recorded run to the program through serial")

        position = (Utility.SCREEN_SIZE + 160, 30)
        super().__init__(position, "Images/Buttons/robot.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to ROBOT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.ROBOT

    # Implementing Clickable function
    # When clicked, set to robot mode
    def click(self):
        self.softwareState.mode = Mode.ROBOT

        
# Button on panel to select odom mode
class OdomButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Test robot odometry by displaying the VEX", "robot's real-time position through serial")

        position = (Utility.SCREEN_SIZE + 230, 30)
        super().__init__(position, "Images/Buttons/odom.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to ODOM
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.ODOM

    # Implementing Clickable function
    # When clicked, set to odom mode
    def click(self):
        self.softwareState.mode = Mode.ODOM