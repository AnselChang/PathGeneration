from Simulation.HUDGraphics.HUDGraphics import HUDGraphics
from SingletonState.ReferenceFrame import PointRef
from SingletonState.ReferenceFrame import VectorRef
import pygame
import Graphics, colors

"""
HUD Graphics related to the pure pursuit controller.
Currently, displays only the position of the lookahead
"""

class AnselGraphics(HUDGraphics):

    def __init__(self, closest: PointRef, target: PointRef):
        self.closest = closest
        self.target = target

    def draw(self, screen: pygame.Surface):
        
        Graphics.drawCircle(screen, *self.closest.screenRef, colors.BLUE, 4)
        Graphics.drawCircle(screen, *self.target.screenRef, colors.RED, 4)