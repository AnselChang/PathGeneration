from Graphics import *
import Utility

class SimulationAnaysis:
    def __init__(self):
        self.positionErrorAvg =  0
        self.headingErrorAvg = 0
        self.numTicks = 0
    
    def tickError(self, posError: float, headingError: float):
        self.positionErrorAvg = (self.positionErrorAvg*self.numTicks+posError)/(self.numTicks+1)
        self.headingErrorAvg = (self.headingErrorAvg*self.numTicks+headingError)/(self.numTicks+1)
        self.numTicks += 1

    def draw(self, surface: pygame.Surface):
        posString = "Average Position Error: "+self.positionErrorAvg
        headString = "Average Position Error: "+self.headingErrorAvg
        # Print centered on the panel, halfway down the screen
        drawText(surface, font=FONT20, string=posString, 
            x=Utility.FIELD_SIZE_IN_PIXELS+Utility.PANEL_WIDTH/2, y=Utility.SCREEN_SIZE/2)
        drawText(surface, font=FONT20, string=headString, 
            x=Utility.FIELD_SIZE_IN_PIXELS+Utility.PANEL_WIDTH/2, y=Utility.SCREEN_SIZE/2+25)