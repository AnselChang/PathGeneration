from Hoverable import Hoverable
from SingletonState.SoftwareState import SoftwareState
from SingletonState.UserInput import UserInput
from SingletonState.FieldTransform import FieldTransform
from SingletonState.ReferenceFrame import PointRef
from VisibleElements.FieldSurface import FieldSurface
from VisibleElements.FullPath import FullPath
from VisibleElements.PathSegment import PathSegment
from VisibleElements.PathPoint import PathPoint
from Draggable import Draggable

# Handle left clicks for dealing with the field
def handleLeftClick(state: SoftwareState, shadowPointRef: PointRef, fieldSurface: FieldSurface, path: FullPath):

    # If nothing is hovered, create a new PathPoint at that location
    if state.objectHovering is fieldSurface or isinstance(state.objectHovering, PathSegment):
        path.createPathPoint(shadowPointRef)

# Handle right clicks for dealing with the field
def handleRightClick(state: SoftwareState):
    print("Right click")
    # Right clicking PathPoint toggles its shape
    if isinstance(state.objectHovering, PathPoint):
        state.objectHovering.toggleShape()

        
# Handle zooming through mousewheel. Zoom "origin" should be at the mouse location
def handleMousewheel(fieldSurface: FieldSurface, fieldTransform: FieldTransform, userInput: UserInput) -> None:
    
    if userInput.mousewheelDelta != 0:

        oldMouseX, oldMouseY = userInput.mousePosition.screenRef

        zoomDelta = userInput.mousewheelDelta * 0.1
        fieldTransform.zoom += zoomDelta

        # Pan to adjust for the translate that would result from the zoom
        panX, panY = fieldTransform.pan
        newMouseX, newMouseY = userInput.mousePosition.screenRef
        fieldTransform.pan = (panX + oldMouseX - newMouseX, panY + oldMouseY - newMouseY)


        fieldSurface.updateScaledSurface()

# A generator to iterate through all the hoverable objects to determine which object is being hovered by the mouse in order
def getHoverables(userInput: UserInput, path: FullPath, fieldSurface: FieldSurface):

    # The points, segments, and field can only be hoverable if the mouse is on the field permieter and not on the panel
    if userInput.isMouseOnField:

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
        pass # no panel yet!

    # weird python hack to make it return an empty iterator if nothing hoverable
    return
    yield


# Find the object that is hoverable, update that object's hoverable state, and return the object
def handleHoverables(state: SoftwareState, userInput: UserInput, path: FullPath, fieldSurface: FieldSurface):

    if state.objectHovering is not None:
        state.objectHovering.resetHoverableObject()

    for hoverableObject in getHoverables(userInput, path, fieldSurface):
        obj: Hoverable = hoverableObject # just for type hinting
        if obj.checkIfHovering(userInput):
            state.objectHovering = obj
            obj.setHoveringObject()
            break

# Called when the mouse was just pressed and we want to see if a new object is about to be dragged
# This will try to drag either some object on the screen, or pan the entire field if no object is selected
def handleStartingDraggingObject(userInput: UserInput, state: SoftwareState, fieldSurface: FieldSurface) -> None:

    # if the mouse is down on some object, try to drag that object
    if isinstance(state.objectHovering, Draggable):
        state.objectDragged = state.objectHovering
        state.objectDragged.startDragging(userInput.mousePosition)


# Determine what object is being dragged based on the mouse's rising and falling edges, and actually drag the object in question
# If the mouse is dragging but not on any particular object, it will pan the field
def handleDragging(userInput: UserInput, state: SoftwareState, fieldSurface: FieldSurface) -> None:

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
        state.objectDragged.beDraggedByMouse(userInput)