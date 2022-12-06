import pygame, Utility
from SingletonState.ReferenceFrame import PointRef
from SingletonState.FieldTransform import FieldTransform
    
"""A class that encapsulates all the mouse and keyboard input into one object.
It handles all events and stores things like whether the left mouse button was pressed.
To use, call getUserInput() at the beginning of every tick to read user input events, then this object's data
can be read for the rest of the fraame
"""

# Buttons
_LEFT = 1
_RIGHT = 3

class UserInput:
    def __init__(self, pygameMouseObject, pygameKeyObject):
        
        # Singleton state objects
        self._mouse = pygameMouseObject
        self._key = pygameKeyObject

        # Position of the mouse in both screen and field reference frames
        self.mousePosition = PointRef()
        self.isMouseOnField = True # whether mouse is on the field, as opposed to the panel

        # Key that was just pressed this frame
        self.keyJustPressed = None
        
        # Amount of shift on the mousewheel
        self.mousewheelDelta = 0

        # The file object if a loaded file was dragged onto the screen this frame
        self.loadedFile = None

        # If the quit button was dragged onto the screen
        self.isQuit = False

        # For left/right mouse button pressing/releasing
        self.leftPressed = False
        self.rightPressed = False
        self.mouseReleased = False
        self.isMousePressing = False

        # Used to compare mouse press and mouse release positions to determine if a mouse release constitutes a "click"
        self._mousePressPosition = (0,0)
        self._lastMousePress = _LEFT

        # Clicking is defined as press then release without movement of mouse position
        self.leftClicked = False
        self.rightClicked = False
        

    # return whether the key is currently being pressed. The key parameter is a pygame key constant
    def isKeyPressing(self, key):
        return self._key.get_pressed()[key]

    # return whether the key has just been pressed (rising edge)
    def isKeyPressed(self, key):
        return self.keyJustPressed == key

    # Reset user input state at the start of each frame
    def resetState(self):
        self.keyJustPressed = None
        self.isQuit = False

        self.mousewheelDelta = 0

        self.leftPressed = False
        self.rightPressed = False

        self.leftClicked = False
        self.rightClicked = False

        self.mouseReleased = False

        self.loadedFile = None

    # Update the UserInput state machine. keyJustPressed is the key pressed starting in this frame, or None if none exists.
    # Call this at the start of every frame
    def getUserInput(self):

        # handle events
        self.resetState()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.isQuit = True
            elif event.type == pygame.KEYDOWN:
                self.keyJustPressed = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:

                ctrlKey: bool= self.isKeyPressing(pygame.K_LCTRL) or self.isKeyPressing(pygame.K_RCTRL)

                # Determine if it was a left or right press and update which mouse button was pressed.
                # Store position to be able to see if, when the mouse is released, it constitutes a "click"
                if (event.button == _LEFT and ctrlKey) or event.button == _RIGHT:
                    self._lastMousePress = _RIGHT
                    self.rightPressed = True
                    self._mousePressPosition = self._mouse.get_pos()
                elif event.button == _LEFT:
                    self._lastMousePress = _LEFT
                    self.leftPressed = True
                    self._mousePressPosition = self._mouse.get_pos()
                else:
                    self._lastMousePress = None
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseReleased = True

                # If the mouse button was pressed and released at roughly the same location, that constitutes a click
                if (Utility.distanceTuples(self._mouse.get_pos(), self._mousePressPosition)) < 5:
                    if self._lastMousePress == _RIGHT:
                        self.rightClicked = True
                    elif self._lastMousePress == _LEFT:
                        self.leftClicked = True
                self._lastMousePress = None

            elif event.type == pygame.MOUSEWHEEL:
                self.mousewheelDelta = event.y
            elif event.type == pygame.DROPFILE and event.file is not None:
                self.loadedFile = str(event.file)

        # Update mouse position
        self.isMousePressing = self._mouse.get_pressed()[0]
        self.mousePosition.screenRef = self._mouse.get_pos()
        self.isMouseOnField = self.mousePosition.screenRef[0] < Utility.SCREEN_SIZE
