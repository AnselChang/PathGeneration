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
       

    def handleMouse(self, m):

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

        return anyHovered

    def addPose(self, x, y, theta):
            self.poses.append(Pose(x, y, theta))
            if len(self.poses) >= 2: # no path created if it's only one node
                self.paths.append(PathType.LINEAR)

    def draw(self, screen):

        if len(self.poses) == 0:
            return
        
        for i in range(1, len(self.poses)):
            Utility.drawLine(screen, Utility.LINEGREY, self.poses[i-1].x, self.poses[i-1].y, self.poses[i].x, self.poses[i].y, 3)

        for pose in self.poses:
            pose.draw(screen)
