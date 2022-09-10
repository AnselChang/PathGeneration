from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
import Utility

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