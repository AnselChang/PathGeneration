from MouseInterfaces.Draggable import Draggable
from SingletonState.UserInput import UserInput
from SingletonState.SoftwareState import SoftwareState, Mode
from RobotSpecs import RobotSpecs
import pygame, Utility, Graphics

"""
A GUI panel that both visualizes the velocity of the robot, and allows the user to control the desired velocity

At the leftmost point, wheel velocities are at (-V, V)
At the center point, wheel velocities are at (V, V)
At the rightmost point, wheel velocities are at (V, -V)

At the topmost, center, and bottom-most points, V is at maximumVelocity, 0, and -maximumVelocity respectively

ALL VELOCITIES ARE STORED AS A PERCENT FROM 0-1! To get the actual velocity, multiply by maximumVelocity

At each frame, setDesiredVelocity() and setActualVelocity() determine where the desiredVelocity and actualVelocity
points are drawn

In addition, in user input mode, the class is draggable and can set desired velocity from dragging the mouse
"""

# colors
PANEL_RED = (235, 60, 60)
PANEL_RED_HOVERED = (235, 73, 73)
GRID = (235, 100, 100)
ACTUAL = (97, 207, 117)
ACTUAL2 = (125, 221, 166)
DESIRED = (95, 85, 251)
DESIRED2 = (120,110,254)


class VelocityGUI(Draggable):

    def __init__(self, robotSpecs: RobotSpecs, state: SoftwareState):

        self.maximumVelocity = robotSpecs.maximumVelocity
        self.state: SoftwareState = state

        self.desired: tuple = (0,0) # desired percent velocity from [-1, 1]
        self.actual: tuple = (0,0) # desired actual veloctiy from [-1, 1]

        self.showDesired = False
        self.showActual = False

        MARGIN = 20
        self.PADDING = 5
        self.x = Utility.SCREEN_SIZE + MARGIN + 2
        self.width = Utility.PANEL_WIDTH - MARGIN*2

        self.height = 150
        self.y = Utility.SCREEN_SIZE - MARGIN - self.height

        super().__init__()

    # Set the desired percent of velocity with domain [-1, 1], to be drawn on the gui
    def setDesiredPercent(self, left: float, right: float):
        self.desired = Utility.clamp(left, -1, 1), Utility.clamp(right, -1, 1)
        self.showDesired = True

    # Set the actual percent of velocity with domain [-1, 1], to be drawn on the gui
    def setActualPercent(self, left: float, right: float):
        self.actual = Utility.clamp(left, -1, 1), Utility.clamp(right, -1, 1)
        self.showActual = True

    # Set desired velocity and convert to percent
    def setDesiredVelocity(self, leftVelocity: float, rightVelocity: float):
        self.setDesiredPercent(leftVelocity / self.maximumVelocity, rightVelocity / self.maximumVelocity)

    # Set actual velocity and convert to percent
    def setActualVelocity(self, leftVelocity: float, rightVelocity: float):
        self.setActualPercent(leftVelocity / self.maximumVelocity, rightVelocity / self.maximumVelocity)

    # Called to determine if the mouse is touching this object (and if is the first object touched, would be considered hovered)
    def checkIfHovering(self, userInput: UserInput) -> bool:

        # can only interact with mouse in odometry mode
        if self.state.mode != Mode.ODOM:
            return False

        mx, my = userInput.mousePosition.screenRef
        return mx >= self.x and mx <= self.x + self.width and my >= self.y and my <= self.y + self.height

    # Called when the object was just pressed at the start of a drag
    def startDragging(self, userInput: UserInput):
        pass

    # Called every frame that the object is being dragged. Most likely used to update the position of the object based
    # on where the mouse is
    def beDraggedByMouse(self, userInput: UserInput):
        pass

    # Callback when the dragged object was just released
    def stopDragging(self):
        pass

    def draw(self, screen: pygame.Surface):

        # Draw gui
        color = PANEL_RED_HOVERED if self.isHovering else PANEL_RED
        Graphics.drawRoundedRectangle(screen, (self.x-self.PADDING, self.y-self.PADDING, self.width+self.PADDING*2, self.height+self.PADDING*2), color, 10)

        # Draw axes
        midX = self.x + self.width/2
        midY = self.y + self.height/2
        Graphics.drawLine(screen, GRID, midX, self.y-self.PADDING, midX, self.y + self.height+self.PADDING, 2)
        Graphics.drawLine(screen, GRID, self.x-self.PADDING, midY, self.x + self.width+self.PADDING, midY, 2)

        # Draw actual point on gui
        if self.showActual:
            actualX = self.x + self.width/2 + (self.width/2) * self.actual[0]
            actualY = self.y + self.height/2 + (self.height/2) * self.actual[1]
            Graphics.drawCircle(screen, actualX, actualY, ACTUAL2, 10)
            Graphics.drawCircle(screen, actualX, actualY, ACTUAL, 7)
            
            self.showActual = False

        # Draw desired point on gui (on top of actual possibly)
        if self.showDesired:
            desiredX = self.x + self.width/2 + (self.width/2) * self.desired[0]
            desiredY = self.y + self.height/2 + (self.height/2) * self.desired[1]
            Graphics.drawCircle(screen, desiredX, desiredY, DESIRED2, 10)
            Graphics.drawCircle(screen, desiredX, desiredY, DESIRED, 7)
            self.showDesired = False

