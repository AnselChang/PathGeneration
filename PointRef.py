import re
import Utility
from FieldTransform import FieldTransform
from enum import Enum

"""
A class that stores the location of a single point, which can be interpreted from both field and screen reference frames.
The field reference frame is 144x144 inches while the screen has dimensions (SCREEN_SIZE + PANEL_WIDTH, SCREEN_SIZE) in pixels

To use this class, create a PointRef, and pass the fieldTransform object which has field info, 
as well as the point location and reference frame:
    p = PointRef(fieldTransform, Enum.SCREEN, (40, 50))

Now, through the automatic getter and setter methods, you can use the screen and frame reference frames interchangeably:
    p.screenRef = (2,3)
    print(p.fieldRef)
    p.fieldRef = (1,-1)
    print(p.screenRef)
"""

class Ref(Enum):
    SCREEN = 1 # screen reference mode
    FIELD = 2 # field reference mode

class PointRef:

    def __init__(self, fieldTransform: FieldTransform, referenceMode: Ref = None, point: tuple = (0,0)):
        self.transform = fieldTransform
        if referenceMode == Ref.SCREEN:
            self._setScreenRef(point)
        else:
            self._setFieldRef(point)

    def _setScreenRef(self, point: tuple) -> None:
        self._xs, self._ys = point

        # undo the panning and zooming
        panX, panY = self.transform.pan
        normalizedScreenX = (self._xs - panX) / self.transform.zoom
        normalizedScreenY = (self._ys - panY) / self.transform.zoom

        # convert to field reference frame
        self._xf = (normalizedScreenX - Utility.PIXELS_TO_FIELD_CORNER) / Utility.FIELD_SIZE_IN_PIXELS * Utility.FIELD_SIZE_IN_INCHES
        self._yf = (normalizedScreenY - Utility.PIXELS_TO_FIELD_CORNER) / Utility.FIELD_SIZE_IN_PIXELS * Utility.FIELD_SIZE_IN_INCHES

    def _getScreenRef(self) -> tuple:
        return self._xs, self._ys

    # getter and setter for point in screen reference frame
    screenRef = property(_getScreenRef, _setScreenRef)
    
    def _setFieldRef(self, point: tuple) -> None:
        self._xf, self._yf = point

        # convert to normalized (pre-zoom and pre-panning) coordinates
        normalizedScreenX = self._xf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER
        normalizedScreenY = self._yf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER

        # convert to screen reference frame
        print(self.transform.pan)
        panX, panY = self.transform.pan
        self._xs = normalizedScreenX * self.transform.zoom + panX
        self._ys = normalizedScreenY * self.transform.zoom + panY
        
    def _getFieldRef(self) -> tuple:
        return self._xf, self._yf

    # getter and setter for point in field reference frame
    fieldRef = property(_getFieldRef, _setFieldRef)

    # Return position with specified reference frame
    def get(self, referenceMode: Ref) -> tuple:
        return self.fieldRef if referenceMode == Ref.FIELD else self.screenRef

    # Return (this - otherPoint) in terms of the referenceMode reference frame
    # Does not modify either object
    def subtract(self, otherPoint: 'PointRef', referenceMode: Ref) -> tuple:
        if referenceMode == Ref.FIELD:
            return (self._xf - otherPoint._xf, self._yf - otherPoint._yf)
        else:
            return (self._xs - otherPoint._xs, self._ys - otherPoint._ys)

    # Add some offset to this point, modifying the object. Must specify reference frame
    def addInPlace(self, offset: tuple, referenceMode: Ref) -> None:
        if referenceMode == Ref.FIELD:
            self.fieldRef = (self.fieldRef[0] + tuple[0], self.fieldRef[1] + tuple[1])
        else:
            self.screenRef = (self.screenRef[0] + tuple[0], self.screenRef[1] + tuple[1])

    # Create a deep copy of the object and return the copy
    def copy(self) -> 'PointRef':
        return PointRef(self.transform, Ref.FIELD, self.fieldRef)


    def __str__(self):
        return "Point object:\nScreen: ({},{})\nField: ({},{})".format(self._xs, self._ys, self._xf, self._yf)

# Return a new PointRef object that translates the given PointRef by deltaPosition given by the referenceFrame (field/screen)
# Does not modify existing PointRef
def translateByVector(point: PointRef, deltaPosition: tuple, referenceFrame: Ref) -> PointRef:

    oldPosition = point.get(referenceFrame)
    newPosition: tuple = (oldPosition[0] + deltaPosition[0], oldPosition[1] + deltaPosition[1])
    return PointRef(point.transform, referenceFrame, newPosition)

# Testing code
if __name__ == "__main__":
    f = FieldTransform(2, (0,0))
    p = PointRef(f, Ref.FIELD, (10,10))
    p.screenRef = (0,0)
    print(p)
    p.fieldRef = (0,0)
    print(p)
