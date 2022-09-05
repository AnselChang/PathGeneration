import pygame, sys
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
from SingletonState.SoftwareState import SoftwareState
from SingletonState.UserInput import UserInput
from VisibleElements.FieldSurface import FieldSurface
from MouseInteraction import *
from VisibleElements.FullPath import FullPath


import Utility

def main():

    screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation 2.0 by Ansel")

    fieldTransform: FieldTransform = FieldTransform()
    fieldSurface: FieldSurface = FieldSurface(fieldTransform)
    userInput: UserInput = UserInput(fieldTransform, pygame.mouse, pygame.key)

    state: SoftwareState = SoftwareState()
    path: FullPath = FullPath(fieldTransform)

    # Main software loop
    while True:
        userInput.getUserInput()
        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        if not fieldSurface.isCurrentlyDragging:
            handleMousewheel(fieldSurface, fieldTransform, userInput)
        
        state.objectHovering = handleHoverables(state, userInput, path, fieldSurface)
        shadowPointRef = path.getShadowPosition(userInput.mousePosition)
        handleDragging(userInput, state, fieldSurface)

        if userInput.leftClicked and userInput.isMouseOnField:
            handleLeftClick(state, shadowPointRef, path)

        drawEverything(screen, state, fieldSurface, path, userInput, shadowPointRef)
        
        #print(state)


def drawEverything(screen: pygame.Surface, state: SoftwareState, fieldSurface: FieldSurface, path: FullPath, userInput: UserInput, shadowPointRef: PointRef) -> None:
    
    # Draw the vex field
    fieldSurface.draw(screen)

    # Draw the entire path with segments and PathPoints
    path.draw(screen)

    # Draw PathPoint shadow at mouse
    if userInput.isMouseOnField:
        Utility.drawCircle(screen, *shadowPointRef.screenRef, Utility.GREEN, 10, 140)
            

    # Draw panel background
    border = 5
    pygame.draw.rect(screen, Utility.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, Utility.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])

    pygame.display.update()

main()