from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from VisibleElements.FullPath import FullPath
from SingletonState.SoftwareState import SoftwareState
from typing import Iterator
import pygame


"""
Stores all the UI for the Robot tab
"""

class RobotTab(AbstractTab):

    def __init__(self, state: SoftwareState, path: FullPath):
        pass

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        pass
