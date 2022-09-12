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

    def draw(self, screen: pygame.Surface):
        Graphics.drawCircle(screen, *self.position.screenRef, colors.LIGHTBLUE, 5)

class DiscNodes:

    def __init__(self, transform: FieldTransform):

        self.initDiscs(transform)

    # Initialize the disc list by creating disc objects at each location and specifying their coordinates
    def initDiscs(self, transform: FieldTransform) -> list[Disc]:

        Disc.transform = transform
        self.discs: list[Disc] = [

            Disc(1,1),
            Disc(2,2)

        ]

    # Draw each disc
    def draw(self, screen: pygame.Surface):
        for disc in self.discs:
            disc.draw(screen)