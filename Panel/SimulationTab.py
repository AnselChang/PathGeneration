from Panel.AbstractTab import AbstractTab
from Panel.UIButtons.LeftButton import LeftButton
from Panel.UIButtons.RightButton import RightButton
from Panel.UIButtons.SimulationOnOffButton import SimulationOnOffButton
from Panel.UIButtons.ParamResetButton import ParamResetButton
from SingletonState.SoftwareState import SoftwareState, Mode
from MouseInterfaces.Hoverable import Hoverable
from typing import Iterator
from Simulation.Simulation import Simulation
import pygame, Graphics, colors, Utility
from Sliders.Slider import Slider


"""
Stores all the UI for the Simulation tab
"""

class SimulationTab(AbstractTab):


    def __init__(self, state: SoftwareState, simulation: Simulation):
        self.simulation = simulation
        self.state = state

        self.leftButton: LeftButton = LeftButton(simulation.controllers)
        self.rightButton: RightButton = RightButton(simulation.controllers)
        self.resetButton: ParamResetButton = ParamResetButton(simulation.controllers)
        self.playButton: SimulationOnOffButton = SimulationOnOffButton(state, simulation)

    # If space key pressed, toggle play button.
    # If left or right key pressed, scrub one frame for simulation
    # Esc to exit back to edit mode
    def handleKeyboardInput(self, keyJustPressed):
        if keyJustPressed == pygame.K_SPACE:
            self.playButton.toggleButton()
        elif keyJustPressed == pygame.K_LEFT or keyJustPressed == pygame.K_RIGHT:
            self.simulation.moveSlider(1 if keyJustPressed == pygame.K_RIGHT else -1)
            self.playButton.state.playingSimulation = False
        elif keyJustPressed == pygame.K_ESCAPE:
            self.state.mode = Mode.EDIT

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:

        yield self.simulation.velocityGUI

        yield self.leftButton
        yield self.rightButton
        yield self.resetButton
        yield self.playButton

        if self.simulation.exists():
            yield self.simulation.slider

        for slider in self.simulation.controllers.getCurrentSliders():
            yield slider


    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):

        # Draw text horizontally centered in panel
        textPosition = (Utility.SCREEN_SIZE + Utility.PANEL_WIDTH/2, 120)
        controllerName: str = self.simulation.controllers.getCurrentName()
        Graphics.drawText(screen, Graphics.FONT40, controllerName, colors.BLACK, *textPosition)

        self.simulation.draw(screen)

        self.resetButton.draw(screen)
        self.leftButton.draw(screen)
        self.rightButton.draw(screen)
        self.playButton.draw(screen)

        if self.simulation.exists():
            self.simulation.slider.draw(screen)

        for slider in self.simulation.controllers.getCurrentSliders():
            slider.draw(screen)

        self.simulation.velocityGUI.draw(screen)

