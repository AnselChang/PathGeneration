import math, Utility, random

STEP_TIME = 0.02 # 20 millisecond cycle time
K_P_TRANS = 30
K_P_ROT = 1
STOP_DISTANCE_THRESHOLD = 1 # In inches, pathfinding algo terminates when distance to destination dips below threshold
POSITION_NOISE = 0.1 # position noise in inches that cna be generated at each timestep. triangular distribution with [-POSITION_NOISE, POSITION_NOISE]

# A point at some timestep in the simulation, generated numerically from some pathfinding algorithm, which can differ slightly from the theoretical trajectory
class SimulationPoint:
    def __init__(self, x, y, theta, **kwargs):
        self.x = x
        self.y = y
        self.theta = theta

        self.__dict__.update(kwargs) # handy way to store any keyword arguments as instance variables

# Abstract
class GenericRobot:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.simulation = None

    def startSimulation(self, points):
        raise NotImplementedError("Must implement this function")

    # return if animation is still going
    def simulationTick(self, screen, m, pointIndex):

        if pointIndex == len(self.simulation):
            return False
        
        p = self.simulation[pointIndex]
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

        return True

class IdealRobot(GenericRobot):

    def __init__(self, width, height):
        super().__init__(width, height)

    # With an ideal robot, the robot's actual position in each timestep is what it is supposed to be
    def startSimulation(self, points):
        self.simulation = [SimulationPoint(p.x, p.y, p.theta) for p in points]
        return len(self.simulation)

class PurePursuitRobot(GenericRobot):

    # lookahead in inches
    # acceleration limits in inches/seconds^2
    def __init__(self, width, height, lookahead, maxTransAccel, maxRotAccel):
        super().__init__(width, height)
        self.lookahead = lookahead
        self.maxTransAccel = maxTransAccel
        self.maxRotAccel = maxRotAccel

    # Find closest point to (x,y) in points, from index range [start, end)
    # Returns index of closest point in points lis
    def findClosestPoint(self, points, x, y, start, end):

        start = max(start, 0)
        end = min(end, len(points) - 1)

        minIndex = start
        minDist = Utility.distance(x, y, points[start].x, points[start].y)
        start += 1
        while start < end:
            dist = Utility.distance(x, y, points[start].x, points[start].y)
            if dist < minDist:
                minIndex = start
                minDist = dist
            start += 1

        return minIndex

    # starting x, y, theta
    def startSimulation(self, points):

        MAX_TIMESTEPS = 1000
        timestep = 0

        self.simulation = []

        # Start pose, which has inbuilt noise
        x = points[0].x + 10 * random.triangular(-POSITION_NOISE, POSITION_NOISE)
        y = points[0].y + 10 * random.triangular(-POSITION_NOISE, POSITION_NOISE)
        theta = points[0].theta
        
        xvel = 0 # velocities in inches/second
        yvel = 0
        tvel = 0 # angular velocity
        li = 0 # lookahead index
        ci = 0 # closest index

        while li != len(points) - 1 or Utility.distance(points[-1].x, points[-1].y, x, y) < STOP_DISTANCE_THRESHOLD:

            if timestep > MAX_TIMESTEPS:
                break

            # Find closest waypoint within 5 points of the current waypoint
            ci = self.findClosestPoint(points, x, y, ci - 5, ci + 5)
        
            # Update lookahead distance
            while li < len(points) - 1 and Utility.distance(points[li].x, points[li].y, points[ci].x, points[ci].y) < self.lookahead:
                li += 1

             # Calculate target velocities
            targetXVel = (points[li].x - x) * K_P_TRANS
            targetYVel = (points[li].y - y) * K_P_TRANS

            dtheta = (points[li].theta - theta) % (2*math.pi)
            if dtheta > math.pi:
                dtheta -= math.pi
            targetTVel = dtheta * K_P_ROT

            # I'd constrain individual wheel accelerations here but I don't know mecanum kinematics yet

            # Update velocities given target velocities, with acceleration limits in mind
            xvel += Utility.clamp(targetXVel - xvel, -self.maxTransAccel, self.maxTransAccel)
            yvel += Utility.clamp(targetYVel - yvel, -self.maxTransAccel, self.maxTransAccel)
            tvel += Utility.clamp(targetTVel - tvel, -self.maxRotAccel, self.maxRotAccel)

            # d = r * t
            x += xvel * STEP_TIME + random.triangular(-POSITION_NOISE, POSITION_NOISE) # add positional noise to simulation for realism 
            y += yvel * STEP_TIME + random.triangular(-POSITION_NOISE, POSITION_NOISE)
            theta += tvel * STEP_TIME

            # Add timestep to simulation
            self.simulation.append(SimulationPoint(x, y, theta, xvel = xvel, yvel = yvel, tvel = tvel, cx = points[ci].x, cy = points[ci].y, lx = points[li].x, ly = points[li].y))
            timestep += 1

        print("Simulation length: ", len(self.simulation))
        return len(self.simulation)

    # Override generic simulationTick by drawing stats and lookahead line
    def simulationTick(self, screen, m, pointIndex):

        ret = super().simulationTick(screen, m, pointIndex)

        # Draw position and velocity stats
        p = self.simulation[pointIndex]
        Utility.drawText(screen, Utility.getFont(30), "Pure Pursuit", Utility.BLACK, 200, 30, 0)
        Utility.drawText(screen, Utility.getFont(20), "xpos: {} inch".format(round(p.x, 2)), Utility.BLACK, 200, 50, 0)
        Utility.drawText(screen, Utility.getFont(20), "ypos: {} inch".format(round(p.y, 2)), Utility.BLACK, 200, 65, 0)
        Utility.drawText(screen, Utility.getFont(20), "theta: {} deg".format(round(p.theta * 180 / math.pi, 2)), Utility.BLACK, 200, 80, 0)
        Utility.drawText(screen, Utility.getFont(20), "xvel: {} inch/sec".format(round(p.xvel, 2)), Utility.BLACK, 330, 50, 0)
        Utility.drawText(screen, Utility.getFont(20), "yvel: {} inch/sec".format(round(p.yvel, 2)), Utility.BLACK, 330, 65, 0)
        Utility.drawText(screen, Utility.getFont(20), "tvel: {} deg/sec".format(round(p.tvel * 180 / math.pi, 2)), Utility.BLACK, 330, 80, 0)

        # Draw lookahead line

        lx, ly = m.inchToPixel(p.lx, p.ly)
        Utility.drawCircle(screen, *m.inchToPixel(p.cx, p.cy), Utility.ORANGE, 2)
        Utility.drawLine(screen, Utility.GREEN, *m.inchToPixel(p.x, p.y), lx, ly, 2)
        Utility.drawCircle(screen, lx, ly, Utility.GREEN, 2)
        
        

        return ret
        
    
