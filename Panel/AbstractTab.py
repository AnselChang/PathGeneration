from abc import ABC, abstractmethod
from MouseInterfaces.Hoverable import Hoverable
import pygame
from typing import Iterator


"""
An interface that defines the methods needed to integrate UI into a tab (aka mode)
"""

class AbstractTab(ABC):

    # By default, nothing happens when handling keyboard import. Subclasses may overload this
    def handleKeyboardInput(self, keyJustPressed):
        pass

    # A generator for all the hoverable UI objects
    @abstractmethod
    def getHoverables(self) -> Iterator[Hoverable]:
        pass

    # Draw all the UI onto the screen
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass