from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import pygame

"""
Left button for going to the previous controller in the Simulation tab
"""

class LeftButton(ClickButton):

    def __init__(self, controllers: ControllerManager):

        self.controllers: ControllerManager = controllers

        self.tooltip = Tooltip("Select previous controller")

        imageHovered = Graphics.getImage("Images/Buttons/Arrows/left2.png", 0.08)
        imageEnabled = Graphics.getImage("Images/Buttons/Arrows/left.png", 0.08)
        imageDisabled = Graphics.getLighterImage(imageEnabled, 0.33)
        super().__init__((Utility.SCREEN_SIZE+20, 100), imageDisabled, imageEnabled, imageHovered)

    # Draw left button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)


    # Whether there is a previous controller
    def isDisabled(self) -> bool:
        return not self.controllers.isPrevious()


    # When clicked, go to previous controller
    def clickEnabledButton(self) -> None:
        self.controllers.previous()