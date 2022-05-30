import Utility

SLIDER_WIDTH = 150
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

    def mouseHovering(self):
        # Only hovering when slider is actually shown (in simulation)
        if not m.simulating:
            return False
        
        return m.x >= self.leftX - 5 and m.x <= self.rightX + 5 and abs(m.y - self.y) < 10

    def goToX(self, x):
        self.x = min(self.rightX, max(self.leftX, x))
        
    def draw(self, screen):

        # Do not draw if not simulating
        if not m.simulating:
            return
        
        # Draw slider line
        corner = Utility.SCREEN_SIZE - SLIDER_MARGIN
        Utility.drawRoundedLine(screen, Utility.BLACK, corner - SLIDER_WIDTH, corner, corner, corner, 10)

        # Draw slider knob
        Utility.drawCircle(screen, self.x, self.y, Utility.BLACK, 10)
