from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.AbstractButton import Button, ToggleButton
from VisibleElements.Tooltip import Tooltip
import Utility

# Button on panel to select edit mode (as opposed to play mode)
class EditButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Edit path")

        position = (Utility.SCREEN_SIZE + 30, 30)
        super().__init__(position, "Images/Buttons/edit.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.EDIT

    # Implementing Clickable function
    # When clicked, set to edit mode
    def click(self):
        self.softwareState.mode = Mode.EDIT


# Button on panel to select play mode (as opposed to edit mode)
class PlayButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Simulate and test path")

        position = (Utility.SCREEN_SIZE + 100, 30)
        super().__init__(position, "Images/Buttons/play.png", 0.1)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.PLAY

    # Implementing Clickable function
    # When clicked, set to play mode
    def click(self):
        self.softwareState.mode = Mode.PLAY
