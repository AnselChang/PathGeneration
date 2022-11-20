from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Panel.UIButtons.ExportButton import ExportButton
from Panel.UIButtons.ImportButton import ImportButton
from FileInteraction.CSVExporter import CSVExporter
from FileInteraction.PickleExporter import PickleExporter
from FileInteraction.PickleImporter import PickleImporter
from VisibleElements.FullPath import FullPath
from SingletonState.SoftwareState import SoftwareState
from typing import Iterator
import pygame


"""
Stores all the UI for the Robot tab
"""

class RobotTab(AbstractTab):

    def __init__(self, state: SoftwareState, path: FullPath):
        self.exportToCSV = ExportButton(CSVExporter(path),(66,100))
        self.exportSerialize = ExportButton(PickleExporter(path), (132,100))
        self.importButton = ImportButton(PickleImporter(state, path), (194,100))

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        yield self.exportToCSV
        yield self.exportSerialize
        yield self.importButton

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        self.exportToCSV.draw(screen)
        self.exportSerialize.draw(screen)
        self.importButton.draw(screen)