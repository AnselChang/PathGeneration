import pygame, Utility, PointRef, FieldTransform
    

class UserInput:
    def __init__(self, transform: FieldTransform.FieldTransform, pygameMouseObject, pygameKeyObject):
        
        # Singleton state objects
        self._mouse = pygameMouseObject
        self._key = pygameKeyObject
        self._transform = transform

        # Position of the mouse in both screen and field reference frames
        self._mousePosition = PointRef.PointRef(self._transform)

        # Key that was just pressed this frame
        self.keyJustPressed = None

        # For left/right mouse button pressing/releasing
        self._isCtrlPressing = False
        self.pressingLeft = False
        self.pressingRight = False
        self.pressingLeftPrevious = False
        self.pressingRightPrevious = False

        # old state stuff that hasn't been refactored yet
        self.poseDragged  = None
        self.scrolling = False
        self.simulating = False
        self.playingSimulation = False
        self.draggingSlider = False
        
    # Get the mouse coordinates from the screen reference frame
    def mouseScreenRef(self) -> tuple:
        return self._mousePosition.screenRef

    # Get the mouse coordinates from the field reference frame
    def mouseFieldRef(self) -> tuple:
        return self._mousePosition.fieldRef

    # return whether the key is currently being pressed. The key parameter is a pygame key constant
    def isKeyPressing(self, key):
        return self.key.get_pressed()[key]

    # return whether the key has just been pressed (rising edge)
    def isKeyPressed(self, key):
        return self.keyJustPressed == key

    # If the left mouse button was just pressed on this frame
    def isMousePressedLeft(self):
        return not self._isCtrlPressing and self.pressingLeft and not self.pressingLeftPrevious

    # If the right mouse button was just pressed on this frame
    def isMousePressedRight(self):
        controlClick = self._isCtrlPressing and self.pressingLeft and not self.pressingLeftPrevious
        return controlClick or self.pressingRight and not self.pressingRightPrevious

    # If the left mouse button was just released on this frame
    def isMouseReleasedLeft(self):
        return not self.pressingLeft and self.pressingLeftPrevious    

    # Update the UserInput state machine. keyJustPressed is the key pressed starting in this frame, or None if none exists.
    # Call this at the start of every frame
    def getUserInput(self, keyJustPressed):

        # Update mouse position
        self._mousePosition.screenRef = self._mouse.get_pos()

        # Update  key just pressed
        self.keyJustPressed = keyJustPressed

        # Update left aand right mouse that just got clicked or release
        self._isCtrlPressing = self.isKeyPressing(pygame.K_LCTRL) or self.isKeyPressing(pygame.K_RCTRL)
        self.pressingLeftPrevious = self.pressingLeft
        self.pressingRightPrevious = self.pressingRight
        self.pressingLeft = self._mouse.get_pressed()[0]
        self.pressingRight = self._mouse.get_pressed()[1]
        


        

    
