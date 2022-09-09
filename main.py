import pygame, sys
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
from SingletonState.SoftwareState import SoftwareState, Mode
from SingletonState.UserInput import UserInput
from VisibleElements.FieldSurface import FieldSurface
from MouseInteraction import *
from VisibleElements.FullPath import FullPath
from Buttons.ButtonCollection import Buttons
import Utility

def main():

    screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation 2.0 by Ansel")

    fieldTransform: FieldTransform = FieldTransform()
    fieldSurface: FieldSurface = FieldSurface(fieldTransform)
    userInput: UserInput = UserInput(fieldTransform, pygame.mouse, pygame.key)

    state: SoftwareState = SoftwareState()
    path: FullPath = FullPath(fieldTransform)
    buttons: Buttons = Buttons(state)

    # Main software loop
    while True:

        state.recomputeInterpolation = False

        userInput.getUserInput()
        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        # Handle zooming with mousewheel
        handleMousewheel(fieldSurface, fieldTransform, userInput)
        
        # Find the hovered object out of all the possible hoverable objects
        handleHoverables(state, userInput, path, buttons, fieldSurface)
        
        # Now that the hovered object is computed, handle what object is being dragged and then actually dragging the object
        handleDragging(userInput, state, fieldSurface)

        # If the X key is pressed, delete hovered PathPoint/segment
        handleDeleting(userInput, state, path)

        # get the shadow point based on the mouse position
        shadowPointRef = path.getShadowPosition(userInput.mousePosition, state)

        # Handle all field left click functionality
        if userInput.isMouseOnField:
            if userInput.leftClicked:
                handleLeftClick(state, shadowPointRef, fieldSurface, path)
            elif userInput.rightClicked:
                handleRightClick(state)

        # Whenever the path is modified, the interpolated beizer points have to be recomputed again
        if state.recomputeInterpolation:
            path.calculateInterpolatedPoints()

        # Draw everything on the screen
        drawEverything(screen, state, fieldSurface, path, buttons, shadowPointRef, userInput)
        
        

# Draw the vex field, full path, and panel
def drawEverything(screen: pygame.Surface, state: SoftwareState, fieldSurface: FieldSurface, path: FullPath, buttons: Buttons, shadowPointRef: PointRef, userInput: UserInput) -> None:
    
    # Draw the vex field
    fieldSurface.draw(screen)

    # Draw the entire path with segments and PathPoints
    path.draw(screen, state)

    # Draw PathPoint shadow at mouse
    if state.mode == Mode.EDIT and (state.objectHovering is fieldSurface or isinstance(state.objectHovering, PathSegment)):
        Utility.drawCircle(screen, *shadowPointRef.screenRef, Utility.GREEN, 10, 140)
            
    # Draw panel background
    border = 5
    pygame.draw.rect(screen, Utility.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, Utility.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])

    # Draw panel buttons
    buttons.draw(screen)

    # Draw a tooltip if there is one
    if state.objectHovering is not None and hasattr(state.objectHovering, "tooltip"):
        state.objectHovering.tooltip.draw(screen, userInput.mousePosition.screenRef)

    pygame.display.update()


import cProfile
import re
cProfile.run('main()')
#main()