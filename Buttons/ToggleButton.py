from Buttons.AbstractButton import AbstactButton
from abc import abstractmethod
from MouseInterfaces.TooltipOwner import TooltipOwner
import Utility, Graphics, pygame

"""
An abstract button that can be toggled on and off, which yields visual differences.
imageA -> toggled off
imageB -> toggled off but hovered
imageC -> toggled on
"""
class ToggleButton(AbstactButton, TooltipOwner):

    def __init__(self, position: tuple, imageName: str, imageScale: float = 1, optionalDisabledImageName: str = None):
        
        self.imageC = Graphics.getImage(imageName, imageScale)
        self.imageB = Graphics.getLighterImage(self.imageC, 0.66)

        if optionalDisabledImageName is None:
            self.imageA = Graphics.getLighterImage(self.imageC, 0.33)
        else: 
            disabledImage = Graphics.getImage(optionalDisabledImageName, imageScale)
            self.imageA = Graphics.getLighterImage(disabledImage, 0.33)

        super().__init__(position, self.imageC.get_width(), self.imageC.get_height())

    # Return whether object was toggled on
    @abstractmethod
    def isToggled(self) -> bool:
        pass

    # Whether the object is disabled from being toggled on, and thus also does not change color when hovering
    @abstractmethod
    def isDisabled(self) -> bool:
        pass

    # Implementing Clickable function
    # When clicked AND not disabled, then call toggleButtonOn()
    def click(self):
        if not self.isDisabled():
            self.toggleButtonOn()

    # The action to do when the button is toggled on
    @abstractmethod
    def toggleButtonOn(self) -> None:
        pass

    # Implementing abstract method
    def getImage(self) -> pygame.Surface:
        if self.isToggled():
            return self.imageC
        else:
            return self.imageB if (self.isHovering and not self.isDisabled()) else self.imageA
