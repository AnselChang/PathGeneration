import pygame, Utility, PointRef
from FieldTransform import FieldTransform
    

class UserInput:
    def __init__(self, transform: FieldTransform, pygameMouseObject, pygameKeyObject):
        
        # Singleton state objects
        self._mouse = pygameMouseObject
        self._key = pygameKeyObject
        self._transform = transform

        # Position of the mouse in both screen and field reference frames
        self.mousePosition = PointRef.PointRef(self._transform)

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
        

    # return whether the key is currently being pressed. The key parameter is a pygame key constant
    def isKeyPressing(self, key):
        return self.key.get_pressed()[key]

    # return whether the key has just been pressed (rising edge)
    def isKeyPressed(self, key):
        return self.keyJustPressed == key


    # Update the UserInput state machine. keyJustPressed is the key pressed starting in this frame, or None if none exists.
    # Call this at the start of every frame
    def getUserInput(self):

        # handle events
        self.keyJustPressed = None
        self.isQuit = False
        self.mousewheelDelta = 0
        self.leftPressed = False
        self.rightPressed = False
        self.mouseReleased = False
        self.loadedFile = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isQuit = True
            elif event.type == pygame.KEYDOWN:
                self.keyJustPressed = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Control key pressed for right click
                if self.isKeyPressing(pygame.K_LCTRL) or self.isKeyPressing(pygame.K_RCTRL):
                    self.rightPressed = True
                else:
                    self.leftPressed = True
            elif event.type == pygame.MOUSEWHEEL:
                self.mousewheelDelta = event.y
            elif event.type == pygame.DROPFILE:
                self.loadedFile = event.file

        # Update mouse position
        self.mousePosition.screenRef = self._mouse.get_pos()

        

    
