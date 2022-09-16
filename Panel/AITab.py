from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Panel.UIButtons.AIRunButton import AIRunButton
from Sliders.Slider import Slider
from typing import Iterator
from AI.DiscManager import DiscManager
import pygame, Utility, colors


"""
Stores all the UI for the Simulation tab
"""

class AITab(AbstractTab):

    def __init__(self, discManager: DiscManager):
        
        self.runButton: AIRunButton = AIRunButton(discManager)
        self.explorationSlider: Slider = Slider(Utility.SCREEN_SIZE + 30, 150, 100, 25, 400, 1, colors.ORANGE)
        discManager.initSlider(self.explorationSlider)


    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:

        yield self.runButton
        yield self.explorationSlider

        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        self.runButton.draw(screen)
        self.explorationSlider.draw(screen)