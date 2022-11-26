from Panel.AbstractButtons.ClickButton import ClickButton
import Utility, Graphics
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from VisibleElements.Tooltip import Tooltip
import pygame

"""
Reset all the controller parameters for the currently-selected controller
"""

class ParamResetButton(ClickButton):

    def __init__(self, controllers: ControllerManager):

        self.controllers: ControllerManager = controllers

        self.tooltip = Tooltip("Reset controller parameters")

        imageEnabled = Graphics.getImage("Images/Buttons/reset.png", 0.27)
        imageHovered = Graphics.getLighterImage(imageEnabled, 0.75)
        imageDisabled = Graphics.getLighterImage(imageEnabled, 0.33)
        super().__init__((Utility.SCREEN_SIZE + 15, 162), imageDisabled, imageEnabled, imageHovered)

    # Draw right button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        self.tooltip.draw(screen, mousePosition)

    # disabled if all the controller parameters are already set to default
    def isDisabled(self) -> bool:
        for slider in self.controllers.getController().sliders:
            if slider.getValue() != slider.default:
                return False
        return True

    # When clicked, reset controller parameter sliders
    def clickEnabledButton(self) -> None:
        for slider in self.controllers.getController().sliders:
            slider.reset()