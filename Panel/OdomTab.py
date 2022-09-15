from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Simulation.Simulation import Simulation
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class OdomTab(AbstractTab):

    def __init__(self, simulation: Simulation):
        self.simulation: Simulation = simulation

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        
        yield self.simulation.velocityGUI

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        
        self.simulation.velocityGUI.draw(screen)