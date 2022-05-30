import math, Utility

class Robot:

    def __init__(self, width, length):
        self.width = width
        self.length = length

    def startSimulation(self, points):
        self.points = points
        self.pointIndex = 0

    # return if animation is still going
    def simulationTick(self, screen):

        if self.pointIndex == len(self.points):
            return False
        
        p = self.points[self.pointIndex]
        cx, cy, theta = p.x, p.y, p.theta

        dxw = math.cos(theta) * self.width
        dyw = math.sin(theta) * self.width
        dxl = math.cos(theta) * self.length
        dyl = math.sin(theta) * self.length
        print(theta, dxw, dyw, dxl,  dyl)

        # Generate four points of a rectangle around (cx, cy) given some heading
        points = [
            (cx - dxw - dxl, cy - dyw - dyl),
            (cx + dxw - dxl, cy + dyw - dyl),
            (cx + dxw + dxl, cy + dyw + dyl),
            (cx - dxw + dxl, cy - dyw + dyl),
        ]
        print(points)

        Utility.drawPolygon(screen, Utility.BLACK, points, 3)

        self.pointIndex += 1
        return True
