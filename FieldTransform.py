import Utility

# A struct for storing the field transformation relative to the screen, i.e. the current field pan and zoom.
# This class also bounds the pan and zoom so that the field never leaves the screen.
class FieldTransform:

    def __init__(self, fieldZoom: float = 1, xyFieldPanInPixels: tuple = (0,0)):
        self._zoom = fieldZoom
        self._panX, self._panY = xyFieldPanInPixels

    # Restrict the panning range for the field as to keep the field in sight of the screen
    def _boundFieldPan(self):
        maxPan = (1-self._zoom)*Utility.SCREEN_SIZE
        self._panX = Utility.clamp(self._panX, 0, maxPan)
        self._panY = Utility.clamp(self._panY, 0, maxPan)

    # A setter function for self.zoom, which bounds zoom and pan after zoom is updated to keep the field in sight of hte screen
    def getZoom(self):
        return self._zoom

    def setZoom(self, fieldZoom: float):
        self._zoom = Utility.clamp(fieldZoom, 1, 3) # limits to how much you can zoom in or out
        self._boundFieldPan()

    # self.zoom property that is gettable and settable
    zoom = property(getZoom, setZoom)

    def getPan(self):
        return self._panX, self._panY

    # After updating the field pan, make sure it is in bounds
    def setPan(self, xyFieldPanInPixels: tuple):
        self._panX, self._panY = xyFieldPanInPixels
        self._boundFieldPan()

    # self.pan property that is gettable and settable
    pan = property(getPan, setPan)