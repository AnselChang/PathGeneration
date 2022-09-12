from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class OdomTab(AbstractTab):

    def __init__(self):
        pass

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        pass