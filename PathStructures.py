class Pose:

    RADIUS = 5
    
    # units are in SCREEN PIXELS (which would be converted to inches during export) and theta is in degrees (0-360)
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta  = theta
        self.hovered = False

    def touching(self, m):
        return distance(self.x, self.y, m.x, m.y) <= Pose.RADIUS

    def draw(self, screen):
        drawCircle(screen, self.x, self.y, GREEN, Pose.RADIUS + 3 if self.hovered else Pose.RADIUS)

class PathType(Enum):
    LINEAR  = 1
    CURVE = 2
        
class Path:
    
    def __init__(self):

        self.poses = []
        self.paths = [] # size of paths is size of self.poses - 1, specifies PathType between poses

    def handleMouse(self, m):

        if m.poseDragged is not None:
            if not m.pressing:
                m.poseDragged = None
            else:
                m.poseDragged.x = m.x
                m.poseDragged.y = m.y

        anyHovered = False
        for pose in self.poses:
            if pose.touching(m):
                anyHovered = True
                pose.hovered = True

                if m.pressed and m.poseDragged is None:
                    m.poseDragged = pose
            else:
                pose.hovered = False

        return anyHovered

    def addPose(self, x, y, theta):
            self.poses.append(Pose(x, y, theta))

    def draw(self, screen):
        for pose in self.poses:
            pose.draw(screen)
