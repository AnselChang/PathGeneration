from Simulation.HUDGraphics.HUDGraphics import HUDGraphics
from SingletonState.ReferenceFrame import PointRef
from SingletonState.ReferenceFrame import VectorRef
import pygame
import Graphics, colors

"""
HUD Graphics related to the pure pursuit controller.
Currently, displays only the position of the lookahead
"""

class PPGraphics(HUDGraphics):

    def __init__(self, robotPosition: PointRef, waypoint: PointRef, lookaheadDistance: float):
        self.position = robotPosition.copy()
        self.waypoint: PointRef = waypoint

    def draw(self, screen: pygame.Surface):
        
        Graphics.drawCircle(screen, *self.waypoint.screenRef, colors.BLUE, 4)