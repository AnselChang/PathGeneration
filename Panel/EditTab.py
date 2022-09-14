from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from SingletonState.SoftwareState import SoftwareState, Mode
from VisibleElements.FullPath import FullPath
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class EditTab(AbstractTab):

    def __init__(self, state: SoftwareState, path: FullPath):
        self.state: SoftwareState = state
        self.path: FullPath = path

    # Spacebar shortcut to go to simulation mode from edit mode
    def handleKeyboardInput(self, keyJustPressed):
        if keyJustPressed == pygame.K_SPACE and self.path.waypoints.size >= 2:
            self.state.mode = Mode.SIMULATE

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        pass