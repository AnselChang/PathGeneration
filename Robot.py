import math, Utility

class Robot:

    def __init__(self, width, length):
        self.width = width
        self.length = length

    def startSimulation(self, points):
        self.points = points
        self.pointIndex = 0

    # return if animation is still going
    def simulationTick(self, screen, m):

        if self.pointIndex == len(self.points):
            return False
        
        p = self.points[self.pointIndex]
        cx, cy = m.inchToPixel(p.x, p.y)
        theta = p.theta
        width = self.width * m.zoom
        length = self.length * m.zoom

        dxw = math.cos(theta + math.pi/2) * width
        dyw = math.sin(theta + math.pi/2) * width
        dxl = math.cos(theta) * length
        dyl = math.sin(theta) * length

        # Generate four points of a rectangle around (cx, cy) given some heading
        points = [
            (cx - dxw - dxl, cy - dyw - dyl),
            (cx + dxw - dxl, cy + dyw - dyl),
            (cx + dxw + dxl, cy + dyw + dyl),
            (cx - dxw + dxl, cy - dyw + dyl),
        ]

        s = m.getPartialZoom(0.5)
        Utility.drawPolygon(screen, Utility.BLACK, points, 3 * s)

        # Draw arrow
        tx = cx + math.cos(theta)*length * 0.4
        ty = cy + math.sin(theta)*length * 0.4
        Utility.drawLine(screen, Utility.BLACK, cx, cy, tx, ty, 4  * s)
        Utility.drawPolarTriangle(screen, Utility.BLACK, tx, ty, theta, 7 * s, 1, math.pi / 2)

        self.pointIndex += 1
        return True
