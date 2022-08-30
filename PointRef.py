import Utility
import FieldTransform
from enum import Enum

"""
A class that stores the location of a single point, which can be interpreted from both field and screen reference frames.
The field reference frame is 144x144 inches while the screen has dimensions (SCREEN_SIZE + PANEL_WIDTH, SCREEN_SIZE) in pixels

To use this class, create a PointRef, and pass the fieldTransform object which has field info, 
as well as the point location and reference frame:
    p = PointRef(fieldTransform, Enum.SCREEN, (40, 50))

Now, through the decorator getter and setter methods, you can use the screen and frame reference frames interchangeably:
    p.screenRef = (2,3)
    print(p.fieldRef)
    p.fieldRef = (1,-1)
    print(p.screenRef)
"""

class Ref(Enum):
    SCREEN = 1 # screen reference mode
    FIELD = 2 # field reference mode

class PointRef:

    def __init__(self, fieldTransform: FieldTransform.FieldTransform, referenceMode: Ref, point: tuple = (0,0)):
        self.transform = FieldTransform
        if referenceMode == Ref.SCREEN:
            self._setScreenRef(point)
        else:
            self._setFieldRef(point)

    def _setScreenRef(self, point: tuple) -> None:
        self._xs, self._ys = tuple

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
        self._xf, self._yf = tuple

        # convert to normalized (pre-zoom and pre-panning) coordinates
        normalizedScreenX = self._xf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER
        normalizedScreenY = self._yf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER

        # convert to screen reference frame
        panX, panY = self.transform.pan
        self._xs = normalizedScreenX * self.transform.zoom + panX
        self._ys = normalizedScreenY * self.transform.zoom + panY
        
    def _getFieldRef(self) -> tuple:
        return self._xf, self._yf

    # getter and setter for point in field reference frame
    fieldRef = property(_getFieldRef, _setFieldRef)