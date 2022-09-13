import math
from AI.Disc import Disc



"""
A MCTS node
"""
class MCTSNode:

    totalSimulations = 0 # class variable to store the total number of simulations across all nodes in MCTS
    globalShortestDistance = math.inf # shortest distance across entire MCTS tree
    EXPLORATION_FACTOR = 1
    
    def __init__(self, childArray: list[int] = None, discID: int = 0, parent: 'MCTSNode' = None, startDistance = 0, depth = 0):

        if childArray is None:
            self.childArray = [-1] * 31
        else:
            self.childArray = childArray

        self.children: list[MCTSNode] = []

        if parent is not None:
            self.childArray[parent.discID] = discID

        self.parent = parent
        self.discID = discID
        self.startDistance = startDistance
        self.depth = 0

        self.numSimulations = 0
        self.shortestFullDistance = math.inf


    # the exploration-exploitation value for this node
    def getUCT(self):
        exploitation =  MCTSNode.globalShortestDistance / self.globalShortestDistance
        exploration = math.sqrt(math.log(self.numSimulations) / MCTSNode.totalSimulations)
        return exploitation * MCTSNode.EXPLORATION_FACTOR * exploration

    # Inner class to help with selection of the next leaf
    class LeafSelector:

        def __init__(self):
            self.bestLeaf: MCTSNode = None
            self.bestUTC = -math.inf

        def consider(self, node: 'MCTSNode'):
            utc = node.getUCT()
            if utc > self.bestUTC:
                self.bestUTC = utc
                self.bestLeaf = node

    # Only called on top-leveled node. Selects a leaf node based on highest UTC value
    def selectNode(self) -> 'MCTSNode':

        selector = self.LeafSelector()
        self._selectNode(selector)
        return selector.bestLeaf

    # private recursive function to traverse leaf nodes and select node
    def _selectNode(self, selector: LeafSelector) -> None:

        # prevent from going too deep
        if self.depth >= 30:
            return

        if len(self.children) == 0:
            selector.consider(self)
        else:
            for child in self.children:
                child._selectNode(selector)

    # Expand all possible children of the node, but do not perform rollout
    # Expand in order of closest to furthest disc away
    def expandNode(self, discs: list[Disc]):

        for child in discs[self.discID].neighbors:

            # Append only if child disc is unvisited
            if self.childArray[child.id] == -1:
                childDistance = self.startDistance + discs[self.discID].distanceTo(child)
                self.children.append(MCTSNode(self.childArray.copy(), child.id, self, childDistance, self.depth + 1))

    # Backpropagate distance for leaf node
    def backpropagate(self, fullDistance: float):
        self.numSimulations += 1
        if fullDistance < self.shortestFullDistance:
            self.shortestFullDistance = fullDistance
    
        # If at root node, update global simulation numbers
        if self.depth == 0:
            MCTSNode.totalSimulations += 1
            if fullDistance < MCTSNode.globalShortestDistance:
                MCTSNode.globalShortestDistance = fullDistance
        else:
            # Otherwise, backpropagate up!
            self.parent.backpropagate(fullDistance)

    # Get the best child in terms of shortest path of the current object
    def getBestChild(self) -> 'MCTSNode':
        for child in self.children:
            if child.shortestFullDistance == MCTSNode.globalShortestDistance:
                return child