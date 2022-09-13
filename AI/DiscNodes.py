from SingletonState.ReferenceFrame import PointRef, Ref
from SingletonState.FieldTransform import FieldTransform
import Graphics, pygame, colors


"""
A class that stores the complete list of discs on the field as PointRefs
"""

class Disc:

    transform: FieldTransform = None # gets initialized in DiscNodes

    # For convenience, the location of the disc is in field tile units.
    def __init__(self, fieldTileX: float, fieldTileY: float, isStartNode: bool = False):
        self.position: PointRef = PointRef(Disc.transform, Ref.FIELD, (fieldTileX*24 - 0.5, fieldTileY*24 - 0.5))

        self.child: 'Disc' = None
        self.parent: 'Disc' = None

        self.isStartNode = isStartNode


    # Sort self.otherDiscs from closest to furthest disc
    def sortOtherDiscs(self, discs: 'Disc'):
        self.otherDiscs: list['Disc'] = sorted(discs, key = lambda other: self.distanceTo(other))
        del self.otherDiscs[0] # delete the first element, which is just identity because sorting by distance

    # return the distance to the other disc in inches
    def distanceTo(self, other: 'Disc') -> float:
        return (other.position - self.position).magnitude(Ref.FIELD)

    # Recursive greedy rollout algorithm
    # marks itself as visited then calls next closest node
    def rollout(self, parent: 'Disc', color: Graphics.ColorCycle):
        self.parent = parent
        self.color = color.next()

        # Find the closest unvisited disc then end
        for disc in self.otherDiscs:
            if disc.parent is None:
                self.child = disc
                disc.rollout(self, color)
                return

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
        color = colors.RED if self.isStartNode else colors.LIGHTBLUE
        Graphics.drawCircle(screen, *self.position.screenRef, color, 5 * Disc.transform.zoom)

class DiscNodes:

    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)
        self.rollout(self.discs[0])

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
            disc.sortOtherDiscs(self.discs)

    # Set the visited attribute of all Discs to false
    def resetVisited(self):
        for disc in self.discs:
            disc.child = None
            disc.parent = None

    # Rollout policy is simply to select the closest unvisited disc 
    def rollout(self, disc: Disc):
        self.resetVisited()
        disc.rollout(disc, Graphics.ColorCycle())


    # Draw each disc
    def draw(self, screen: pygame.Surface):
        for disc in self.discs:
            disc.draw(screen)

        self.discs[0].drawPath(screen)
