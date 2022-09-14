from Panel.AbstractButtons.FlipFlopButton import FlipFlopButton
import Utility, Graphics
from SingletonState.SoftwareState import SoftwareState
from Simulation.Simulation import Simulation
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import pygame

"""
Right button for going to the previous controller in the Simulation tab
"""

class AIRunButton(FlipFlopButton):

    def __init__(self):


        self.tooltipRun = Tooltip("Run MCTS")
        self.tooltipRunning = Tooltip("Running...")

        imageOn = Graphics.getImage("Images/Buttons/ai_on.png", 0.08)
        imageHoveredOn = Graphics.getLighterImage(imageOn, 0.8)
        imageHoveredOff = Graphics.getImage("Images/Buttons/ai_off_hovered.png", 0.08)
        imageOff = Graphics.getImage("Images/Buttons/ai_off.png", 0.08)
        super().__init__((Utility.SCREEN_SIZE + 50, 170), imageOff, imageHoveredOff, imageOn, imageHoveredOn)

    # Draw right button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        if self.isOn():
            self.tooltipRunning.draw(screen, mousePosition)
        else:
            self.tooltipRun.draw(screen, mousePosition)

     # Return whether MCTS algorithm is running
    def isOn(self) -> bool:
        return False

  # When clicked, either start or stop the MCTS
    def toggleButton(self) -> None:
        pass

