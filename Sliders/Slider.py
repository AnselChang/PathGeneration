from MouseInterfaces.Draggable import Draggable
from SingletonState.UserInput import UserInput
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
from MouseInterfaces.TooltipOwner import TooltipOwner
import colors, pygame, Graphics, Utility

from typing import Callable

"""
A visual slider with customizable position, range of value, and step
does not implement Tooltip owner because of custom functionality where tooltip if DRAGGING
"""


class Slider(Draggable, TooltipOwner):

    def __init__(self, x: int, y: int, width: int, min: float, max: float, step: float, color: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.min = min
        self.max = max
        self.step = step
        self.color = color

        self.setValue(self.min)

        super().__init__()

    def beDraggedByMouse(self, userInput: UserInput) -> bool:
        mouseX, mouseY = userInput.mousePosition.screenRef
        self.setValue(round((mouseX - self.x) / self.width * (self.max - self.min) / self.step) * self.step)

        return True

    def stopDragging(self):
        pass

    def checkIfHovering(self, userInput: UserInput) -> bool:
        mouseX, mouseY = userInput.mousePosition.screenRef
        return Utility.pointTouchingLine(mouseX, mouseY, self.x - 10, self.y, self.x + self.width + 10, self.y, 10)

    def startDragging(self, userInput: UserInput):
        pass

    # Set the minimum and maximum bounds, inclusive, of the controlled value
    def setBounds(self, minimum: float, maximum: float):
        self.min = minimum
        self.max = maximum

    # Get the current slider value
    # If the bounds and step size are integers, should return an integer. Otherwise return float
    def getValue(self):
        if round(self.val) == self.val:
            return int(self.val)
        else:
            return self.val

    # Manually override the slider position. One example would when playing a simulation, and the slider moves by itself
    def setValue(self, val: float):
        self.val = Utility.clamp(val, self.min, self.max)
        self.tooltip = Tooltip(str(self.val))

    def getCircleX(self) -> int:
        return self.x + ((self.val - self.min) / (self.max - self.min)) * self.width

    # Draw slider on surface
    def draw(self, screen: pygame.Surface):
        Graphics.drawRoundedLine(screen, colors.LINEGREY, self.x, self.y, self.x + self.width, self.y, 20)
        Graphics.drawCircle(screen, self.getCircleX(), self.y, self.color, 8)

    # Draw tooltip for value
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:

        self.tooltip.draw(screen, (mousePosition[0], self.y - 58))
        