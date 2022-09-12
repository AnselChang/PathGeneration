from SingletonState.ReferenceFrame import PointRef, Ref
from SingletonState.FieldTransform import FieldTransform
import Graphics, pygame, colors

"""
A class that stores the complete list of discs on the field as PointRefs
"""

class Disc:

    transform: FieldTransform = None # gets initialized in DiscNodes

    # For convenience, the location of the disc is in field tile units.
    def __init__(self, fieldTileX: float, fieldTileY: float):
        self.position: PointRef = PointRef(Disc.transform, Ref.FIELD, (fieldTileX*24 - 0.5, fieldTileY*24 - 0.5))
        self.visited: bool = False

    # Sort self.otherDiscs from closest to furthest disc
    def sortOtherDiscs(self, discs: 'Disc'):
        self.otherDiscs = sorted(discs, key = lambda other: self.distanceTo(other))

    # return the distance to the other disc in inches
    def distanceTo(self, other: 'Disc') -> float:
        return (other.position - self.position).magnitude(Ref.FIELD)

    def draw(self, screen: pygame.Surface):
        Graphics.drawCircle(screen, *self.position.screenRef, colors.LIGHTBLUE, 5 * Disc.transform.zoom)

class DiscNodes:

    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self, transform: FieldTransform) -> list[Disc]:

        Disc.transform = transform
        self.discs: list[Disc] = [

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

    # Rollout policy is simply to select the closest unvisited disc 

    # Draw each disc
    def draw(self, screen: pygame.Surface):
        for disc in self.discs:
            disc.draw(screen)