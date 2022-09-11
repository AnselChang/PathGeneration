from SingletonState.SoftwareState import SoftwareState, Mode
from Buttons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import Utility, pygame

# Button on panel to select edit mode
class EditButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Edit path")

        position = (Utility.SCREEN_SIZE + 20, 30)
        super().__init__(position, "Images/Buttons/edit.png", 0.1)

    # EditButton only ever has one tooltip message to draw
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.EDIT

    # edit button is never disabled
    def isDisabled(self) -> bool:
        return False

    # Implementing ToggleButton function
    # When toggled on, set mode to edit
    def toggleButtonOn(self):
        self.softwareState.mode = Mode.EDIT