from Panel.AbstractTab import AbstractTab
from Panel.UIButtons.LeftButton import LeftButton
from Panel.UIButtons.RightButton import RightButton
from Panel.UIButtons.SimulationOnOffButton import SimulationOnOffButton
from SingletonState.SoftwareState import SoftwareState
from MouseInterfaces.Hoverable import Hoverable
from typing import Iterator
from Simulation.Simulation import Simulation
import pygame, Graphics, colors, Utility


"""
Stores all the UI for the Simulation tab
"""

class SimulationTab(AbstractTab):

    def __init__(self, state: SoftwareState, simulation: Simulation):
        self.simulation = simulation

        self.leftButton: LeftButton = LeftButton(simulation.controllers)
        self.rightButton: RightButton = RightButton(simulation.controllers)
        self.playButton: SimulationOnOffButton = SimulationOnOffButton(state, simulation)

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        yield self.leftButton
        yield self.rightButton
        yield self.playButton

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):

        # Draw text horizontally centered in panel
        textPosition = (Utility.SCREEN_SIZE + Utility.PANEL_WIDTH/2, 120)
        controllerName: str = self.simulation.controllers.getController().name
        Graphics.drawText(screen, Graphics.FONT40, controllerName, colors.BLACK, *textPosition)

        self.simulation.draw(screen)
        self.leftButton.draw(screen)
        self.rightButton.draw(screen)
        self.playButton.draw(screen)