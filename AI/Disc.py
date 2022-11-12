from SingletonState.ReferenceFrame import PointRef, Ref
import Graphics, pygame

"""
A class that stores the complete list of discs on the field as PointRefs
"""

class Disc:


    # For convenience, the location of the disc is in field tile units.
    def __init__(self, fieldTileX: float, fieldTileY: float, isStartNode: bool = False):
        self.position: PointRef = PointRef(Ref.FIELD, (fieldTileX*24 - 0.5, fieldTileY*24 - 0.5))

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


    def draw(self, screen: pygame.Surface):
        pos = self.position.screenRef
        Graphics.drawText(screen, Graphics.FONT30, str(self.id), (0,0,0), *pos)


# The position of every disc on the field
# 31 DISCS
def getAllDiscs(): 
    return [
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
