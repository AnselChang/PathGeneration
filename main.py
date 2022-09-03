import pygame, sys
from Draggable import Draggable
import FieldTransform, FieldSurface, SoftwareState, FullPath, UserInput, Utility

def main():

    screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation 2.0 by Ansel")

    fieldTransform: FieldTransform.FieldTransform = FieldTransform.FieldTransform()
    fieldSurface: FieldSurface.FieldSurface = FieldSurface.FieldSurface(fieldTransform)
    userInput: UserInput.UserInput = UserInput.UserInput(fieldTransform, pygame.mouse, pygame.key)

    state: SoftwareState.SoftwareState = SoftwareState.SoftwareState()
    path: FullPath.FullPath = FullPath.FullPath()

    # Main software loop
    while True:
        userInput.getUserInput()
        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        if not fieldSurface.isCurrentlyDragging:
            handleMousewheel(fieldSurface, fieldTransform, userInput)
        
        
        state.objectHovering = getMouseHoveringObject(path, userInput)
        handleDragging(userInput, state, fieldSurface)

        drawEverything(screen, fieldSurface)
        
        #print(state)

        if userInput.leftClicked:
            print("left")
        elif userInput.rightClicked:
            print("right")
        
# Handle zooming through mousewheel. Zoom "origin" should be at the mouse location
def handleMousewheel(fieldSurface:FieldSurface.FieldSurface, fieldTransform: FieldTransform.FieldTransform, userInput: UserInput.UserInput) -> None:
    
    if userInput.mousewheelDelta != 0:

        oldMouseX, oldMouseY = userInput.mousePosition.screenRef

        zoomDelta = userInput.mousewheelDelta * 0.1
        fieldTransform.zoom += zoomDelta

        # Pan to adjust for the translate that would result from the zoom
        panX, panY = fieldTransform.pan
        newMouseX, newMouseY = userInput.mousePosition.screenRef
        fieldTransform.pan = (panX + oldMouseX - newMouseX, panY + oldMouseY - newMouseY)


        fieldSurface.updateScaledSurface()

# Figure out what object, if any, the mouse is hovering over
def getMouseHoveringObject(path: FullPath.FullPath, userInput: UserInput.UserInput) -> object:
    
    # Figure out what the mouse is hovering over
        if userInput.isMouseOnField: # if mouse is on the field (instead of the panel)
            
            # Check if mouse is hovering over PathPoint
            hoveringPathPoint = path.getMouseHoveringPoint(userInput.mousePosition)
            if hoveringPathPoint is not None:
                return hoveringPathPoint

            # Check if mouse is hovering over segment
            pass
            
        else:
            # Mouse is on the panel (instead of the field)
            # Check for sliders
            pass


# Called when the mouse was just pressed and we want to see if a new object is about to be dragged
# This will try to drag either some object on the screen, or pan the entire field if no object is selected
def handleStartingDraggingObject(userInput: UserInput.UserInput, state: SoftwareState.SoftwareState, fieldSurface: FieldSurface.FieldSurface) -> None:

    # if the mouse is down on some object, try to drag that object
    if state.objectHovering is not None:

        # If the object is draggable and the mouse is down on that object, drag that object!
        if isinstance(state.objectHovering, Draggable):
            state.objectDragged = state.objectHovering
            state.objectDragged.startDragging()

    elif userInput.isMouseOnField: # The mouse pressed on the field but not on any particular object.
        # We want the mouse to control panning in this case.
        # To do this, we simply set the object dragged to be Draggable FieldTransform, which controls the field pan
        state.objectDragged = fieldSurface
        state.objectDragged.startDragging(userInput.mousePosition)


# Determine what object is being dragged based on the mouse's rising and falling edges, and actually drag the object in question
# If the mouse is dragging but not on any particular object, it will pan the field
def handleDragging(userInput: UserInput.UserInput, state: SoftwareState.SoftwareState, fieldSurface: FieldSurface.FieldSurface) -> None:

    if userInput.leftPressed and userInput.mousewheelDelta == 0: # left mouse button just pressed

        # When the mouse has just clicked on the object, nothing should have been dragging before
        if state.objectDragged is not None:
            print("Error", userInput.leftPressed)
            raise Exception("objectDragged should always be None if the mouse was up before this frame.")
        else:
            handleStartingDraggingObject(userInput, state, fieldSurface)   
    
    elif userInput.mouseReleased: # released, so nothing should be dragged
        if state.objectDragged is not None: # there was an object being dragged, so release that
            state.objectDragged.stopDragging()
            state.objectDragged = None

    # Now that we know what's being dragged, actually drag the object
    if state.objectDragged is not None:
        state.objectDragged.beDraggedByMouse(userInput.mousePosition)


def drawEverything(screen: pygame.Surface, fieldSurface: FieldSurface.FieldSurface) -> None:
    

    fieldSurface.draw(screen)

    # Draw panel background
    border = 5
    pygame.draw.rect(screen, Utility.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, Utility.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])
    
    pygame.display.update()

main()