from AI.Disc import Disc, getAllDiscs
from AI.MCTS import MCTS
from Sliders.Slider import Slider
import Graphics, pygame, colors, Utility


class DiscManager:


    def __init__(self):

        self.initDiscs()
        
        self.mcts: MCTS = MCTS(self.discs)
        self.explorationSlider: Slider = None

    def initSlider(self, explorationSlider: Slider):
        self.explorationSlider = explorationSlider

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self) -> list[Disc]:

        self.discs: list[Disc] = getAllDiscs()

        # Pre-process by sorting each disc's distance to each other disc. O(n^2*log(n))
        for disc in self.discs:
            disc.preprocess(self.discs)

    # update disk manager things. Called every tick
    def update(self):
        
        # Get exploration slider value and update mcts process with it
        self.mcts.updateExplorationParameter(self.explorationSlider.getValue())


    # Draw each disc
    def draw(self, screen: pygame.Surface):

        # Get the disc order from self.mcts
        discOrder, totalDistance = self.mcts.get()

        if len(discOrder) > 0:

            # for slowly-changing line color between discs
            color = Graphics.ColorCycle(0.03)

            # Draw lines between each disc in the discOrder
            pos1 = discOrder[0].position.screenRef
            i = 1
            while i < len(discOrder):
                # Draw line between discOrder[i] and discOrder[i+1]
                pos2 = discOrder[i].position.screenRef
                Graphics.drawLine(screen, color.next(), *pos1, *pos2, 3)

                pos1 = pos2
                i += 1
        
                
        # Draw each disc
        for disc in self.discs:
            disc.draw(screen)

        # Display shortest distance
        text: str = "Shortest Distance: {} inches".format(round(totalDistance, 2))
        Graphics.drawText(screen, Graphics.FONT25, text, colors.BLACK, Utility.SCREEN_SIZE + 25, Utility.SCREEN_SIZE - 200, 0)

