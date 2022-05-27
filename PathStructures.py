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
        return Utility.distance(self.x, self.y, m.x, m.y) <= Pose.RADIUS + 5

    def draw(self, screen, forceOrange = False):

        r = Pose.RADIUS + 2 if self.hovered else Pose.RADIUS

        if forceOrange:
            color = Utility.ORANGE
            r += 3
        else:
            color = Utility.RED if self.isBreak else Utility.GREEN

        #  draw triangle
        if self.theta is not None:
            a = 0.9
            x1 = self.x + r * math.cos(self.theta - a)
            y1 = self.y + r * math.sin(self.theta - a)
            x2 = self.x + r * math.cos(self.theta + a)
            y2 = self.y + r * math.sin(self.theta + a)
            x3 = self.x + 2.3 * r * math.cos(self.theta)
            y3 = self.y + 2.3 * r * math.sin(self.theta)
            Utility.drawTriangle(screen, Utility.BLACK, x1, y1, x2, y2, x3, y3)

        Utility.drawCircle(screen, self.x, self.y, color, r)
        
        if self.showCoords or self.hovered:
            string = "({},{})".format(round(Utility.pixelsToTiles(self.x), 2), round(Utility.pixelsToTiles(Utility.SCREEN_SIZE - self.y), 2))
            Utility.drawText(screen, Utility.FONT20, string, Utility.TEXTCOLOR, self.x, self.y - 25)

class PathType(Enum):
    LINEAR  = 1
    CURVE = 2

    def succ(self):
        return PathType(self.value % 2 + 1)
        
class Path:
    
    def __init__(self):

        self.poses = []
        self.paths = [] # size of paths is size of self.poses - 1, specifies PathType between poses

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
        

    def handleMouse(self, m):

        if m.poseDragged is not None:
            
            if m.pressing: 
                if m.startDragX != m.x or m.startDragY != m.y: # make sure mouse actually has moved
                    m.poseDragged.x = m.x
                    m.poseDragged.y = m.y
            else:
                if m.released and m.startDragX == m.x and m.startDragY == m.y:
                    m.poseDragged.showCoords = not m.poseDragged.showCoords
                    
                m.poseDragged = None
       
        anyHovered = False
        for pose in self.poses:
            if pose.touching(m):
                anyHovered = True
                pose.hovered = True

                if m.pressedR:
                    pose.isBreak = not pose.isBreak

                if m.keyX:
                    self.deletePose(pose)
                elif m.pressed and m.poseDragged is None:
                    m.poseDragged = pose
                    m.startDragX = m.x
                    m.startDragY = m.y
            else:
                pose.hovered = False

        self.pathIndex = -1 if anyHovered else self.getTouchingPathIndex(m.x, m.y)

        # Toggle type of path if c pressed
        if self.pathIndex != -1 and m.pressedC:
            self.paths[self.pathIndex] = self.paths[self.pathIndex].succ()

        if not anyHovered and m.pressed:
            self.addPose(m.x, m.y)

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
            
            self.poses.append(Pose(px, py, 3*math.pi/2 if len(self.poses) == 0 else None)) # only the first pose has a predefined position
            if len(self.poses) >= 2: # no path created if it's only one node
                self.paths.append(PathType.LINEAR if len(self.paths) == 0 else self.paths[-1])
                
        else: # insert between two poses
        
            self.poses.insert(self.pathIndex + 1, Pose(px, py, None))

            self.paths.insert(self.pathIndex, self.paths[self.pathIndex])
    

    def draw(self, screen):

        if len(self.poses) == 0:
            return
        
        for i in range(1, len(self.poses)):
            color = Utility.LINEDARKGREY if (self.pathIndex == i-1) else Utility.LINEGREY
            Utility.drawLine(screen, color, self.poses[i-1].x, self.poses[i-1].y, self.poses[i].x, self.poses[i].y, 3)

        first = True
        for pose in self.poses:
            pose.draw(screen, first)
            first = False

    def drawPoints(self, screen, ds):

        s = 0

        for i in range(len(self.paths)):

            if self.paths[i] == PathType.LINEAR:
                magnitude = Utility.distance(self.poses[i].x, self.poses[i].y, self.poses[i+1].x, self.poses[i+1].y)
                normx = (self.poses[i+1].x - self.poses[i].x) / magnitude
                normy = (self.poses[i+1].y - self.poses[i].y) / magnitude
                while s < magnitude:
                    x = self.poses[i].x + normx * s
                    y = self.poses[i].y + normy * s
                    Utility.drawCircle(screen, x, y, Utility.BLUE, 2)
                    s += ds
                s -= magnitude # any "spillover" gets carried over to the next point in the next path so that across all paths, every segment is equidistant

            else: # PathType.CURVE

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
                    Utility.drawCircle(screen, x, y, Utility.RED, 2)

                    dxds,dyds = SplineCurves.getSplineGradient(ns, P1, P2, P3, P4)
                    dsdt = ds / Utility.hypo(dxds, dyds)
                    ns += dsdt

                s = ds - Utility.distance(x,y,*P3)

            # no spillovers at break points
            if self.poses[i+1].isBreak:
                s = 0
