from abc import ABC, abstractmethod
from SingletonState.ReferenceFrame import PointRef
import pygame

"""
Classes with the TooltipOwner interface have a tooltip when the mouse is hovered over. Those classes
must implement drawTooltip() which calls the tooltip object's draw() method
"""

class TooltipOwner(ABC):

    # Classes implementing TooltipOwner must implement this and draw the tooltip
    @abstractmethod
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        pass