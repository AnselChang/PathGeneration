from ctypes import sizeof
from SingletonState.ReferenceFrame import PointRef, VectorRef, Ref
from SingletonState.FieldTransform import FieldTransform
import pygame, Graphics, colors

"""
Storing the relative coordinates of the shapes associated with the robot sprite (square + 2 wheels)
Draws the robot given a PointRef as the center of the robot
"""

class RobotDrawing:

    def __init__(self, transform: FieldTransform, size: float):


        self.topleft = VectorRef(transform, Ref.FIELD, (-size/2,-size/2))
        self.size = VectorRef(transform, Ref.FIELD, (size, size))

        WHEEL_HEIGHT = 3
        WHEEL_WIDTH = 1
        self.wheelSize = VectorRef(transform, Ref.FIELD, (WHEEL_HEIGHT,WHEEL_HEIGHT))
        
        self.leftWheel = VectorRef(transform, Ref.FIELD, (-size/2, -WHEEL_HEIGHT/2))
        self.rightWheel = VectorRef(transform, Ref.FIELD, (size/2 - WHEEL_WIDTH/2, -WHEEL_HEIGHT/2))


    # Draw the robot centered around the center PointRef onto the screen
    def draw(self, screen: pygame.Surface, center: PointRef):

        # Draw robot
        topleft = (center + self.topleft).screenRef
        size = self.size.screenRef
        pygame.draw.rect(screen, (200,200,200), (*topleft, *size))

        # Draw left wheel
        wheelsize = self.wheelSize.screenRef
        leftwheel = (center + self.leftWheel).screenRef
        pygame.draw.rect(screen, (100,100,100), (*leftwheel, *wheelsize))

        # Draw right wheel
        rightwheel = (center + self.rightWheel).screenRef
        pygame.draw.rect(screen, (100,100,100), (*rightwheel, *wheelsize))


