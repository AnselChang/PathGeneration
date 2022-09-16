from Panel.AbstractButtons.FlipFlopButton import FlipFlopButton
import Utility, Graphics
from VisibleElements.Tooltip import Tooltip
from AI.DiscManager import DiscManager
from AI.MCTS import MCTS

import pygame

"""
Right button for going to the previous controller in the Simulation tab
"""

class AIRunButton(FlipFlopButton):

    def __init__(self, discManager: DiscManager):

        self.mcts: MCTS = discManager.mcts

        self.tooltipRun = Tooltip("Run MCTS")
        self.tooltipRunning = Tooltip("Running...")

        imageOn = Graphics.getImage("Images/Buttons/ai_on.png", 0.3)
        imageHoveredOn = Graphics.getLighterImage(imageOn, 0.75)
        imageOff = Graphics.getImage("Images/Buttons/ai_off_hovered.png", 0.3)
        imageHoveredOff = Graphics.getLighterImage(imageOff, 0.75)

        self.on = False

        super().__init__((Utility.SCREEN_SIZE + 75, Utility.SCREEN_SIZE - 180), imageOff, imageHoveredOff, imageOn, imageHoveredOn)

    # Draw right button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        if self.isOn():
            self.tooltipRunning.draw(screen, mousePosition)
        else:
            self.tooltipRun.draw(screen, mousePosition)

     # Return whether MCTS algorithm is running
    def isOn(self) -> bool:
        return self.mcts.isRunning()

  # When clicked, either start or stop the MCTS
    def toggleButton(self) -> None:
        
        if self.isOn():
            self.mcts.disable()
        else:
            self.mcts.enable()

