from AbstractClasses.Hoverable import Hoverable
from SingletonState.SoftwareState import SoftwareState, Mode
from SingletonState.UserInput import UserInput
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
from VisibleElements.FieldSurface import FieldSurface
from VisibleElements.FullPath import FullPath
from VisibleElements.PathSegment import PathSegment
from VisibleElements.PathPoint import PathPoint
from VisibleElements.Point import Point
from Buttons.ButtonCollection import Buttons
from AbstractClasses.Draggable import Draggable
from AbstractClasses.Clickable import Clickable

import pygame

# Handle left clicks for dealing with the field
def handleLeftClick(state: SoftwareState, shadowPointRef: PointRef, fieldSurface: FieldSurface, path: FullPath):

    # can only add new PathPoints when in edit mode
    if state.mode == Mode.EDIT:

        # If nothing is hovered, create a new PathPoint at that location
        if state.objectHovering is fieldSurface:
            path.createPathPoint(shadowPointRef)
            state.recomputeInterpolation = True
        elif isinstance(state.objectHovering, PathSegment):
            index = path.segments.index(state.objectHovering) + 1
            path.createPathPoint(shadowPointRef, index)
            state.recomputeInterpolation = True

# Handle right clicks for dealing with the field
def handleRightClick(state: SoftwareState):
    print("Right click")
    # Right clicking PathPoint toggles its shape
    if isinstance(state.objectHovering, PathPoint):
        state.objectHovering.toggleShape()
        state.recomputeInterpolation = True
        
# Handle zooming through mousewheel. Zoom "origin" should be at the mouse location
def handleMousewheel(fieldSurface: FieldSurface, fieldTransform: FieldTransform, userInput: UserInput) -> None:
    
    if not fieldSurface.isCurrentlyDragging and userInput.mousewheelDelta != 0:

        oldMouseX, oldMouseY = userInput.mousePosition.screenRef

        zoomDelta = userInput.mousewheelDelta * 0.1
        fieldTransform.zoom += zoomDelta

        # Pan to adjust for the translate that would result from the zoom
        panX, panY = fieldTransform.pan
        newMouseX, newMouseY = userInput.mousePosition.screenRef
        fieldTransform.pan = (panX + oldMouseX - newMouseX, panY + oldMouseY - newMouseY)


        fieldSurface.updateScaledSurface()


# If X is pressed and hovering over PathPoint/PathSegment, delete it
def handleDeleting(userInput: UserInput, state: SoftwareState, path: FullPath):

    # Obviously, if X is not pressed, we're not deleting anything
    if not userInput.isKeyPressing(pygame.K_x):
        return

    if isinstance(state.objectHovering, PathPoint): # Delete pathPoint
        path.deletePathPoint(state.objectHovering)
        state.recomputeInterpolation = True

    elif isinstance(state.objectHovering, PathSegment): # Delete segment
        path.deletePathPoint(state.objectHovering.pointA)
        path.deletePathPoint(state.objectHovering.pointB)
        state.recomputeInterpolation = True



# A generator to iterate through all the hoverable objects to determine which object is being hovered by the mouse in order
def getHoverables(state: SoftwareState, userInput: UserInput, path: FullPath, buttons: Buttons, fieldSurface: FieldSurface):

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
        for button in buttons.buttons:
            yield button

    # weird python hack to make it return an empty iterator if nothing hoverable
    return
    yield


# Find the object that is hoverable, update that object's hoverable state, and return the object
def handleHoverables(state: SoftwareState, userInput: UserInput, path: FullPath, buttons: Buttons, fieldSurface: FieldSurface):

    if state.objectHovering is not None:
        state.objectHovering.resetHoverableObject()
        state.objectHovering = None

    for hoverableObject in getHoverables(state, userInput, path, buttons, fieldSurface):
        obj: Hoverable = hoverableObject # just for type hinting
        if obj.checkIfHovering(userInput):
            state.objectHovering = obj
            obj.setHoveringObject()
            break

# Called when the mouse was just pressed and we want to see if a new object is cliked or about to be dragged
# If the object is draggable, drag it
# Elif object is clickable, click it
def handleStartingPressingObject(userInput: UserInput, state: SoftwareState, fieldSurface: FieldSurface) -> None:

    # if the mouse is down on some object, try to drag that object
    if isinstance(state.objectHovering, Draggable):
        state.objectDragged = state.objectHovering
        state.objectDragged.startDragging(userInput.mousePosition)
    elif isinstance(state.objectHovering, Clickable):
        objectClicked: Clickable = state.objectHovering # "cast" type hint to Clickable
        objectClicked.click()


# Determine what object is being dragged based on the mouse's rising and falling edges, and actually drag the object in question
# If the mouse is dragging but not on any particular object, it will pan the field
def handleDragging(userInput: UserInput, state: SoftwareState, fieldSurface: FieldSurface) -> None:

    if userInput.leftPressed and userInput.mousewheelDelta == 0: # left mouse button just pressed

        # When the mouse has just clicked on the object, nothing should have been dragging before
        if state.objectDragged is not None:
            print("Error", userInput.leftPressed)
            raise Exception("objectDragged should always be None if the mouse was up before this frame.")
        else:
            handleStartingPressingObject(userInput, state, fieldSurface)   
    
    elif userInput.mouseReleased: # released, so nothing should be dragged
        if state.objectDragged is not None: # there was an object being dragged, so release that
            state.objectDragged.stopDragging()
            state.objectDragged = None

    # Now that we know what's being dragged, actually drag the object
    if state.objectDragged is not None:
        changed = state.objectDragged.beDraggedByMouse(userInput)
        if changed and (isinstance(state.objectDragged, Point)):
            state.recomputeInterpolation = True