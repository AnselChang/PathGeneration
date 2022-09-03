import pygame, sys
import FieldTransform, SoftwareState, FullPath, PointRef, UserInput, Utility

def main():

    screen = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation by Ansel")

    fieldTranform = FieldTransform.FieldTransform()
    userInput = UserInput.UserInput(fieldTranform, pygame.mouse, pygame.key)

    state = SoftwareState.SoftwareState()
    path = FullPath.FullPath()

    while True:

        userInput.getUserInput()

        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        state.objectHovering = getMouseHoveringObject(path, userInput)

        # Drag the object being dragged
        if state.objectDragged is not None:
            state.objectDragged.beDraggedByMouse(userInput.mousePosition)


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
            pass



main()