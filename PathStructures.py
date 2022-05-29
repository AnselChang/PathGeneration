from enum import Enum
import Utility, math
import SplineCurves

class Pose:

    RADIUS = 6
    
    # units are in SCREEN PIXELS (which would be converted to inches during export) and theta is in degrees (0-360)
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta  = theta
        self.hovered = False
        self.showCoords = False
        self.isBreak = False # a break pose is a stopping pose where poses on one side of this pose don't affect the other

    def touching(self, m):
        return Utility.distance(self.x, self.y, m.zx, m.zy) <= (Pose.RADIUS + 5)

    def draw(self, screen, m, forceOrange = False):

        r = (Pose.RADIUS + 2 if self.hovered else Pose.RADIUS) * m.getPartialZoom(1.5)
        x, y = m.inchToPixel(self.x, self.y)

        if forceOrange:
            color = Utility.ORANGE
            r += 3
        else:
            color = Utility.RED if self.isBreak else Utility.GREEN

        #  draw triangle
        if self.theta is not None:
            a = 0.9
            x1 = x + r * math.cos(self.theta - a)
            y1 = y + r * math.sin(self.theta - a)
            x2 = x + r * math.cos(self.theta + a)
            y2 = y + r * math.sin(self.theta + a)
            x3 = x + 2.3 * r * math.cos(self.theta)
            y3 = y + 2.3 * r * math.sin(self.theta)
            Utility.drawTriangle(screen, Utility.BLACK, x1, y1, x2, y2, x3, y3)

        Utility.drawCircle(screen, x, y, color, r)
        
        if self.showCoords or self.hovered:
            string = "({},{})".format(round(self.x, 1), round(self.y, 1))
            Utility.drawText(screen, Utility.getFont(23 * m.getPartialZoom(1.02)), string, Utility.TEXTCOLOR, x, y - 25*m.getPartialZoom(1.2))

class PathType(Enum):
    LINEAR  = 1
    CURVE = 2

    def succ(self):
        return PathType(self.value % 2 + 1)

# Each point is generated through interpolating between poses
class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = None
        
class Path:
    
    def __init__(self, segmentDistance):

        self.poses = []
        self.paths = [] # size of paths is size of self.poses - 1, specifies PathType between poses
        self.points = []

        self.segmentDistance = segmentDistance

        self.pathIndex = -1

    def getPoseIndex(self, pose):
        index = -1
        for i in range(len(self.poses)):
            if self.poses[i] == pose:
                index  = i
                break
        return index

    def deletePose(self, pose):
        index  = self.getPoseIndex(pose)
        if index == -1:
            return

        if len(self.paths) != 0:
            del self.paths[max(index - 1, 0)]

        if index == 0 and len(self.poses) > 1 and self.poses[1].theta is None:
            self.poses[1].theta = self.poses[0].theta
        self.poses.remove(pose)

    def getTouchingPathIndex(self, x, y):

        if len(self.poses) == 0:
            return -1
        
        x1 = self.poses[0].x
        y1 = self.poses[0].y
        
        for i in range(1, len(self.poses)):

            x2 = self.poses[i].x
            y2 = self.poses[i].y
            
            if Utility.pointTouchingLine(x, y, x1, y1, x2, y2, 10):
                return i - 1

            x1 = x2
            y1 = y2

        return -1
        
    def handleMouseHeading(self, m):

        if not m.pressing:
            m.poseSelectHeading = None

        # update heading for pose
        if m.poseSelectHeading is not None:
            p = m.poseSelectHeading
            px, py = m.inchToPixel(p.x, p.y)
            
            if  p is not self.poses[0] and Utility.distance(m.x, m.y, px, py) < Pose.RADIUS*2: # for close distances, remove heading. But first MUST have heading
                p.theta = None
            else: # Otherwise, get heading from normalized vector from center to mouse
                p.theta = math.atan2(m.y - py, m.x - px)

            self.interpolatePoints()
                

    def handleHoveringOverPoses(self, m):

        anyHovered = False
        
        if m.poseDragged is None and m.poseSelectHeading is None:
            for pose in self.poses:
                if pose.touching(m):
                    anyHovered = True
                    pose.hovered = True

                    if m.pressedR:
                        pose.isBreak = not pose.isBreak

                    if m.keyX:
                        self.deletePose(pose)
                        self.interpolatePoints()
                    elif m.pressed and m.poseDragged is None:
                        if m.keyZ:
                            m.poseSelectHeading = pose
                        else:
                            m.poseDragged = pose
                            m.startDragX = m.x
                            m.startDragY = m.y
                else:
                    pose.hovered = False

        return anyHovered
    
    def handleMouse(self, m):

        # Handle scrolling the field
        if not m.pressing:
            m.scrolling = False
        if m.scrolling:
            dx = m.x - m.prevX
            dy = m.y - m.prevY
            m.panX += dx
            m.panY += dy
            m.boundFieldPan()
        self.handleMouseHeading(m)

        # Update dragging and handle toggling showCoords
        if m.poseDragged is not None:
            
            if m.pressing: 
                if m.startDragX != m.x or m.startDragY != m.y: # make sure mouse actually has moved
                    m.poseDragged.x = m.zx
                    m.poseDragged.y = m.zy
                    self.interpolatePoints()
            else:
                if m.released and m.startDragX == m.x and m.startDragY == m.y:
                    m.poseDragged.showCoords = not m.poseDragged.showCoords
                    
                m.poseDragged = None
       
        anyHovered = self.handleHoveringOverPoses(m)

        self.pathIndex = -1 if (anyHovered or m.poseSelectHeading is not None) else self.getTouchingPathIndex(m.zx, m.zy)

        # Toggle type of path if c pressed
        if self.pathIndex != -1 and m.pressedC:
            self.paths[self.pathIndex] = self.paths[self.pathIndex].succ()
            self.interpolatePoints()

        if not anyHovered:
            if m.pressedR:
                self.addPose(m.zx, m.zy)
            elif m.pressed:
                m.scrolling = True

        return anyHovered

    def getMousePosePosition(self, x, y):

        if self.pathIndex == -1:
               return (x, y)
        else:
            p1, p2 = self.poses[self.pathIndex], self.poses[self.pathIndex+1]
            return Utility.pointOnLineClosestToPoint(x, y, p1.x, p1.y, p2.x, p2.y)

    def addPose(self, x, y):

        px, py = self.getMousePosePosition(x,y)

         
        if self.pathIndex == -1: # add to the end
            
            self.poses.append(Pose(px, py, -math.pi/2 if len(self.poses) == 0 else None)) # only the first pose has a predefined position (pointing up)
            if len(self.poses) >= 2: # no path created if it's only one node
                self.paths.append(PathType.LINEAR if len(self.paths) == 0 else self.paths[-1])
                
        else: # insert between two poses
        
            self.poses.insert(self.pathIndex + 1, Pose(px, py, None))

            self.paths.insert(self.pathIndex, self.paths[self.pathIndex])

        self.interpolatePoints()
    

    def drawPaths(self, screen, m):

        if len(self.poses) == 0:
            return
        
        for i in range(1, len(self.poses)):
            color = Utility.LINEDARKGREY if (self.pathIndex == i-1) else Utility.LINEGREY
            Utility.drawLine(screen, color, *m.inchToPixel(self.poses[i-1].x, self.poses[i-1].y), *m.inchToPixel(self.poses[i].x, self.poses[i].y), 2 *  m.getPartialZoom(1.5))

        first = True
        for pose in self.poses:
            pose.draw(screen, m, first)
            first = False

    # Interpolate pose[i] to pose[i+1] linearly with s spillover
    def interpolateLinear(self, i, s):

        magnitude = Utility.distance(self.poses[i].x, self.poses[i].y, self.poses[i+1].x, self.poses[i+1].y)
        normx = (self.poses[i+1].x - self.poses[i].x) / magnitude
        normy = (self.poses[i+1].y - self.poses[i].y) / magnitude
        while s < magnitude:
            x = self.poses[i].x + normx * s
            y = self.poses[i].y + normy * s
            self.points.append(Point(x, y, Utility.BLUE))
            s += self.segmentDistance
        s -= magnitude # any "spillover" gets carried over to the next point in the next path so that across all paths, every segment is equidistant

        return s

    # Interpolate pose[i] to pose[i+1] using Catmull-Rom spline curve with s spillover
    def interpolateSplineCurve(self, i, s):

        P2 = [self.poses[i].x, self.poses[i].y]
        P1 = P2 if i == 0 else [self.poses[i-1].x, self.poses[i-1].y]
        P3 = [self.poses[i+1].x, self.poses[i+1].y]
        P4 = P3 if i+2 == len(self.poses) else [self.poses[i+2].x, self.poses[i+2].y]

        # Find starting point from previous "spillover"
        if s == 0:
            ns = 0
        else:
            dxds,dyds = SplineCurves.getSplineGradient(0, P1, P2, P3, P4)
            dsdt = s / Utility.hypo(dxds, dyds)
            ns = dsdt # s normalized from 0 to 1 for this specific spline

        while ns < 1:
            x,y = SplineCurves.getSplinePoint(ns, P1, P2, P3, P4)
            self.points.append(Point(x, y, Utility.RED))

            dxds,dyds = SplineCurves.getSplineGradient(ns, P1, P2, P3, P4)
            dsdt = self.segmentDistance / Utility.hypo(dxds, dyds)
            ns += dsdt

        s = self.segmentDistance - Utility.distance(x,y,*P3)
        return s

    # Interpolate between all the *given* thetas, as in some poses do not specify theta and should just be interpolated between the poses besides them
    def interpolateTheta(self, knownThetaIndexes):

        i1, theta1 = knownThetaIndexes[0]
        assert i1 == 0
        for ki in range(1, len(knownThetaIndexes)):
            i2, theta2 = knownThetaIndexes[ki]

            for i in range(0, i2-i1+1):
                # Eliminate mod "wraparounds" by always finding the closest direction to spin
                theta2adjusted = theta2
                if theta2 - theta1 >= math.pi:
                    theta2adjusted -= 2*math.pi
                elif theta1 - theta2 >= math.pi:
                    theta2adjusted += 2*math.pi
                    
                self.points[ i1 + i].theta = theta1 + (theta2adjusted - theta1) * (i / (i2-i1))    

            i1 = i2
            theta1 = theta2

        # For all the points past the last known theta index, just set theta to the same number
        for index in range(i1, len(self.points)):
            self.points[index].theta = theta1

    # Call this function to update self.points whenever there is a change in interpolation. Generates a list of points from the entire combined path
    def interpolatePoints(self):

        self.points = []
        knownThetaIndexes = [] # for the purposes of interpolating theta after initially generating list of points

        if len(self.paths) == 0:
            return

        s = 0
        for i in range(len(self.paths)):

            if self.poses[i].x == self.poses[i+1].x and self.poses[i].y == self.poses[i+1].y:
                continue

            # Mark point with theta if pose has specified theta
            if self.poses[i].theta is not None:
                knownThetaIndexes.append([len(self.points), self.poses[i].theta])

            if self.paths[i] == PathType.LINEAR:
                s = self.interpolateLinear(i, s)

            else: # PathType.CURVE
                s = self.interpolateSplineCurve(i, s)

            # no spillovers at break points
            if self.poses[i+1].isBreak:
                s = 0

        # Mark last point with theta if it exists
        if self.poses[-1].theta is not None:
            knownThetaIndexes.append([len(self.points)-1, self.poses[-1].theta])

        if len(self.poses) > 1:
            self.interpolateTheta(knownThetaIndexes)

    def drawPoints(self, screen, m):

        POINT_SIZE = 1
        TANGENT_LENGTH = 10


        for p in self.points:
            p.px, p.py = m.inchToPixel(p.x, p.y)
            Utility.drawLine(screen, Utility.PURPLE, p.px, p.py, *Utility.vector(p.px, p.py, p.theta, TANGENT_LENGTH *  m.getPartialZoom(1.25)),  m.getPartialZoom(1.5))
        
        for p in self.points:
            Utility.drawCircle(screen, p.px, p.py, p.color, POINT_SIZE * m.getPartialZoom(1.5))
