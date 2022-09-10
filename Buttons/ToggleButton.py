from Buttons.AbstractButton import AbstactButton
from abc import abstractmethod
import Utility, Graphics, pygame

"""
An abstract button that can be toggled on and off, which yields visual differences.
imageA -> toggled off
imageB -> toggled off but hovered
imageC -> toggled on
"""
class ToggleButton(AbstactButton):

    def __init__(self, position: tuple, imageName: str, imageScale: float = 1):
        
        self.imageC = Graphics.getImage(imageName, imageScale)
        self.imageB = Graphics.getLighterImage(self.imageC, 0.66)
        self.imageA = Graphics.getLighterImage(self.imageC, 0.33)

        super().__init__(position, self.imageC.get_width(), self.imageC.get_height())

    # Return whether object was toggled on
    @abstractmethod
    def isToggled(self) -> bool:
        pass

    # Implementing abstract method
    def getImage(self) -> pygame.Surface:
        if self.isToggled():
            return self.imageC
        else:
            return self.imageB if self.isHovering else self.imageA
