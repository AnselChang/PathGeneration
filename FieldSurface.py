import FieldTransform, PointRef, Draggable, Utility, pygame

"""A class that stores the scaled surface of the vex field, and contains a draw() method to draw it onto the screen.
It implements Draggable, meaning that the mouse can drag the field to pan the screen. This is coupled with FieldTransform,
in that panning the screen will change panning values in FieldTransform and therefore pan every other object on the field.
"""

class FieldSurface(Draggable.Draggable):

    def __init__(self, fieldTransform: FieldTransform.FieldTransform):
        self.transform = fieldTransform
        self.rawFieldSurface: pygame.Surface = pygame.image.load("Images/squarefield.png")
        self.updateScaledSurface()

        self.previousMouseX, self.previousMouseY = None, None # For calculating mouse dragging delta to determine panning amount

    # Whenever the zoom is changed, this function should be called to scale the raw surface into the scaled one
    def updateScaledSurface(self):
        self.scaledFieldSurface: pygame.Surface = pygame.transform.smoothscale(
            self.rawFieldSurface, [Utility.SCREEN_SIZE * self.transform.zoom, Utility.SCREEN_SIZE * self.transform.zoom])

    
    # Called when the field was just pressed at the start of the drag
    def startDragging(self, mousePosition: PointRef.PointRef):
        self.previousMouseX, self.previousMouseY = mousePosition.screenRef

    # Called every frame that the object is being dragged. Most likely used to update the position of the object based
    # on where the mouse is
    def beDraggedByMouse(self, mousePosition: PointRef.PointRef):

        print("dragging")

        deltaX = mousePosition.screenRef[0] - self.previousMouseX
        deltaY = mousePosition.screenRef[1] - self.previousMouseY

        panX, panY = self.transform.pan
        self.transform.pan = panX + deltaX, panY + deltaY

        self.previousMouseX, self.previousMouseY = mousePosition.screenRef # update previous mouse position to current frame

    # Called when the dragged object was just released
    def stopDragging(self):
        self.previousMouseX, self.previousMouseY = None, None

    # Draw the scaled field with the stored pan
    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaledFieldSurface, self.transform.pan)

    def __str__(self):
        return "FieldSurface with transform: {}".format(self.transform)