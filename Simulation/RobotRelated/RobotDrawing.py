from ctypes import sizeof
from SingletonState.ReferenceFrame import PointRef, VectorRef, Ref
from SingletonState.FieldTransform import FieldTransform
import pygame, Graphics, colors, math

"""
Storing the relative coordinates of the shapes associated with the robot sprite (square + 2 wheels)
Draws the robot given a PointRef as the center of the robot
"""

# Define a rectangle as four vectors from the center
def getRect(deltaX: float, deltaY: float, width: float, height: float):
    return (
        VectorRef(Ref.FIELD, (deltaX - width/2, deltaY - height/2)),
        VectorRef(Ref.FIELD, (deltaX + width/2, deltaY - height/2)),
        VectorRef(Ref.FIELD, (deltaX + width/2, deltaY + height/2)),
        VectorRef(Ref.FIELD, (deltaX - width/2, deltaY + height/2)),
        
    )

# Rotate the four vectors about some theta counterclockwise
def rotateRect(rect: list[VectorRef], theta: float):
    return [vector.rotate(theta) for vector in rect]

# Get the absolute points (list of (x,y)) of the rectangle given the list of vectors and the central PointRef
def getAbsolutePoints(rect: list[VectorRef], center: PointRef):
    return [(center + vector).screenRef for vector in rect]

class RobotDrawing:

    def __init__(self, size: float):

        self.robot = getRect(0, 0, size, size)

        WHEEL_HEIGHT = 1
        WHEEL_WIDTH = 3
        self.leftWheel = getRect(0, -size/2 + WHEEL_HEIGHT/2, WHEEL_WIDTH, WHEEL_HEIGHT)
        self.rightWheel = getRect(0, size/2 - WHEEL_HEIGHT/2, WHEEL_WIDTH, WHEEL_HEIGHT)

    # Draw the robot centered around the center PointRef onto the screen
    def draw(self, screen: pygame.Surface, center: PointRef, heading: float):

        robotPoints: list[tuple] = getAbsolutePoints(rotateRect(self.robot, heading), center)
        Graphics.drawPolygon(screen, (200,200,200), robotPoints)

        # Draw left wheel
        leftPoints: list[tuple] = getAbsolutePoints(rotateRect(self.leftWheel, heading), center)
        Graphics.drawPolygon(screen, (100,100,100), leftPoints)

        # Draw right wheel
        rightPoints: list[tuple] = getAbsolutePoints(rotateRect(self.rightWheel, heading), center)
        Graphics.drawPolygon(screen, (100,100,100), rightPoints)

        # Draw vector to indicate direction        
        Graphics.drawVector(screen, *center.screenRef, 10, heading)



