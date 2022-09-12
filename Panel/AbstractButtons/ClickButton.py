from email.mime import image
from Panel.AbstractButtons.AbstractButton import AbstactButton
from abc import abstractmethod
from MouseInterfaces.TooltipOwner import TooltipOwner
import Utility, Graphics, pygame

"""
An abstract button that can be clicked to call clickEnabledFunction()
This button can be enabled or disabled

self.imageEnabled -> clickable
self.imageDIsabled -> not clickable
self.hovered -> when clickable and mouse is hovering
"""
class ClickButton(AbstactButton):

    def __init__(self, position: tuple, imageDisabled: pygame.Surface, imageEnabled: pygame.Surface, imageHovered: pygame.Surface):
        
        self.imageEnabled = imageEnabled
        self.imageHovered = imageHovered
        self.imageDisabled = imageDisabled

        super().__init__(position, self.imageEnabled.get_width(), self.imageEnabled.get_height())


    # Whether the object is disabled from being toggled on, and thus also does not change color when hovering
    @abstractmethod
    def isDisabled(self) -> bool:
        pass

    # Implementing Clickable function
    # When clicked AND not disabled, then call toggleButtonOn()
    def click(self):
        if not self.isDisabled():
            self.clickEnabledButton()

    # The action to do when the button is toggled on
    @abstractmethod
    def clickEnabledButton(self) -> None:
        pass

    # Implementing abstract method
    def getImage(self) -> pygame.Surface:
        if self.isDisabled():
            return self.imageDisabled
        else:
            return self.imageHovered if self.isHovering else self.imageEnabled
