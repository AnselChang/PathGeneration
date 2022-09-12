from email.mime import image
from Panel.AbstractButtons.AbstractButton import AbstactButton
from abc import abstractmethod
import Utility, Graphics, pygame

"""
An abstract button that can be toggled on and off, which yields visual differences.
self.imageOn - when toggled on
self.imageOff - when toggled off
self.imageHovered - when toggled off, not disabled, and hovering
"""
class ToggleButton(AbstactButton):

    def __init__(self, position: tuple, imageOff: pygame.Surface, imageHovered: pygame.Surface, imageOn: pygame.Surface):
        
        self.imageOn = imageOn
        self.imageHovered = imageHovered
        self.imageOff = imageOff

        super().__init__(position, self.imageOn.get_width(), self.imageOn.get_height())

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
            return self.imageOn
        else:
            return self.imageHovered if (self.isHovering and not self.isDisabled()) else self.imageOff
