from MouseInterfaces.Draggable import Draggable
import pygame



class Slider(Draggable):
    # TODO Margaret write code here
    # TODO make sure to implement all the Draggable methods!

    # Set the minimum and maximum bounds, inclusive, of the controlled value
    def setBounds(minimum: float, maximum: float):
        # TODO
        pass

    # Get the current slider value
    # If the bounds and step size are integers, should return an integer. Otherwise return float
    def getValue(self):
        # TODO
        pass

    # Manually override the slider position. One example would when playing a simulation, and the slider moves by itself
    def setValue(self):
        # TODO
        pass

    # Draw slider on surface
    def draw(self, screen: pygame.Surface):
        # TODO
        pass
        