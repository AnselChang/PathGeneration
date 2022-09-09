from Buttons.ButtonClasses import *
from Buttons.AbstractButton import Button
from SingletonState.SoftwareState import SoftwareState
import pygame

"""
A class to initialize and store a collection of buttons
"""

class Buttons:

    def __init__(self, state: SoftwareState):
        self.buttons: Button = [
            
            EditButton(state),
            PlayButton(state),

        ]

    def draw(self, screen: pygame.Surface):
        button: Button
        for button in self.buttons:
            button.draw(screen)