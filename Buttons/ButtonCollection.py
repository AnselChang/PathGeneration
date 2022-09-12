from Buttons.ConcreteButtons import AIButton, EditButton, OdomButton, RobotButton, SimulateButton
from Buttons.AbstractButton import AbstactButton
from SingletonState.SoftwareState import SoftwareState
from Simulation.Waypoints import Waypoints
import pygame

"""
A class to initialize and store a collection of buttons to be displayed on the panel
"""

class Buttons:

    def __init__(self, state: SoftwareState, waypoints: Waypoints):
        self.buttons: AbstactButton = [
            
            AIButton.AIButton(state),
            EditButton.EditButton(state),
            SimulateButton.SimulateButton(state, waypoints),
            RobotButton.RobotButton(state, waypoints),
            OdomButton.OdomButton(state)

        ]

    def draw(self, screen: pygame.Surface):
        button: AbstactButton
        for button in self.buttons:
            button.draw(screen)