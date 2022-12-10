from SingletonState.FieldTransform import FieldTransform
import Utility, math
from enum import Enum

transform: FieldTransform = None
def initFieldTransform(fieldTransform: FieldTransform):
    global transform
    transform = fieldTransform

"""
A class that stores the location of a single point, which can be interpreted from both field and screen reference frames.
The field reference frame is 144x144 inches while the screen has dimensions (SCREEN_SIZE + PANEL_WIDTH, SCREEN_SIZE) in pixels

To use this class, create a PointRef, and pass the fieldTransform object which has field info, 
as well as the point location and reference frame:
    p = PointRef(fieldTransform, Ref.SCREEN, (40, 50))

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

    def __init__(self, referenceMode: Ref = None, point: tuple = (0,0)):
        self.transform = transform
        self._xf, self._yf = None, None
        if referenceMode == Ref.SCREEN:
            self.screenRef = point
        else:
            self.fieldRef = point

    # Given we only store the point in the field reference frame, convert to field reference frame before storing it
    def _setScreenRef(self, point: tuple) -> None:

        # undo the panning and zooming
        panX, panY = self.transform.pan
        normalizedScreenX = (point[0] - panX) / self.transform.zoom
        normalizedScreenY = (point[1] - panY) / self.transform.zoom

        # convert to field reference frame
        self._xf = (normalizedScreenX - Utility.PIXELS_TO_FIELD_CORNER) / Utility.FIELD_SIZE_IN_PIXELS * Utility.FIELD_SIZE_IN_INCHES
        self._yf = (normalizedScreenY - Utility.PIXELS_TO_FIELD_CORNER) / Utility.FIELD_SIZE_IN_PIXELS * Utility.FIELD_SIZE_IN_INCHES

    # Given we only store the point in the field reference frame, we need to convert it to return as screen reference frame
    def _getScreenRef(self) -> tuple:
        # convert to normalized (pre-zoom and pre-panning) coordinates
        normalizedScreenX = self._xf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER
        normalizedScreenY = self._yf / Utility.FIELD_SIZE_IN_INCHES * Utility.FIELD_SIZE_IN_PIXELS + Utility.PIXELS_TO_FIELD_CORNER

        # convert to screen reference frame
        panX, panY = self.transform.pan
        xs = normalizedScreenX * self.transform.zoom + panX
        ys = normalizedScreenY * self.transform.zoom + panY

        return xs, ys

    # getter and setter for point in screen reference frame
    screenRef = property(_getScreenRef, _setScreenRef)
    
    def _setFieldRef(self, point: tuple) -> None:
        self._xf, self._yf = point
        
    def _getFieldRef(self) -> tuple:
        return self._xf, self._yf

    # getter and setter for point in field reference frame
    fieldRef = property(_getFieldRef, _setFieldRef)

    # Return position with specified reference frame
    def get(self, referenceMode: Ref) -> tuple:
        return self.fieldRef if referenceMode == Ref.FIELD else self.screenRef

    # PointRef + VectorRef = PointRef
    def __add__(self, other: 'VectorRef') -> 'PointRef':
        return PointRef(Ref.FIELD, Utility.addTuples(self.fieldRef, other.fieldRef))

    # PointRef - VectorRef = PointRef
    # PointRef - PointRef = VectorRef
    def __sub__(self, other):
        if type(other) == PointRef:
            return VectorRef(Ref.FIELD, Utility.subtractTuples(self.fieldRef, other.fieldRef))
        else: # other is of type VectorRef
            return PointRef(Ref.FIELD, Utility.subtract(self.fieldRef, other.fieldRef))

    def __eq__(self, other):

        if not type(other) == PointRef:
            return False

        return self._xf == other._xf and self._yf == other._yf

    # Create a deep copy of the object and return the copy
    def copy(self) -> 'PointRef':
        return PointRef(Ref.FIELD, self.fieldRef)

    def __str__(self):
        return "Point object:\nScreen: ({},{})\nField: ({},{})".format(*self.screenRef, *self.fieldRef)


"""A class that stores a translation vector in both field and reference frames.
PointRef + VectorRef = PointRef
PointRef - VectorRef = PointRef
PointRef - PointRef = VectorRef
VectorRef + VectorRef = VectorRef
VectorRef - VectorRef = VectorRef
"""
class VectorRef:

    def __init__(self, referenceMode: Ref = None, vector: tuple = (0,0)):
        self.transform: FieldTransform = transform
        self._vxf, self._vyf = None, None
        if referenceMode == Ref.SCREEN:
            self.screenRef = vector
        else:
            self.fieldRef = vector

    def _setFieldRef(self, vector: tuple):
        self._vxf, self._vyf = vector

    def _getFieldRef(self) -> tuple:
        return self._vxf, self._vyf

    fieldRef = property(_getFieldRef, _setFieldRef)

    # Given we only store the point in the field reference frame, convert to field reference frame before storing it
    def _setScreenRef(self, vector: tuple):
        scalar = Utility.FIELD_SIZE_IN_INCHES / Utility.FIELD_SIZE_IN_PIXELS / self.transform.zoom
        self._vxf = vector[0] * scalar
        self._vyf = vector[0] * scalar

    # Given we only store the point in the field reference frame, we need to convert it to return as screen reference frame
    def _getScreenRef(self):
        scalar = self.transform.zoom * Utility.FIELD_SIZE_IN_PIXELS / Utility.FIELD_SIZE_IN_INCHES
        return self._vxf * scalar, self._vyf * scalar

    screenRef = property(_getScreenRef, _getFieldRef)

    # Return the magnitude of the vector based on the given reference frame
    def magnitude(self, referenceFrame: Ref) -> float:
        if referenceFrame == Ref.FIELD:
            return Utility.distance(0, 0, *self.fieldRef)
        else:
            return Utility.distance(0, 0, *self.screenRef)

    # Get the angle of the vector in radians
    def theta(self) -> float:
        return math.atan2(self._vyf, self._vxf)

    # Returns an new vector that is rotated counterclockwise the specified theta in radians
    # Does not modify the current object
    def rotate(self, theta: float) -> 'VectorRef':
        mag = self.magnitude(Ref.FIELD)
        angle = self.theta()
        angle += theta
        return VectorRef(Ref.FIELD, (mag * math.cos(angle), mag * math.sin(angle)))

    # Does not modify the current object but creates a new object with a magnitude of 1
    def normalize(self) -> 'VectorRef':
        mag = self.magnitude(Ref.FIELD)
        return VectorRef(Ref.FIELD, Utility.divideTuple(self.fieldRef, mag))

    # Vector addition. Does not modify but returns new VectorRef
    def __add__(self, other: 'VectorRef') -> 'VectorRef':
        return VectorRef(Ref.FIELD, Utility.addTuples(self.fieldRef, other.fieldRef))

    # Vector subtraction. Does not modify but returns new VectorRef
    def __sub__(self, other: 'VectorRef') -> 'VectorRef':
        return VectorRef(Ref.FIELD, Utility.subtractTuples(self.fieldRef, other.fieldRef))

    # Scales vector by some scalar. Does not modify but returns new VectorRef
    def __mul__(self, scalar: float) -> 'VectorRef':
        return VectorRef(Ref.FIELD, Utility.scaleTuple(self.fieldRef, scalar))


# Testing code
if __name__ == "__main__":
    f = FieldTransform(2, (0,0))
    p = PointRef(f, Ref.FIELD, (10,10))
    p.screenRef = (0,0)
    print(p)
    p.fieldRef = (0,0)
    print(p)
