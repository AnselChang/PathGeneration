from SingletonState.SoftwareState import SoftwareState, Mode
from Panel.AbstractButtons.ToggleButton import ToggleButton
from VisibleElements.Tooltip import Tooltip
from Simulation.Waypoints import Waypoints
from SingletonState.ReferenceFrame import PointRef
import Utility, pygame

# Button on panel to select simulate mode
class SimulateButton(ToggleButton):

    def __init__(self, state: SoftwareState, waypoints: Waypoints):
        self.softwareState = state
        self.waypoints = waypoints
        self.tooltipEnabled = Tooltip("Tune parameters for path following on the virtual", "robot, and simulate path following algorithms")
        self.tooltipDisabled = Tooltip("Disabled: Draw a path first in Edit mode", "before trying to simulate path following!")

        position = (Utility.SCREEN_SIZE + 130, 30)
        super().__init__(position, "Images/Buttons/simulate.png", 0.08)

    # If there are at least two waypoints, then we can switch to this mode. Otherwise, we display an error tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        if self.isDisabled():
            self.tooltipDisabled.draw(screen, mousePosition)
        else:
            self.tooltipEnabled.draw(screen, mousePosition)

    # Implementing ToggleButton function
    # button is active when the software mode is set to EDIT
    def isToggled(self) ->  bool:
        return self.softwareState.mode == Mode.SIMULATE

    # robot button is disabled if there is no path
    def isDisabled(self) -> bool:
        return self.waypoints.size < 2

    # Implementing ToggleButton function
    # When toggled on, set mode to edit
    def toggleButtonOn(self):
        self.softwareState.mode = Mode.SIMULATE