from MouseInterfaces.Clickable import Clickable
from abc import abstractmethod
from SingletonState.UserInput import UserInput
import Utility, pygame

"""
An visual button class that appears on the panel. It switches between "hovered" and "non-hovered" versions
of the image depending on where the mouse is. It can be clicked, which results in click() being called.

This abstract class can be subclassed to give functionality to click().
"""

class Button(Clickable):

    def __init__(self, position: tuple, imageWidth: int, imageHeight: int):

        super().__init__()

        # Buttons are always relative to the screen, not the field, so we don't need to make use of PointRefs
        self.position = position
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.margin = 1

    # Implementing Hoverable method
    # Return whether mouse is hovering over button using position and dimensions of image
    def checkIfHovering(self, userInput: UserInput) -> bool:
        mouseX, mouseY = userInput.mousePosition.screenRef
        dx, dy = mouseX - self.position[0], mouseY - self.position[1]
        
        if dx >= -self.margin and dx <= self.imageWidth + self.margin:
            if dy >= -self.margin and dy <= self.imageHeight + self.margin:
                return True
        return False

    # Get the image surface to draw it
    @abstractmethod
    def getImage(self) -> pygame.Surface:
        pass

    # Draw either the hovered or nonhovered version of the image based on self.isHovering inherited from Hoverable
    def draw(self, screen: pygame.Surface):
        screen.blit(self.getImage(), self.position)

"""
An abstract button that can be toggled on and off, which yields visual differences.
imageA -> toggled off
imageB -> toggled off but hovered
imageC -> toggled on
"""
class ToggleButton(Button):

    def __init__(self, position: tuple, imageName: str, imageScale: float = 1):
        
        self.imageC = Utility.getImage(imageName, imageScale)
        self.imageB = Utility.getLighterImage(self.imageC, 0.66)
        self.imageA = Utility.getLighterImage(self.imageC, 0.33)

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
