from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from UIButtons.ExportButton import ExportButton
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class RobotTab(AbstractTab):

    def __init__(self, export:ExportButton):
        self.exportButton

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        pass