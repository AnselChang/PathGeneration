from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
from FileInteraction.AbstractExporter import AbstractExporter
import tkinter
import tkinter.filedialog
import pygame

"""
Provides search and run functionality for exporting the path to various functionality
"""

class ExportButton(ClickButton):

    def __init__(self, exporter: AbstractExporter, position: tuple[int,int]):

        self.exporter: AbstractExporter = exporter

        self.tooltip = Tooltip("Export a .csv file to be used in the C++ robot code")

        imageHovered = Graphics.getImage("Images/Buttons/robot.png", 0.08)
        imageEnabled = Graphics.getImage("Images/Buttons/robot.png", 0.08)
        imageDisabled = Graphics.getLighterImage(imageEnabled, 0.33)
        super().__init__((Utility.SCREEN_SIZE+position[0], position[1]), imageDisabled, imageEnabled, imageHovered)

    # Draw export button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)

    # No reason to disable this button
    def isDisabled(self) -> bool:
        return False


    # When clicked, go to previous controller
    def clickEnabledButton(self) -> None:
        top = tkinter.Tk()
        top.withdraw()
        fileName = tkinter.filedialog.asksaveasfilename(parent=top, defaultextension=".csv", 
            filetypes=[("Comma-Separated Value Documents","*.csv")])
        if fileName == "":
            return
        self.exporter.export(fileName)