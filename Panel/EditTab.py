from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from SingletonState.SoftwareState import SoftwareState, Mode
from VisibleElements.FullPath import FullPath
from Panel.UIButtons.ExportButton import ExportButton
from FileInteraction.CSVExporter import CSVExporter
from FileInteraction.PickleExporter import PickleExporter
import Graphics
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class EditTab(AbstractTab):

    def __init__(self, state: SoftwareState, path: FullPath):
        self.state: SoftwareState = state
        self.path: FullPath = path

        self.exportToCSV = ExportButton(path,
            CSVExporter(path),
            (77,110),
            Graphics.getImage("Images/Buttons/csv.png", 0.1))
        self.exportSerialize = ExportButton(path,
            PickleExporter(path),
            (177,110),
            Graphics.getImage("Images/Buttons/save.png", 0.23))

    # Spacebar shortcut to go to simulation mode from edit mode
    def handleKeyboardInput(self, keyJustPressed):
        if keyJustPressed == pygame.K_SPACE and self.path.waypoints.size >= 2:
            self.state.mode = Mode.SIMULATE

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        yield self.exportToCSV
        yield self.exportSerialize

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        self.exportToCSV.draw(screen)
        self.exportSerialize.draw(screen)