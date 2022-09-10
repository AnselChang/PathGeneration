from Buttons.ConcreteButtons import EditButton, OdomButton, RobotButton, SimulateButton
from Buttons.AbstractButton import AbstactButton
from SingletonState.SoftwareState import SoftwareState
import pygame

"""
A class to initialize and store a collection of buttons to be displayed on the panel
"""

class Buttons:

    def __init__(self, state: SoftwareState):
        self.buttons: AbstactButton = [
            
            EditButton.EditButton(state),
            SimulateButton.SimulateButton(state),
            RobotButton.RobotButton(state),
            OdomButton.OdomButton(state)

        ]

    def draw(self, screen: pygame.Surface):
        button: AbstactButton
        for button in self.buttons:
            button.draw(screen)