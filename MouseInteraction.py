from MouseInterfaces.Hoverable import Hoverable
from SingletonState.SoftwareState import SoftwareState, Mode
from SingletonState.UserInput import UserInput
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef, Ref
from VisibleElements.FieldSurface import FieldSurface
from VisibleElements.FullPath import FullPath
from VisibleElements.PathSegment import PathSegment
from VisibleElements.PathPoint import PathPoint
from VisibleElements.Point import Point
from Panel.Panel import Panel
from MouseInterfaces.Draggable import Draggable
from MouseInterfaces.Clickable import Clickable
import Utility
from typing import Iterator
from FileInteraction.PickleImporter import importFile

import pygame

# Return the location of the shadow PathPoint where the mouse is.
# This is exactly equal to the location of the mouse if the mouse is not hovering on a segment,
# but if the mouse is near a segment the shadow will "snap" to it
def getShadowPosition(mousePosition: PointRef, state: SoftwareState) -> PointRef:

    # If hovering over a segment, the shadow position is the point on the segment closest to the mouse
    if isinstance(state.objectHovering, PathSegment):
        positionA = state.objectHovering.pointA.position.fieldRef
        positionB = state.objectHovering.pointB.position.fieldRef
        positionOnSegment = Utility.pointOnLineClosestToPoint(*mousePosition.fieldRef, *positionA, *positionB)
        return PointRef(Ref.FIELD, positionOnSegment)
    # otherwise, the shadow position is simply the position of hte mouse
    else:
        return mousePosition

# Handle left clicks for dealing with the field
def handleLeftClick(state: SoftwareState, shadowPointRef: PointRef, fieldSurface: FieldSurface, path: FullPath):

    # can only add new PathPoints when in edit mode
    if state.mode == Mode.EDIT:

        # If nothing is hovered, create a new PathPoint at that location
        if state.objectHovering is fieldSurface:
            if len(path.sections) == 0:
                path.createSection(shadowPointRef)
            else:
                path.createPathPoint(shadowPointRef, path.currentSection)
        elif isinstance(state.objectHovering, PathSegment):
            sectionIndex, segmentIndex = path.getSegmentIndex(state.objectHovering)
            path.currentSection = sectionIndex
            path.createPathPoint(shadowPointRef, sectionIndex, segmentIndex + 1)

# Handle right clicks for dealing with the field
def handleRightClick(state: SoftwareState, path: FullPath, mousePosition: PointRef):

    print("Right click")

    if state.mode != Mode.EDIT:
        return

    if type(state.objectHovering) == FieldSurface:
        path.createSection(mousePosition)
    elif type(state.objectHovering) == PathPoint:
        hoveredPathPoint: PathPoint = state.objectHovering
        path.currentSection = hoveredPathPoint.section.sectionIndex # set the active section to be the clicked one
        print("right pathpoint", hoveredPathPoint.section)
        
# Handle zooming through mousewheel. Zoom "origin" should be at the mouse location
def handleMousewheel(fieldSurface: FieldSurface, fieldTransform: FieldTransform, userInput: UserInput) -> None:
    
    if not fieldSurface.isDragging and userInput.mousewheelDelta != 0:

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

    elif isinstance(state.objectHovering, PathSegment): # Delete segment
        path.deletePathPoint(state.objectHovering.pointA)
        path.deletePathPoint(state.objectHovering.pointB)


# Find the object that is hoverable, update that object's hoverable state, and return the object
def handleHoverables(state: SoftwareState, userInput: UserInput, hoverablesGenerator: Iterator[Hoverable]):

    if state.objectHovering is not None:
        state.objectHovering.resetHoverableObject()
        state.objectHovering = None

    for hoverableObject in hoverablesGenerator:
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
        state.objectDragged._startDragging(userInput.mousePosition)
    elif isinstance(state.objectHovering, Clickable):
        objectClicked: Clickable = state.objectHovering # "cast" type hint to Clickable
        objectClicked.click()


# Determine what object is being dragged based on the mouse's rising and falling edges, and actually drag the object in question
# If the mouse is dragging but not on any particular object, it will pan the field
def handleDragging(userInput: UserInput, state: SoftwareState, fieldSurface: FieldSurface, path: FullPath) -> None:

    if userInput.leftPressed and userInput.mousewheelDelta == 0: # left mouse button just pressed

        # When the mouse has just clicked on the object, nothing should have been dragging before        
        handleStartingPressingObject(userInput, state, fieldSurface)   
    
    elif userInput.mouseReleased: # released, so nothing should be dragged
        if state.objectDragged is not None: # there was an object being dragged, so release that
            state.objectDragged._stopDragging()
            state.objectDragged = None

    # Now that we know what's being dragged, actually drag the object
    if state.objectDragged is not None:
        changed = state.objectDragged.beDraggedByMouse(userInput)
        if changed and (isinstance(state.objectDragged, Point)):
            point: Point = state.objectDragged
            path.currentSection = point.section.sectionIndex
            path.sections[point.section.sectionIndex].calculateInterpolatedPoints()

        # if an object is being dragged it always takes precedence over any object that might be "hovering"
        if state.objectHovering is not state.objectDragged:
            if state.objectHovering is not None:
                state.objectHovering.resetHoverableObject()
            state.objectHovering = state.objectDragged
            state.objectHovering.setHoveringObject()

# If file is dragged into screen, import contents
def handleImportPath(filename, state: SoftwareState, path: FullPath):

    if filename is None or not filename.endswith(".path"):
        return
    
    importFile(filename, state, path)
    state.mode = Mode.EDIT
    print("Imported .path file.")