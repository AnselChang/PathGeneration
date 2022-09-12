from Panel.AbstractTab import AbstractTab
from Panel.UIButtons.LeftButton import LeftButton
from Panel.UIButtons.RightButton import RightButton
from MouseInterfaces.Hoverable import Hoverable
from typing import Iterator
from Simulation.ControllerManager import ControllerManager
import pygame, Graphics, colors, Utility


"""
Stores all the UI for the Simulation tab
"""

class SimulationTab(AbstractTab):

    def __init__(self, controllers: ControllerManager):
        self.controllers = controllers

        self.leftButton: LeftButton = LeftButton(controllers)
        self.rightButton: RightButton = RightButton(controllers)

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        yield self.leftButton
        yield self.rightButton

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):

        # Draw text horizontally centered in panel
        textPosition = (Utility.SCREEN_SIZE + Utility.PANEL_WIDTH/2, 120)
        Graphics.drawText(screen, Graphics.FONT40, self.controllers.getController().name, colors.BLACK, *textPosition)

        self.leftButton.draw(screen)
        self.rightButton.draw(screen)