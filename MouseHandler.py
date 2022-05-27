import pygame

class Mouse:
    def __init__(self, mouse, key):
        self.mouse = mouse
        self.key = key
        
        self.prevPressed = False
        self.pressing = False
        self.pressed = False
        self.released = False

        self.prevPressedR = False
        self.pressingR = False
        self.pressedR = False
        self.releasedR = False
        
        self.x = -1
        self.y = -1

        self.poseDragged  = None
        self.poseSelectHeading = None
        self.keyX = False
        self.keyC = False
        self.keyCPressed = False

        self.startDragX = -1
        self.startDragY = -1
        

    def tick(self):

        ctrl = self.key.get_pressed()[pygame.K_LCTRL] or self.key.get_pressed()[pygame.K_RCTRL]
        

        self.prevPressed = self.pressing
        self.pressing = self.mouse.get_pressed()[0]

        self.prevPressedR = self.pressingR
        self.pressingR = self.mouse.get_pressed()[1]
        
        self.x, self.y = self.mouse.get_pos()
        self.pressed = self.pressing and not self.prevPressed
        self.released = not self.pressing and self.prevPressed
        self.pressedR = (self.pressingR and not self.prevPressedR) or (self.pressed and ctrl)
        self.releasedR = not self.pressingR and self.prevPressedR or (self.released and ctrl)
        if ctrl:
            self.pressed = False
            self.released = False

            

        # keyboard
        self.keyX = self.key.get_pressed()[pygame.K_x]
        self.pressedC = self.key.get_pressed()[pygame.K_c] and not self.keyC
        self.keyC = self.key.get_pressed()[pygame.K_c]
        self.keyZ = self.key.get_pressed()[pygame.K_z]


        

    
