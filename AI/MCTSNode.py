import math
from AI.Disc import Disc



"""
A MCTS node
"""
class MCTSNode:

    totalSimulations = 0 # class variable to store the total number of simulations across all nodes in MCTS
    globalShortestDistance = math.inf # shortest distance across entire MCTS tree
    EXPLORATION_FACTOR = 100

    discData: list[Disc] = None # preprocessed information for each disc
    
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

    # the exploration-exploitation value for this node. Selection picks the node with the highest UCT value
    def getUCT(self):

        if self.numSimulations == 0:
            return math.inf

        exploitation =  1000 - self.shortestFullDistance
        exploration = math.sqrt(math.log(MCTSNode.totalSimulations) / self.numSimulations)
        return exploitation + MCTSNode.EXPLORATION_FACTOR * exploration


    # Selects a leaf node based on highest UTC value recursively, by expanding layer by layer until leaf node is reached
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


    # Expand all possible children of the node, but do not perform rollout on each child
    # Expand in order of closest to furthest disc away
    def expandNode(self):

        LIMIT = 3

        i = 0

        for child in MCTSNode.discData[self.discID].neighbors:

            # Append only if child disc is unvisited
            if self.childArray[child.id] == -1:
                i += 1
                childDistance = self.startDistance + MCTSNode.discData[self.discID].distanceTo(child)
                self.children.append(MCTSNode(self.childArray, child.id, self, childDistance, self.depth + 1))

                if i == LIMIT:
                    return

    # Rollout policy is simply to select the closest unvisited disc 
    # Return the evaluation of this position
    def rollout(self) -> float:

        # Make a copy of the child array during simulation to not affect the actual MCTS nodes
        childArray: list[int] = self.childArray.copy()

        currentID = self.discID # current disc element

        totalDistance = self.startDistance # we add the distance to the current disc to the totalDistance

        while True:
            
            # Look for nearest unvisited neighbor
            nextID = -1
            for neighbor in MCTSNode.discData[currentID].neighbors:
                if childArray[neighbor.id] == -1:
                    nextID = neighbor.id
                    break # We found nearest neighbor, don't keep searching
            # Exhausted search, unvisited neighbor not founded. Terminate loop
            if nextID == -1:
                break

            # we have found closest unvisited neighbor
            childArray[currentID] = nextID

            # update total distance
            totalDistance += MCTSNode.discData[currentID].distanceTo(MCTSNode.discData[nextID])

            currentID = nextID
            #print(round(totalDistance, 1), child)

        return totalDistance



    # Backpropagate distances and number of simulations from leaf node all the way to root
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


    # Get best leaf node so far
    def getBestNode(self) -> 'MCTSNode':

        if self.leaf():
            return self

        bestDistance = math.inf
        best = None
        for child in self.children:
            if child.shortestFullDistance <= bestDistance:
                bestDistance = child.shortestFullDistance
                best = child
        
        return best.getBestNode()

    def leaf(self):
        return len(self.children) == 0

    def __str__(self) -> str:
        return "MCTSNode ({})".format(self.discID)

    def tree(self):
        s = "\t" * self.depth
        s += "{} {} {}".format(self.discID, self.numSimulations,  self.shortestFullDistance)
        print(s)

        if self.depth == 3:
            return

        for child in self.children:
            child.tree()