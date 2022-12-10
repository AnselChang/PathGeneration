from SingletonState.SoftwareState import SoftwareState, Mode
from Panel.AbstractButtons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
from VisibleElements.FullPath import FullPath
from SingletonState.ReferenceFrame import PointRef
import Utility, pygame, Graphics


# Button on panel to select robot mode
class RobotButton(ToggleButton):

    def __init__(self, state: SoftwareState, path: FullPath):
        self.softwareState = state
        self.path = path
        self.tooltipEnabled = Tooltip("Export the path to the VEX robot and import a", "recorded run to the program through serial")
        self.tooltipDisabled = Tooltip("Disabled: Draw a path first in Edit mode", "before interfacing with the robot!")

        position = (Utility.SCREEN_SIZE + 185, 30)
        imageOn = Graphics.getImage("Images/Buttons/robot.png", 0.08)
        imageHovered = Graphics.getLighterImage(imageOn, 0.66)
        imageOff = Graphics.getLighterImage(imageOn, 0.33)
        super().__init__(position, imageOff, imageHovered, imageOn)

    # If there are at least two waypoints, then we can switch to this mode. Otherwise, we display an error tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        if self.isDisabled():
            self.tooltipDisabled.draw(screen, mousePosition)
        else:
            self.tooltipEnabled.draw(screen, mousePosition)

    # Implementing ToggleButton function
    # button is active when the software mode is set to ROBOT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.ROBOT

    # robot button is disabled if there is no path
    def isDisabled(self) -> bool:
        return self.path.isEmptyInterpolated()

    # Implementing ToggleButton function
    # When toggled on, set mode to edit
    def toggleButtonOn(self):
        self.softwareState.mode = Mode.ROBOT