from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from typing import Iterator
import pygame, Graphics, colors, Utility


"""
Stores all the UI for the Simulation tab
"""

class SimulationTab(AbstractTab):

    def __init__(self):
        pass

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):

        # Draw text horizontally centered in panel
        textPosition = (Utility.SCREEN_SIZE + Utility.PANEL_WIDTH/2, 120)
        Graphics.drawText(screen, Graphics.FONT40, "Pure Pursuit", colors.BLACK, *textPosition)