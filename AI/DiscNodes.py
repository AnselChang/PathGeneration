from SingletonState.FieldTransform import FieldTransform
from AI.Disc import Disc, getAllDiscs
from AI.MCTSNode import MCTSNode
import Graphics, pygame, math
import time


class DiscNodes:


    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)

        self.treeMCTS = MCTSNode()
        self.MCTS()

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self, transform: FieldTransform) -> list[Disc]:

        Disc.transform = transform
        self.discs: list[Disc] = getAllDiscs()

        # Pre-process by sorting each disc's distance to each other disc. O(n^2*log(n))
        for disc in self.discs:
            disc.preprocess(self.discs)


    def MCTS(self):

        for i in range(1000):
            selectedNode: MCTSNode = self.treeMCTS.selectNode()
            selectedNode.expandNode(self.discs)
            simulationNode = selectedNode.childArray[0]
            distance = self.rollout(simulationNode.childArray.copy(), simulationNode.discID, simulationNode.startDistance)
            selectedNode.backpropagate(distance)

        best: MCTSNode = self.treeMCTS.getBestChild()


    # Rollout policy is simply to select the closest unvisited disc 
    # Return the evaluation of this position
    def rollout(self, childArray: list[int], startID, startDistance) -> float:

        currentID = startID # current disc element

        totalDistance = startDistance

        while True:
            
            # Look for nearest unvisited neighbor
            nextID = -1
            for neighbor in self.discs[currentID].neighbors:
                if childArray[neighbor.id] == -1:
                    nextID = neighbor.id
                    break # We found nearest neighbor, don't keep searching
            # Exhausted search, unvisited neighbor not founded. Terminate loop
            if nextID == -1:
                break

            # we have found closest unvisited neighbor
            childArray[currentID] = nextID

            # update total distance
            totalDistance += self.discs[currentID].distanceTo(self.discs[nextID])

            currentID = nextID
            #print(round(totalDistance, 1), child)

        return totalDistance



    # Draw each disc
    def draw(self, screen: pygame.Surface):

        color = Graphics.ColorCycle(0.03)

        # Draw disc path from self.child
        index = 0
        pos1 = self.discs[index].position.screenRef
        while True:
            index = self.bestChild[index]
            if index == -1:
                break
            pos2 = self.discs[index].position.screenRef
            Graphics.drawLine(screen, color.next(), *pos1, *pos2, 3)
            pos1 = pos2

        # Draw discs
        for disc in self.discs:
            disc.draw(screen)