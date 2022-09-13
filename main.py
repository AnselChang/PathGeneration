import pygame, sys
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
from SingletonState.SoftwareState import SoftwareState, Mode
from SingletonState.UserInput import UserInput
from VisibleElements.FieldSurface import FieldSurface
from Simulation.ControllerManager import ControllerManager
from Simulation.Simulation import Simulation
from MouseInteraction import *
from VisibleElements.FullPath import FullPath
from Panel.Panel import Panel
from MouseInterfaces.TooltipOwner import TooltipOwner
from AI.DiscNodes import DiscNodes
from RobotSpecs import RobotSpecs
import Utility, colors
from typing import Iterator



# All the global singleton objects
screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
pygame.display.set_caption("Path Generation 2.0 by Ansel")

fieldTransform: FieldTransform = FieldTransform()
fieldSurface: FieldSurface = FieldSurface(fieldTransform)
userInput: UserInput = UserInput(fieldTransform, pygame.mouse, pygame.key)
controllers: ControllerManager = ControllerManager()

state: SoftwareState = SoftwareState()
path: FullPath = FullPath(fieldTransform)
discNodes: DiscNodes = DiscNodes(fieldTransform)
robotSpecs: RobotSpecs = RobotSpecs()
simulation: Simulation = Simulation(state, fieldTransform, controllers, path, robotSpecs)
panel: Panel = Panel(state, path, simulation)


def main():

    # Main software loop
    while True:

        state.recomputeInterpolation = False

        userInput.getUserInput()
        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        
        # Handle zooming with mousewheel
        handleMousewheel(fieldSurface, fieldTransform, userInput)

        # Handle panel keyboard input
        panel.handleKeyboardInput(userInput.keyJustPressed)
        
        # Find the hovered object out of all the possible hoverable objects
        handleHoverables(state, userInput, getHoverables())
        
        # Now that the hovered object is computed, handle what object is being dragged and then actually dragging the object
        handleDragging(userInput, state, fieldSurface)

        # If the X key is pressed, delete hovered PathPoint/segment
        handleDeleting(userInput, state, path)

        # get the shadow point based on the mouse position
        shadowPointRef = getShadowPosition(userInput.mousePosition, state)

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
        drawEverything(shadowPointRef)
        
        

# Draw the vex field, full path, and panel
def drawEverything(shadowPointRef: PointRef) -> None:
    
    # Draw the vex field
    fieldSurface.draw(screen)

    # Draw the entire path with segments and PathPoints
    path.draw(screen, state)

    # Draw PathPoint shadow at mouse
    if state.mode == Mode.EDIT and state.objectDragged is None and (state.objectHovering is fieldSurface or isinstance(state.objectHovering, PathSegment)):
        Utility.drawCircle(screen, *shadowPointRef.screenRef, colors.GREEN, 10, 140)
            
    # Draw panel background
    border = 5
    pygame.draw.rect(screen, colors.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, colors.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])

    # Draw panel buttons
    panel.draw(screen)

    # Draw a tooltip if there is one
    if state.objectHovering is not None and isinstance(state.objectHovering, TooltipOwner):
        state.objectHovering.drawTooltip(screen, userInput.mousePosition.screenRef)

    if state.mode == Mode.AI:
        discNodes.draw(screen)

    print(state.objectHovering is not None, state.objectDragged is not None)
    pygame.display.update()


# returns a generator object to iterate through all the hoverable objects,
# to determine which object is being hovered by the mouse in order
def getHoverables() -> Iterator[Hoverable]:

    # The points, segments, and field can only be hoverable if the mouse is on the field permieter and not on the panel
    if userInput.isMouseOnField:

        if state.mode == Mode.EDIT: # the path is only interactable when on edit mode
            # For each pathPoint, iterate through the control points then the pathPoint itself
            for pathPoint in path.pathPoints:
                yield pathPoint.controlA
                yield pathPoint.controlB
                yield pathPoint

            # After checking all the points, check the segments
            for segment in path.segments:
                yield segment

        # If nothing has been hovered, then finally check fieldSurface
        yield fieldSurface

    else: # hoverable panel objects

        # Iterate through each button on the panel
        for panelObject in panel.getHoverables():
            yield panelObject

    # weird python hack to make it return an empty iterator if nothing hoverable
    return
    yield


#import cProfile
#import re
#cProfile.run('main()')
main()