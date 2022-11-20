from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
from FileInteraction.PickleImporter import PickleImporter
import tkinter
import tkinter.filedialog
import pygame

"""
Provides search and run functionality for importing the path from a previously serialized path
"""

class ImportButton(ClickButton):

    def __init__(self, importer: PickleImporter, position: tuple[int,int]):

        self.importer: PickleImporter = importer

        self.tooltip = Tooltip("Import a "+importer.getExtension()[1]+" file for editing or running the simulator")

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
        try:
            # Macs who try to use the tkinter module may encounter some issues. Wrapped in a try to avoid crashing
            top = tkinter.Tk()
            top.withdraw()
            # Extracts the file extension information
            fileExtension = self.importer.getExtension()
            # Uses the tkinter module to allow the user to select a file name and location
            # Needs to append "*" to the beginning of the file extension for proper displaying of the
            # type hint in the file dialog. Ex. "Comma-Separated Values Document (*.csv)"
            fileName = tkinter.filedialog.askopenfilename(parent=top, defaultextension=fileExtension[1], 
                filetypes=[(fileExtension[0],"*"+fileExtension[1])])
            # If no filename was set, do not import
            if fileName == "":
                return
            # Runs the import
            self.importer.importFile(fileName)
        except:
            # Custom error message to spite Ansel
            print("We do not support Macs in this house. Sorry, but you cannot use the Exporter")