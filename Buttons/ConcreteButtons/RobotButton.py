from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.AbstractButton import AbstactButton, ToggleButton
from VisibleElements.Tooltip import Tooltip
import Utility


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