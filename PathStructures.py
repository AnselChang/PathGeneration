from enum import Enum
import Utility

class Pose:

    RADIUS = 5
    
    # units are in SCREEN PIXELS (which would be converted to inches during export) and theta is in degrees (0-360)
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta  = theta
        self.hovered = False

    def touching(self, m):
        return Utility.distance(self.x, self.y, m.x, m.y) <= Pose.RADIUS + 5

    def draw(self, screen):
        Utility.drawCircle(screen, self.x, self.y, Utility.GREEN, Pose.RADIUS + 3 if self.hovered else Pose.RADIUS)

class PathType(Enum):
    LINEAR  = 1
    CURVE = 2
        
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

        self.pathIndex = self.getTouchingPathIndex(m.x, m.y)

        if m.poseDragged is not None:
            if m.pressing:
                m.poseDragged.x = m.x
                m.poseDragged.y = m.y
            else:
                m.poseDragged = None
       
        anyHovered = False
        for pose in self.poses:
            if pose.touching(m):
                anyHovered = True
                pose.hovered = True

                if m.keyX:
                    self.deletePose(pose)
                elif m.pressed and m.poseDragged is None:
                    m.poseDragged = pose
            else:
                pose.hovered = False

        if not anyHovered and m.pressed:
            self.addPose(m.x, m.y, 0)

        return anyHovered

    def getMousePosePosition(self, x, y):

        if self.pathIndex == -1:
               return (x, y)
        else:
            p1, p2 = self.poses[self.pathIndex], self.poses[self.pathIndex+1]
            return Utility.pointOnLineClosestToPoint(x, y, p1.x, p1.y, p2.x, p2.y)

    def addPose(self, x, y, theta):

        px, py = self.getMousePosePosition(x,y)

         
        if self.pathIndex == -1: # add to the end
            
            self.poses.append(Pose(px, py, theta))
            if len(self.poses) >= 2: # no path created if it's only one node
                self.paths.append(PathType.LINEAR)
                
        else: # insert between two poses
        
            self.poses.insert(self.pathIndex + 1, Pose(px, py, theta))
            self.paths.insert(self.pathIndex, PathType.LINEAR)
    

    def draw(self, screen):

        if len(self.poses) == 0:
            return
        
        for i in range(1, len(self.poses)):
            color = Utility.LINEDARKGREY if (self.pathIndex == i-1) else Utility.LINEGREY
            Utility.drawLine(screen, color, self.poses[i-1].x, self.poses[i-1].y, self.poses[i].x, self.poses[i].y, 3)

        for pose in self.poses:
            pose.draw(screen)
