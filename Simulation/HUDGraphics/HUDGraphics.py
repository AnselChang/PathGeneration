import pygame

"""Interface for storing graphics state for simulations for different controllers.
The object stores data for a single timestep of the simulation.
Creating an object of type HUDGraphics results in a no-op draw command.
"""

class HUDGraphics:

    def draw(self, screen: pygame.Surface):
        pass