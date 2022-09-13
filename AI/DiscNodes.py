from SingletonState.ReferenceFrame import PointRef, Ref
from SingletonState.FieldTransform import FieldTransform
import Graphics, pygame, colors, math
import time


"""
A class that stores the complete list of discs on the field as PointRefs
"""

class Disc:

    transform: FieldTransform = None # gets initialized in DiscNodes

    # For convenience, the location of the disc is in field tile units.
    def __init__(self, fieldTileX: float, fieldTileY: float, isStartNode: bool = False):
        self.position: PointRef = PointRef(Disc.transform, Ref.FIELD, (fieldTileX*24 - 0.5, fieldTileY*24 - 0.5))

        # The index of this node in relation to DiscNodes.discs. Initialied in sortOtherDiscs()
        self.id = -1

        self.isStartNode = isStartNode


    # Get the index of self in relation to disc list
    # Sort self.otherDiscs from closest to furthest disc
    def preprocess(self, discs: list['Disc']):
        self.id = discs.index(self)
        self.neighbors: list['Disc'] = sorted(discs, key = lambda other: self.distanceTo(other))
        del self.neighbors[0] # delete the first element, which is just identity because sorting by distance

    # return the distance to the other disc in inches
    def distanceTo(self, other: 'Disc') -> float:
        return (other.position - self.position).magnitude(Ref.FIELD)


    # Recursive algortihm to draw path
    def drawPath(self, screen: pygame.Surface):

        # terminal node
        if self.child is None:
            return

        # Draw line to child
        pos1 = self.position.screenRef
        pos2 = self.child.position.screenRef
        Graphics.drawLine(screen, self.color, *pos1, *pos2, 2)

        self.child.drawPath(screen)

    def draw(self, screen: pygame.Surface):
        pos = self.position.screenRef
        Graphics.drawText(screen, Graphics.FONT30, str(self.id), (0,0,0), *pos)

class DiscNodes:

    def search(self, depth: int, child: list[int], parent: int = 0, distance: float = 0, string = "0 -> "):

        if depth == 0:
            return *self.rollout(child.copy(), parent, distance), string

        shortest = math.inf
        bestChild = None
        bestString = ""
        for i in range(0, 31):

            if i == parent or child[i] != -1:
                continue

            child[parent] = i
            #print(child)
            nd = distance + self.discs[parent].distanceTo(self.discs[i])
            ns = string + str(i) + " -> "
            newDistance, newChild, newString = self.search(depth - 1, child, i, nd, ns)
            child[parent] = -1

            if newDistance < shortest:
                shortest = newDistance
                bestChild = newChild
                bestString = newString

        return shortest, bestChild, bestString



    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)


        self.bestDistance = math.inf

        depth = 4
        start = time.time()
        shortest,self.bestChild, bestString = self.search(depth, [-1] * len(self.discs), 0)
        print("DEPTH {} ({} seconds)".format(depth, round(time.time()-start, 2)))
        print(bestString + ":", shortest, "inches")

        s = "["
        index = 0
        while index != -1:
            s += "{}, ".format(index)
            index = self.bestChild[index]
        s += "]"
        print(s)

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self, transform: FieldTransform) -> list[Disc]:

        Disc.transform = transform
        self.discs: list[Disc] = [
            Disc(3.5, 5, True), # START NODE
            Disc(1,1),
            Disc(2,2),
            Disc(3,2),
            Disc(0.5,0.5),
            Disc(1.5,1.5),
            Disc(2.5,1.5),
            Disc(2.5,2.5),
            Disc(1.5,2.5),
            Disc(3.5,2.5),
            Disc(3.85,1.13),
            Disc(3.85,1.495),
            Disc(3.85,1.87),
            Disc(3.5,3.5),
            Disc(3.5,4.5),
            Disc(2.5,3.5),
            Disc(3,4),
            Disc(4,4),
            Disc(4.5,4.5),
            Disc(5.5,5.5),
            Disc(4.51,3.5),
            Disc(5,5),
            Disc(4.12,2.165),
            Disc(4.5,2.165),
            Disc(4.87,2.165),
            Disc(1.12,3.85),
            Disc(1.5,3.85),
            Disc(1.88,3.85),
            Disc(2.165,4.133),
            Disc(2.165,4.5),
            Disc(2.165,4.88)
        ]

        # Pre-process by sorting each disc's distance to each other disc. O(n^2*log(n))
        for disc in self.discs:
            disc.preprocess(self.discs)

    # Set the visited attribute of all Discs to false
    def resetVisited(self):
        for disc in self.discs:
            disc.child = None
            disc.parent = None

    # Rollout policy is simply to select the closest unvisited disc 
    # Return the evaluation of this position
    def rollout(self, child: list[int], startID, startDistance) -> float:

        currentID = startID # current disc element

        totalDistance = startDistance

        while True:
            
            # Look for nearest unvisited neighbor
            nextID = -1
            for neighbor in self.discs[currentID].neighbors:
                if child[neighbor.id] == -1:
                    nextID = neighbor.id
                    break # We found nearest neighbor, don't keep searching
            # Exhausted search, unvisited neighbor not founded. Terminate loop
            if nextID == -1:
                break

            # we have found closest unvisited neighbor
            child[currentID] = nextID

            # update total distance
            totalDistance += self.discs[currentID].distanceTo(self.discs[nextID])

            currentID = nextID
            #print(round(totalDistance, 1), child)

        return totalDistance, child



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