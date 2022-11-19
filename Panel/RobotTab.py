from Panel.AbstractTab import AbstractTab
from MouseInterfaces.Hoverable import Hoverable
from Panel.UIButtons.ExportButton import ExportButton
from FileInteraction.CSVExporter import CSVExporter
from VisibleElements.FullPath import FullPath
from typing import Iterator
import pygame


"""
Stores all the UI for the Simulation tab
"""

class RobotTab(AbstractTab):

    def __init__(self, path: FullPath):
        self.exportToCSV = ExportButton(CSVExporter(path),(245,100))
        #self.exportSerialize

    # A generator for all the hoverable UI objects
    def getHoverables(self) -> Iterator[Hoverable]:
        yield self.exportToCSV

    # Draw all the UI onto the screen
    def draw(self, screen: pygame.Surface):
        self.exportToCSV.draw(screen)