from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import pygame

"""
Right button for going to the previous controller in the Simulation tab
"""

class RightButton(ClickButton):

    def __init__(self, exporter: CSVExporter):

        self.exporter: CSVExporter = exporter

        self.tooltip = Tooltip("Export a .csv file to be used in the C++ robot code")

        imageHovered = Graphics.getImage("Images/Buttons/robot.png", 0.08)
        imageEnabled = Graphics.getImage("Images/Buttons/robot.png", 0.08)
        imageDisabled = Graphics.getLighterImage(imageEnabled, 0.33)
        super().__init__((Utility.SCREEN_SIZE+245, 100), imageDisabled, imageEnabled, imageHovered)

    # Draw right button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)


    # Whether there is a previous controller
    def isDisabled(self) -> bool:
        return False


    # When clicked, go to previous controller
    def clickEnabledButton(self) -> None:
        self.exporter.run()