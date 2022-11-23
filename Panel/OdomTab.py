from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Simulation.DriverControl.DriverSimulation import DriverSimulation
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class OdomTab(AbstractTab):

    def __init__(self, driver: DriverSimulation):
        self.driver: DriverSimulation = driver

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        
        yield self.driver.velocityGUI

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        
        self.driver.draw(screen)