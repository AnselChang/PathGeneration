from Interfaces.Clickable import Clickable
import pygame

"""
An visual button class that appears on the panel. It switches between "hovered" and "non-hovered" versions
of the image depending on where the mouse is. It can be clicked, which results in click() being called.

This abstract class can be subclassed to give functionality to click().
"""

class Button(Clickable):

    def __init__(self, hoveredImage: pygame.Surface, nonhoveredImage: pygame.Surface, position: tuple):

        super().__init__()

        self.hoveredImage = hoveredImage
        self.nonhoveredImage = nonhoveredImage

        # Buttons are always relative to the screen, not the field, so we don't need to make use of PointRefs
        self.position = position

    # Draw either the hovered or nonhovered version of the image based on self.isHovering inherited from Hoverable
    def draw(self, screen: pygame.Surface):
        screen.blit(self.hoveredImage if self.isHovering else self.nonhoveredImage, self.position)

    