from email.mime import image
from Panel.AbstractButtons.AbstractButton import AbstactButton
from abc import abstractmethod
import Utility, Graphics, pygame

"""
An abstract button that can be toggled on and off, which yields visual differences.
self.imageOn - when toggled on and not hovered
self.imageOnHovered - when toggled on and hovered
self.imageOff - when toggled off and not hovered
self.imageOffHovered - when toggled off and hovered
"""
class FlipFlopButton(AbstactButton):

    def __init__(self, position: tuple, imageOff: pygame.Surface, imageOffHovered: pygame.Surface, imageOn: pygame.Surface, imageOnHovered: pygame.Surface):
        
        self.imageOffHovered = imageOffHovered
        self.imageOff = imageOff
        self.imageOn = imageOn
        self.imageOnHovered = imageOnHovered

        super().__init__(position, self.imageOn.get_width(), self.imageOn.get_height())

    # Return whether object is on
    @abstractmethod
    def isOn(self) -> bool:
        pass

    # Implementing Clickable function
    # When clicked AND not disabled, then call toggleButtonOn()
    def click(self):
        self.toggleButton()

    # The action to do when the button is toggled on
    @abstractmethod
    def toggleButton(self) -> None:
        pass

    # Implementing abstract method
    def getImage(self) -> pygame.Surface:
        if self.isOn():
            return self.imageOnHovered if self.isHovering else self.imageOn
        else:
            return self.imageOffHovered if self.isHovering else self.imageOff
