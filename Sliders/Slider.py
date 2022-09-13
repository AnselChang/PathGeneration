from MouseInterfaces.Draggable import Draggable
from SingletonState.UserInput import UserInput
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
from MouseInterfaces.TooltipOwner import TooltipOwner
import colors
import pygame
import Graphics
import Utility

class Slider(Draggable, TooltipOwner):

    def __init__(self, x, y, width, min, max, step, color, updateAfterDrag, callback):
        self.x = x
        self.y = y
        self.width = width
        self.min = min
        self.max = max
        self.step = step
        self.color = color
        self.updateAfterDrag = updateAfterDrag
        self.callback = callback

    def beDraggedByMouse(self, userInput: UserInput) -> bool:
        mouseX, mouseY = userInput.mousePosition.screenRef
        self.setValue(round((mouseX - self.x) / self.width * (self.max - self.min) / self.step) * self.step)

        if not self.updateAfterDrag:
            self.callback(self.val)

        return True

    def stopDragging(self):
        self.callback(self.val)
        self.tooltip = Tooltip(str(self.val))

    def checkIfHovering(self, userInput: UserInput) -> bool:
        mouseX, mouseY = userInput.mousePosition.screenRef
        return Utility.pointTouchingLine(mouseX, mouseY, self.x - 10, self.y, self.x + self.width + 10, self.y, 10)

    def startDragging(self, userInput: UserInput):
        self.tooltip = Tooltip(str(self.val))

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
        self.val = Utility.clamp(val, self.min, self.max)
        self.tooltip = Tooltip(str(self.val))

    # Draw slider on surface
    def draw(self, screen: pygame.Surface):
        Graphics.drawRoundedLine(screen, colors.LINEGREY, self.x, self.y, self.x + self.width, self.y, 20)
        Graphics.drawCircle(screen, self.x + ((self.val - self.min) / (self.max - self.min)) * self.width, self.y, self.color, 8)
        pass

    def drawTooltip(self, screen: pygame.Surface, mousePosition: PointRef) -> None:
        self.tooltip.draw(screen, mousePosition)