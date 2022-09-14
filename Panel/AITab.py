from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Panel.UIButtons.AIRunButton import AIRunButton
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class AITab(AbstractTab):

    def __init__(self):
        
        self.runButton: AIRunButton = AIRunButton()


    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:

        yield self.runButton

        return
        yield

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        self.runButton.draw(screen)