import pygame, sys
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
import SingletonState.ReferenceFrame as ReferenceFrame
from SingletonState.SoftwareState import SoftwareState, Mode
from SingletonState.UserInput import UserInput
from VisibleElements.FieldSurface import FieldSurface
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from Simulation.Simulation import Simulation
from Simulation.DriverControl.DriverSimulation import DriverSimulation
import Simulation.ControllerRelated.ControllerSliderBuilder as ControllerSliderBuilder
from MouseInteraction import *
from VisibleElements.FullPath import FullPath
from Panel.Panel import Panel
from MouseInterfaces.TooltipOwner import TooltipOwner
from AI.DiscManager import DiscManager
from RobotSpecs import RobotSpecs
import Utility, colors
from typing import Iterator
import Graphics
import multiprocessing as mp 

if __name__ == '__main__':

    # All the global singleton objects
    screen: pygame.Surface = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation 2.0 by Ansel")

    fieldTransform: FieldTransform = FieldTransform()
    ReferenceFrame.initFieldTransform(fieldTransform)

    fieldSurface: FieldSurface = FieldSurface(fieldTransform)
    userInput: UserInput = UserInput(pygame.mouse, pygame.key)
    

    state: SoftwareState = SoftwareState()
    ControllerSliderBuilder.initState(state)

    controllers: ControllerManager = ControllerManager()
    path: FullPath = FullPath()
    discManager: DiscManager = DiscManager()
    robotSpecs: RobotSpecs = RobotSpecs()
    simulation: Simulation = Simulation(state, controllers, path, robotSpecs)
    driver: DriverSimulation = DriverSimulation(robotSpecs)
    panel: Panel = Panel(state, path, simulation, driver, discManager)



def main():

    # Main software loop
    while True:
        
        userInput.getUserInput()
        if userInput.isQuit:
            pygame.quit()
            sys.exit()

        # Handle import path from dropped file
        handleImportPath(userInput.loadedFile, state, path)
        
        # Handle zooming with mousewheel
        handleMousewheel(fieldSurface, fieldTransform, userInput)

        # Handle panel keyboard input
        panel.handleKeyboardInput(userInput.keyJustPressed)
        
        # Find the hovered object out of all the possible hoverable objects
        handleHoverables(state, userInput, getHoverables())
        
        # Now that the hovered object is computed, handle what object is being dragged and then actually dragging the object
        handleDragging(userInput, state, fieldSurface, path)

        # If the X key is pressed, delete hovered PathPoint/segment
        handleDeleting(userInput, state, path)

        # get the shadow point based on the mouse position
        shadowPointRef = getShadowPosition(userInput.mousePosition, state)

        # Handle all field left click functionality
        if userInput.isMouseOnField:
            if userInput.leftClicked:
                handleLeftClick(state, shadowPointRef, fieldSurface, path)
            elif userInput.rightClicked:
                handleRightClick(state, path, userInput.mousePosition)

        if state.mode == Mode.SIMULATE:
            simulation.update()
        elif state.mode == Mode.ODOM:
            driver.update()
        elif state.mode == Mode.AI:
            discManager.update()

        # Draw everything on the screen
        drawEverything(shadowPointRef)
        
        

# Draw the vex field, full path, and panel
def drawEverything(shadowPointRef: PointRef) -> None:
    
    # Draw the vex field
    fieldSurface.draw(screen)

    if state.mode == Mode.EDIT or state.mode == Mode.SIMULATE or state.mode == Mode.ROBOT:
        # Draw the entire path with segments and PathPoints
        path.draw(screen, state)

    # Draw PathPoint shadow at mouse
    if state.mode == Mode.EDIT and state.objectDragged is None and (state.objectHovering is fieldSurface or isinstance(state.objectHovering, PathSegment)):
        Graphics.drawCircle(screen, *shadowPointRef.screenRef, colors.GREEN, 10, 140)

            
    # Draw panel background
    border = 5
    pygame.draw.rect(screen, colors.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, colors.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])

    if state.mode == Mode.AI:
        discManager.draw(screen)
    
    # Draw panel buttons
    panel.draw(screen)

    # Draw a tooltip if there is one
    if state.objectHovering is not None and isinstance(state.objectHovering, TooltipOwner):
        state.objectHovering.drawTooltip(screen, userInput.mousePosition.screenRef)
        
    pygame.display.update()


# returns a generator object to iterate through all the hoverable objects,
# to determine which object is being hovered by the mouse in order
def getHoverables() -> Iterator[Hoverable]:

    # The points, segments, and field can only be hoverable if the mouse is on the field permieter and not on the panel
    if userInput.isMouseOnField:

        if state.mode == Mode.EDIT: # the path is only interactable when on edit mode
            # For each pathPoint, iterate through the control points then the pathPoint itself
            for section in path.sections:
                for pathPoint in section.pathPoints:
                    yield pathPoint.controlA
                    yield pathPoint.controlB
                    yield pathPoint

            # After checking all the points, check the segments
            for section in path.sections:
                for segment in section.segments:
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


if __name__ == '__main__':
    mp.freeze_support()
    main()