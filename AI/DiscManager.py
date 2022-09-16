from SingletonState.FieldTransform import FieldTransform
from AI.Disc import Disc, getAllDiscs
from AI.MCTS import MCTS
import Graphics, pygame


class DiscManager:


    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)
        
        self.mcts: MCTS = MCTS(self.discs)

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self, transform: FieldTransform) -> list[Disc]:

        Disc.transform = transform
        self.discs: list[Disc] = getAllDiscs()

        # Pre-process by sorting each disc's distance to each other disc. O(n^2*log(n))
        for disc in self.discs:
            disc.preprocess(self.discs)

    # Run MCTS
    def runMCTS(self, iterations = 10000):
        self.mcts.run(iterations)

    # Draw each disc
    def draw(self, screen: pygame.Surface):

        # Get the disc order from self.mcts
        discOrder, totalDistance = self.mcts.getBestPath()

        # for slowly-changing line color between discs
        color = Graphics.ColorCycle(0.03)

       # Draw lines between each disc in the discOrder
        i = 0
        while i < len(discOrder) - 1:
            # Draw line between discOrder[i] and discOrder[i+1]
            pos1 = discOrder[i].position.screenRef
            pos2 = discOrder[i+1].position.screenRef
            Graphics.drawLine(screen, color.next(), *pos1, *pos2, 3)
            i += 1

        # Draw each disc
        for disc in self.discs:
            disc.draw(screen)

