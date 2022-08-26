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
        self.selectVectorNotHeading = False
        
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


    # 19 785
    def pixelToInch(self, x, y):
        x -= self.panX
        y -= self.panY
        x /= self.zoom
        y /= self.zoom

        # x and y are now the pixels of the field. The field begins at 19 with a width of 766
        x -= 19
        y -= 19
        x /= 766
        y /= 766

        # x and y are now between 0 and 1. Field has 144 inches
        x *= 144
        y *= 144
        
        return [x, y]

    def inchToPixel(self, x, y):

        x /= 144
        y /= 144

        x *= 766
        y *= 766
        x += 19
        y += 19
        
        x *= self.zoom
        y *= self.zoom
        x += self.panX
        y += self.panY
        return [x, y]

    # return whether key is currently being pressed
    def getKey(self, k):
        return self.allKeys[k]

    def getKeyPressed(self, k):
        return k == self.keyPressed

    # To make objects grow slightly larger when zoom
    def getPartialZoom(self, scalar):
        return (self.zoom - 1) * scalar + 1

    # Restrict the panning range for the field as to keep the field in sight of the screen
    def boundFieldPan(self):
        self.panX = max(min(0, self.panX),  (1-self.zoom)*Utility.SCREEN_SIZE)
        self.panY = max(min(0, self.panY), (1-self.zoom)*Utility.SCREEN_SIZE)

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
        


        

    
