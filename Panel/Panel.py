from Panel.TabButtons import AIButton, EditButton, OdomButton, RobotButton, SimulateButton
from Panel.AbstractButtons.AbstractButton import AbstactButton
from Panel import AbstractTab, AITab, EditTab, OdomTab, RobotTab, SimulationTab
from SingletonState.SoftwareState import SoftwareState, Mode
from VisibleElements.FullPath import FullPath
from MouseInterfaces.Hoverable import Hoverable
from Simulation.Simulation import Simulation
from Simulation.DriverControl.DriverSimulation import DriverSimulation
from AI.DiscManager import DiscManager
import pygame
from typing import Iterator

"""
A class that handles all the stuff that's drawon on the panel to the right of the vex field
Stores all the Tab objects and draws all the UI from the selected Tab onto the screen
"""

class Panel:

    def __init__(self, state: SoftwareState, path: FullPath, simulation: Simulation, driver: DriverSimulation, discManager: DiscManager):

        self.state: SoftwareState = state
        
        self.tabButtons: list[AbstactButton] = [
            
            AIButton.AIButton(state),
            EditButton.EditButton(state),
            SimulateButton.SimulateButton(state, path),
            RobotButton.RobotButton(state, path),
            OdomButton.OdomButton(state)
        ]

        self.aiTab: AITab.AITab = AITab.AITab(discManager)
        self.editTab: EditTab.EditTab = EditTab.EditTab(state, path)
        self.simulationTab: SimulationTab.SimulationTab = SimulationTab.SimulationTab(state, simulation)
        self.robotTab: RobotTab.RobotTab = RobotTab.RobotTab(state, path)
        self.odomTab: OdomTab.OdomTab = OdomTab.OdomTab(driver)

    # Given the mode, get the tab oject associated with that mode
    def getTab(self, mode: Mode) -> AbstractTab.AbstractTab:
        if mode == Mode.AI:
            return self.aiTab
        elif mode == Mode.EDIT:
            return self.editTab
        elif mode == Mode.SIMULATE:
            return self.simulationTab
        elif mode == Mode.ROBOT:
            return self.robotTab
        else:
            return self.odomTab

    def handleKeyboardInput(self, keyJustPressed):
        if keyJustPressed is not None:
            self.getTab(self.state.mode).handleKeyboardInput(keyJustPressed)


    # Returns a generator of all the hoverable objects for the panel
    def getHoverables(self) -> Iterator[Hoverable]:

        # Yield each tab button
        for tabButton in self.tabButtons:
            yield tabButton
        
        # yield each ui object that would appear in the selected panel tab
        for uiObject in self.getTab(self.state.mode).getHoverables():
            yield uiObject

    # Draw the panel buttons and all the ui objects that would appear in the seleced tab
    def draw(self, screen: pygame.Surface):
        # draw the tab buttons
        for button in self.tabButtons:
            button.draw(screen)

        # draw the ui objects that would appear in the selected panel tab
        self.getTab(self.state.mode).draw(screen)