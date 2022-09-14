import math
from AI.Disc import Disc



"""
A MCTS node
"""
class MCTSNode:

    totalSimulations = 0 # class variable to store the total number of simulations across all nodes in MCTS
    globalShortestDistance = math.inf # shortest distance across entire MCTS tree
    EXPLORATION_FACTOR = 100
    
    def __init__(self, childArray: list[int] = None, discID: int = 0, parent: 'MCTSNode' = None, startDistance = 0, depth = 0):

        # a list of ints corresponding to each element's child
        if childArray is None:
            self.childArray = [-1] * 31
        else:
            self.childArray = childArray.copy()

        # a list of MCTSNode children
        self.children: list[MCTSNode] = []

        if parent is not None:
            self.childArray[parent.discID] = discID

        self.parent = parent
        self.discID = discID
        self.startDistance = startDistance
        self.depth = depth

        self.numSimulations = 0
        self.shortestFullDistance = math.inf



    # the exploration-exploitation value for this node
    def getUCT(self):

        if self.numSimulations == 0:
            return 0.5

        exploitation =  MCTSNode.globalShortestDistance / self.globalShortestDistance
        exploration = math.sqrt(math.log(self.numSimulations) / MCTSNode.totalSimulations)
        return exploitation * MCTSNode.EXPLORATION_FACTOR * exploration


    # Only called on top-leveled node. Selects a leaf node based on highest UTC value
    def selectNode(self) -> 'MCTSNode':

        # If the node is a leaf node, return it
        if len(self.children) == 0:
            return self

        # Otherwise, we find the child with the best UTC value
        best = -math.inf
        bestNode = None
        for child in self.children:
            utc = child.getUCT()
            if utc > best:
                best = utc
                bestNode = child

        return bestNode.selectNode()


    # Expand all possible children of the node, but do not perform rollout
    # Expand in order of closest to furthest disc away
    def expandNode(self, discs: list[Disc]):

        LIMIT = 3

        i = 0

        for child in discs[self.discID].neighbors:

            # Append only if child disc is unvisited
            if self.childArray[child.id] == -1:
                i += 1
                childDistance = self.startDistance + discs[self.discID].distanceTo(child)
                self.children.append(MCTSNode(self.childArray, child.id, self, childDistance, self.depth + 1))

                if i == LIMIT:
                    return

    # Backpropagate distance for leaf node
    def backpropagate(self, fullDistance: float):
        self.numSimulations += 1
        #print("backpropagate", self.discID, self.numSimulations)
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

    def __str__(self) -> str:
        return "MCTSNode ({})".format(self.discID)

    def tree(self):
        s = "\t" * self.depth
        s += "{} {}".format(self.discID, self.numSimulations)
        print(s)

        for child in self.children:
            child.tree()