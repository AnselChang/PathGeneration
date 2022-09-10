from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.ToggleButton import ToggleButton
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