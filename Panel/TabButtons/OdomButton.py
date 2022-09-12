from SingletonState.SoftwareState import SoftwareState, Mode
from Panel.AbstractButtons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import Utility, pygame

# Button on panel to select odom mode
class OdomButton(ToggleButton):

    def __init__(self, state: SoftwareState):
        self.softwareState = state
        self.tooltip = Tooltip("Test robot odometry by displaying the VEX", "robot's real-time position through serial")

        position = (Utility.SCREEN_SIZE + 240, 30)
        super().__init__(position, "Images/Buttons/odom.png", 0.08)

    # Odombutton only ever has one tooltip message to draw
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)

    # Implementing ToggleButton function
    # button is active when the software mode is set to ODOM
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.ODOM

    # odom button is never disabled
    def isDisabled(self) -> bool:
        return False

    # Implementing ToggleButton function
    # When toggled on, set mode to odom
    def toggleButtonOn(self):
        self.softwareState.mode = Mode.ODOM