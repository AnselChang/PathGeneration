from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
from FileInteraction.AbstractExporter import AbstractExporter
from VisibleElements.FullPath import FullPath
import tkinter
import tkinter.filedialog
import pygame
import sys

"""
Provides search and run functionality for exporting the path to various functionality
"""

class ExportButton(ClickButton):

    def __init__(self, path: FullPath, exporter: AbstractExporter, position: tuple[int,int], image):

        self.path = path
        self.exporter: AbstractExporter = exporter

        self.tooltip = Tooltip("Export a "+exporter.getExtension()[1]+" file")

        imageEnabled = image
        imageHovered = Graphics.getLighterImage(imageEnabled, 0.77)
        imageDisabled = Graphics.getLighterImage(imageEnabled, 0.3)
        super().__init__((Utility.SCREEN_SIZE+position[0], position[1]), imageDisabled, imageEnabled, imageHovered)

    # Draw export button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)

    # No reason to disable this button
    def isDisabled(self) -> bool:
        return self.path.isEmptyInterpolated()


    # Runs the exporter (passed in during __init__)
    def clickEnabledButton(self) -> None:

        #Extracts the file extension information
        fileExtension = self.exporter.getExtension()

        if sys.platform != "darwin":
            # Macs who try to use the tkinter module may encounter some issues. Wrapped in a try to avoid crashing
            top = tkinter.Tk()
            top.withdraw()
            
            # Uses the tkinter module to allow the user to select a file name and location
            fileName = tkinter.filedialog.asksaveasfilename(parent=top, defaultextension=fileExtension[1], 
                filetypes=[(fileExtension[0],"*"+fileExtension[1])])
            # If no filename was set, do not export
            if fileName == "":
                return
            
        else:
            print(fileExtension)
            fileName = "GeneratedPath" + fileExtension[1]

        # Runs the exporter
        self.exporter.export(fileName)
        print("Exported as ", fileName)