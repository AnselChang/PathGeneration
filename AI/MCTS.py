from AI.Disc import Disc
from AI.MCTSNode import MCTSNode
from typing import Tuple
import math

"""
The class handling the MCTS algorithm with finding the optimal path for traversing discs.
The MCTS tree is made up of MCTSNodes
A list of Disc objects is passed into the MCTS constructor for the purpose of preprocessed disc distances
"""

class MCTS:


    def __init__(self, discData: list[Disc]):

        self.discData = discData
        MCTSNode.discData = discData

        self.root = MCTSNode()
        
    # Run the full four-step MCTS algorithm some number of times
    # 1. Selection, 2. Expansion, 3. Simulation, 4. Backpropagation
    def run(self, iterations = 10000):

        for i in range(iterations):

            # Select the best node based on UTC value
            selectedNode: MCTSNode = self.root.selectNode()

            #  Expand that node and create an MCTSNode child for each nonvisited disc
            selectedNode.expandNode()

            # Simulate and backpropagate
            if len(selectedNode.children) == 0:
                # if reached a terminal leaf, backpropagate immediately without simulation
                selectedNode.backpropagate(selectedNode.startDistance)
            else:
                # Otherwise, perform a rollout simulation
                simulationNode = selectedNode.children[0]
                distance = simulationNode.rollout()

                # Backpropagate the results of that simulation
                selectedNode.backpropagate(distance)     


    # From the current MCTS tree, return a list of Disc objects (not MCTSNodes) representing the order of the
    # discs from start to end. Also, return the total distance of that path
    def getBestPath(self) -> Tuple[list[Disc], float]:


        # Get the best leaf node in the mcts tree so far. It is not necessarily a terminal node
        bestLeafNode: MCTSNode = self.root.getBestNode()

        # handle empty case
        if bestLeafNode is None:
            return [], math.inf

        # Generate the list of nodes from bestLeafNode to root
        discOrder: list[Disc] = []
        node: MCTSNode = bestLeafNode
        while node.parent is not None:
            currentDisc: Disc = self.discData[node.discID]
            discOrder.append(currentDisc)
            node = node.parent

        # Now, discOrder is ordered from leaf to root. We reverse to get root to leaf
        discOrder.reverse()

        return discOrder, bestLeafNode.shortestFullDistance