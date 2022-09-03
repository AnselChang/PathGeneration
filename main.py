import pygame, sys
from Draggable import Draggable
import FieldTransform, SoftwareState, FullPath, PointRef, UserInput, Utility

def main():

    screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation by Ansel")

    fieldTranform: FieldTransform.FieldTransform = FieldTransform.FieldTransform()
    userInput: UserInput.UserInput = UserInput.UserInput(fieldTranform, pygame.mouse, pygame.key)

    state: SoftwareState.SoftwareState = SoftwareState.SoftwareState()
    path: FullPath.FullPath = FullPath.FullPath()

    while True:

        userInput.getUserInput()

        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        state.objectHovering = getMouseHoveringObject(path, userInput)
        handleDragging(path, userInput, state)

        drawEverything(screen)
        


# Figure out what object, if any, the mouse is hovering over
def getMouseHoveringObject(path: FullPath.FullPath, userInput: UserInput.UserInput) -> object:
    
    # Figure out what the mouse is hovering over
        if userInput.mousePosition.screenRef[0] < Utility.SCREEN_SIZE: # if mouse is on the field
            
            # Check if mouse is hovering over PathPoint
            hoveringPathPoint = path.getMouseHoveringPoint
            if hoveringPathPoint is not None:
                return hoveringPathPoint

            # Check if mouse is hovering over segment
            pass
            
        else:
            # Mouse is on the right panel
            # Check for sliders
            pass

def handleDragging(path: FullPath.FullPath, userInput: UserInput.UserInput, state: SoftwareState.SoftwareState) -> None:

    if userInput.leftPressed: # left mouse button just pressed

            if state.objectHovering is not None: # mouse down on some object

                # If the object is draggable and the mouse is down on that object, drag that object!
                if isinstance(state.objectHovering, Draggable):
                    state.objectDragged = state.objectHovering
                    state.objectDragged.startDragging()
    
    elif userInput.mouseReleased: # mouse released, so nothing should be dragged
        if state.objectDragged is not None: # there was an object being dragged, so release that
            state.objectDragged.stopDragging()
            state.objectDragged = None

    # Now that we know what's being dragged, actually drag the object
    if state.objectDragged is not None:
        state.objectDragged.beDraggedByMouse(userInput.mousePosition)


def drawEverything(screen: pygame.Surface) -> None:
    pass


main()