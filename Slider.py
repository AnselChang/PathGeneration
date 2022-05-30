import Utility

SLIDER_WIDTH = 250
SLIDER_MARGIN = 60

m = None

def init(M):
    global m
    m = M

class Slider:

    def __init__(self):
        self.rightX = Utility.SCREEN_SIZE - SLIDER_MARGIN
        self.leftX = self.rightX - SLIDER_WIDTH
        self.x = self.leftX
        self.y = self.rightX
        self.high = 1
        self.pointIndex = 0

    def setRange(self, simulationLength):
        self.high = simulationLength - 1

    def mouseHovering(self):
        # Only hovering when slider is actually shown (in simulation)
        if not m.simulating:
            return False
        
        return m.x >= self.leftX - 5 and m.x <= self.rightX + 5 and abs(m.y - self.y) < 10

    def updateXFromIndex(self):
        self.x = self.leftX + (self.pointIndex / self.high) * SLIDER_WIDTH

    def incrementPossibly(self, m):

        if m.simulating and m.playingSimulation:
            if self.pointIndex == self.high:
                m.playingSimulation = False
            else:
                self.pointIndex += 1
                self.updateXFromIndex()

    def reset(self):
        self.pointIndex = 0
        self.updateXFromIndex()

    def handleMouse(self):

        if m.pressed and self.mouseHovering():
            m.draggingSlider = True

        if not m.pressing:
            m.draggingSlider = False

        if m.draggingSlider:
            m.playingSimulation = False
            x = min(self.rightX, max(self.leftX, m.x)) - self.leftX
            self.pointIndex = round(self.high * x / SLIDER_WIDTH)
            self.updateXFromIndex()
        
    def draw(self, screen):

        # Do not draw if not simulating
        if not m.simulating:
            return
        
        # Draw slider line
        corner = Utility.SCREEN_SIZE - SLIDER_MARGIN
        Utility.drawRoundedLine(screen, Utility.BLACK, corner - SLIDER_WIDTH, corner, corner, corner, 10)

        # Draw slider knob
        Utility.drawCircle(screen, self.x, self.y, Utility.BLACK, 10)
