from AI.Disc import Disc
from AI.MCTSNode import MCTSNode
from typing import Tuple
import math
import multiprocessing as mp, atexit, time

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
        
        self.running = False # safe to use, no locking needed
        
        # All these need a lock to access
        self.sharedRunning = mp.Value('i', 0)
        self.sharedOrder = mp.Array('i', [-1]*32)
        self.sharedDistance = mp.Value('d', -1)
        self.sharedExplorationFactor = mp.Value('i', 100)
        self.lock = mp.Lock()
        atexit.register(self._kill)
        args = args=(self.lock, self.sharedRunning, self.sharedOrder, self.sharedDistance, discData, self.sharedExplorationFactor)
        self.p: mp.Process = mp.Process(target=self._startMultiprocesing, args = args)

        # Start process
        self.p.start()
        

    # Enable process to run MCTS
    def enable(self):
        self.running = True
        with self.lock:
            self.sharedRunning.value = 1

    # Disable process from running MCTS
    def disable(self):
        self.running = False
        with self.lock:
            self.sharedRunning.value = 0

    # Whether MCTS is running
    def isRunning(self) -> bool:
        return self.running

    # Kill process completely
    def _kill(self):
        with self.lock:
            self.sharedRunning.value = 2

    # Get discOrder and totalDistance. Safe
    def get(self) -> Tuple[list[Disc], float]:

        with self.lock:

            discOrder: list[Disc] = []
            i = 0
            while self.sharedOrder[i] != -1 and i < 32:
                discOrder.append(self.discData[self.sharedOrder[i]])
                i += 1
            totalDistance = self.sharedDistance.value
        return discOrder, totalDistance

    # Update the mcts explroation hyperparameter. Process safe
    def updateExplorationParameter(self, value):
        with self.lock:
            self.sharedExplorationFactor.value = value


    # Run the full four-step MCTS algorithm in a different process
    # Every N iterations, update the shared variables
    # 1. Selection, 2. Expansion, 3. Simulation, 4. Backpropagation
    def _startMultiprocesing(self, lock: mp.Lock, running: mp.Value, sharedOrder: mp.Array, sharedDistance: mp.Value, discData: list[Disc], sharedExplorationParameter: mp.Value):
        MCTSNode.discData = discData
        iterations = 5000

        print("start")

        isDone = False
        numberEpochs = 0
        while not isDone:

            with lock:
                MCTSNode.EXPLORATION_FACTOR = sharedExplorationParameter.value
                if running.value == 0:
                    time.sleep(0.1)
                    continue

            
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

            discOrder, totalDistance = self._getBestPath()
            
            # Update shared resources
            with lock:
                for i in range(len(discOrder)):
                    sharedOrder[i] = discOrder[i]
                for i in range(len(discOrder), 31 + 1):
                    sharedOrder[i] = -1
                sharedDistance.value = totalDistance
                isDone = running.value == 2

            numberEpochs += 1
            print("Finished iteration ", numberEpochs * iterations)


    # From the current MCTS tree, return a list of Disc objects (not MCTSNodes) representing the order of the
    # discs from start to end. Also, return the total distance of that path
    def _getBestPath(self) -> Tuple[list[int], float]:

        # Get the best leaf node in the mcts tree so far. It is not necessarily a terminal node
        bestLeafNode: MCTSNode = self.root.getBestNode()

        # handle empty case
        if bestLeafNode is None:
            return [], math.inf

        # Generate the list of nodes from bestLeafNode to root
        discOrder: list[int] = []
        node: MCTSNode = bestLeafNode
        while node is not None:
            discOrder.append(node.discID)
            node = node.parent

        # Now, discOrder is ordered from leaf to root. We reverse to get root to leaf
        discOrder.reverse()

        return discOrder, bestLeafNode.rollout()