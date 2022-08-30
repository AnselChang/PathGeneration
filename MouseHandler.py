import pygame, Utility
    

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

        self. rx = -1
        self.ry = -1
        self.x = -1
        self.y = -1

        self.prevX = 0
        self.prevY = 0

        self.poseDragged  = None
        
        self.scrolling = False
        self.simulating = False
        self.playingSimulation = False
        self.draggingSlider = False
        
        self.allKeys = None
        self.keyPressed = None

        self.startDragX = -1
        self.startDragY = -1

        self.zoom = 1
        self.panX = 0
        self.panY = 0


    # return whether key is currently being pressed
    def getKey(self, k):
        return self.allKeys[k]

    def getKeyPressed(self, k):
        return k == self.keyPressed

    # To make objects grow slightly larger when zoom
    def getPartialZoom(self, scalar):
        return (self.zoom - 1) * scalar + 1

    def tick(self, keyPressed):

        self.allKeys = self.key.get_pressed()
        self.keyPressed = keyPressed

        ctrl = self.key.get_pressed()[pygame.K_LCTRL] or self.key.get_pressed()[pygame.K_RCTRL]

        self.prevPressed = self.pressing
        self.pressing = self.mouse.get_pressed()[0]

        self.prevPressedR = self.pressingR
        self.pressingR = self.mouse.get_pressed()[1]

        # Get mouse x and y through zoom transformations
        self.prevX = self.x
        self.prevY = self.y
        self.x, self.y = self.mouse.get_pos()
        self.zx, self.zy = self.pixelToInch(self.x, self.y)
        
        self.pressed = self.pressing and not self.prevPressed
        self.released = not self.pressing and self.prevPressed
        self.pressedR = (self.pressingR and not self.prevPressedR) or (self.pressed and ctrl)
        self.releasedR = not self.pressingR and self.prevPressedR or (self.released and ctrl)
        if ctrl:
            self.pressed = False
            self.released = False
        


        

    
