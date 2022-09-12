from MouseInterfaces.Draggable import Draggable
from SingletonState.UserInput import UserInput
import colors
import pygame
import Graphics
import Utility

class Slider(Draggable):

    def __init__(self, x, y, width, min, max, step):
        self.x = x
        self.y = y
        self.width = width
        self.min = min
        self.max = max
        self.step = step

    def beDraggedByMouse(self, userInput: UserInput) -> bool:
        pass


    def stopDragging(self):
        pass

    def checkIfHovering(self, userInput: UserInput) -> bool:
        mouseX, mouseY = pygame.mouse.get_rel()
        return Utility.pointTouchingLine(mouseX, mouseY, self.x, self.y, self.x + self.width, self.y, 20)

    def startDragging(self, userInput: UserInput):
        pass

    # Set the minimum and maximum bounds, inclusive, of the controlled value
    def setBounds(minimum: float, maximum: float):
        self.min = minimum
        self.max = maximum

    # Get the current slider value
    # If the bounds and step size are integers, should return an integer. Otherwise return float
    def getValue(self):
        return self.val

    # Manually override the slider position. One example would when playing a simulation, and the slider moves by itself
    def setValue(self, val):
        self.val = val

    # Draw slider on surface
    def draw(self, screen: pygame.Surface):
        Graphics.drawRoundedLine(screen, colors.LINEGREY, self.x, self.y, self.x + self.width, self.y, 20)
        Graphics.drawCircle(screen, self.x + (self.val / (self.max - self.min)) * self.width, self.y, colors.LIGHTBLUE, 8)
        pass