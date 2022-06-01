import Utility

m = None

def init(M):
    global m
    m = M

class Slider:

    def __init__(self, x1, x2, y, low = 0, high = 100):
        self.y = y
        self.leftX = x1
        self.rightX = x2
        self.width = x2 - x1
        self.x = self.leftX

        self.low = low
        self.high = high
        self.value = 0
        self.draggingSlider = False


    def mouseHovering(self):
        # Only hovering when slider is actually shown (in simulation)
        if not m.simulating:
            return False
        
        return m.x >= self.leftX - 5 and m.x <= self.rightX + 5 and abs(m.y - self.y) < 10

    def updateXFromIndex(self):
        self.x = self.leftX + ((self.value - self.low) / (self.high - self.low)) * (self.width)

    def reset(self):
        self.value = 0
        self.updateXFromIndex()

    def handleMouse(self):

        if m.pressed and self.mouseHovering():
            self.draggingSlider = True

        if not m.pressing:
            self.draggingSlider = False

        if self.draggingSlider:
            x = min(self.rightX, max(self.leftX, m.x)) - self.leftX
            self.value = self.low + round((self.high - self.low) * x / self.width)
            self.updateXFromIndex()
        
    def draw(self, screen):

        # Do not draw if not simulating
        if not m.simulating:
            return
        
        # Draw slider line
        Utility.drawRoundedLine(screen, Utility.BLACK, self.leftX, self.y, self.rightX, self.y, 10)

        # Draw slider knob
        Utility.drawCircle(screen, self.x, self.y, Utility.BLACK, 10)
