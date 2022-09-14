from SingletonState.FieldTransform import FieldTransform
from AI.Disc import Disc, getAllDiscs
from AI.MCTSNode import MCTSNode
import Graphics, pygame, math
import time


class DiscNodes:


    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)

        self.bestLeafNode = None

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

        for i in range(10000):
            selectedNode: MCTSNode = self.treeMCTS.selectNode()
            #print("MCTS EXPANDING NODE", selectedNode.discID, selectedNode.depth, selectedNode.getUCT(), selectedNode.numSimulations)

            selectedNode.expandNode(self.discs)

            if len(selectedNode.children) == 0:
                # if reached a terminal leaf, backpropagate immediately

                selectedNode.backpropagate(selectedNode.startDistance)
            else:
                # Otherwise, perform a rollout
                simulationNode = selectedNode.children[0]
                distance = self.rollout(simulationNode.childArray.copy(), simulationNode.discID, simulationNode.startDistance)
                selectedNode.backpropagate(distance)
            
        self.treeMCTS.tree()
        
        self.bestLeafNode: MCTSNode = self.treeMCTS.getBestNode()
        print(self.bestLeafNode)
        print(self.bestLeafNode.shortestFullDistance)
        print(MCTSNode.globalShortestDistance, "with exploration factor", MCTSNode.EXPLORATION_FACTOR)        


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

        # Draw AI stuff if MCTS has computed
        if self.bestLeafNode is not None:

            color = Graphics.ColorCycle(0.03)

            # Draw disc path from self.child
            node = self.bestLeafNode
            while node.parent is not None:
                pos1 = self.discs[node.discID].position.screenRef
                pos2 = self.discs[node.parent.discID].position.screenRef
                Graphics.drawLine(screen, color.next(), *pos1, *pos2, 3)
                node = node.parent

        # Draw discs
        for disc in self.discs:
            disc.draw(screen)

