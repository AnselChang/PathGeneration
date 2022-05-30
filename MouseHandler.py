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
        self.poseSelectHeading = None
        
        self.scrolling = False
        self.simulating = False
        
        self.keyX = False
        self.keyC = False
        self.keyZ = False
        self.pressedSpace = False
        self.keySpace = False
        self.pressedC = False

        self.startDragX = -1
        self.startDragY = -1

        self.zoom = 1
        self.panX = 0
        self.panY = 0

        self.lastToggledEdge = -1


    def pixelToInch(self, x, y):
        x -= self.panX
        y -= self.panY
        return [x / self.zoom, y / self.zoom]

    def inchToPixel(self, x, y):
        x *= self.zoom
        y *= self.zoom
        return [x + self.panX, y + self.panY]

    def getKey(self, k):
        return self.allKeys[k]

    # To make objects grow slightly larger when zoom
    def getPartialZoom(self, scalar):
        return (self.zoom - 1) * scalar + 1

    def boundFieldPan(self):
        self.panX = max(min(0, self.panX),  (1-self.zoom)*Utility.SCREEN_SIZE)
        self.panY = max(min(0, self.panY), (1-self.zoom)*Utility.SCREEN_SIZE)

    def tick(self):

        self.allKeys = self.key.get_pressed()

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

        # keyboard
        self.keyX = self.getKey(pygame.K_x)
        self.pressedC = self.getKey(pygame.K_c) and not self.keyC
        self.keyC = self.getKey(pygame.K_c)
        self.keyZ = self.getKey(pygame.K_z)
        self.pressedSpace = self.getKey(pygame.K_SPACE) and not self.keySpace
        self.keySpace = self.getKey(pygame.K_SPACE)
        


        

    
