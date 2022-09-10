from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
import Utility

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