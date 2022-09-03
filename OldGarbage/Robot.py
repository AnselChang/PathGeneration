import math, Utility, random, Slider

STEP_TIME = 0.02 # 20 millisecond cycle time
STOP_DISTANCE_THRESHOLD = 1 # In inches, pathfinding algo terminates when distance to destination dips below threshold
POSITION_NOISE = 0.1 # position noise in inches that cna be generated at each timestep. triangular distribution with [-POSITION_NOISE, POSITION_NOISE]

MAX_TRANS_ACCEL= 120 # in/s^2
MAX_ROT_ACCEL = 100 # deg/s^2
MAX_SPEED = 60 # in/s

# convert to accel per timestep, which is 20 msec
MAX_TRANS_ACCEL *= 0.02
MAX_ROT_ACCEL *= 0.02

# A point at some timestep in the simulation, generated numerically from some pathfinding algorithm, which can differ slightly from the theoretical trajectory
class SimulationPoint:
    def __init__(self, x, y, theta, **kwargs):
        self.x = x
        self.y = y
        self.theta = theta

        self.__dict__.update(kwargs) # handy way to store any keyword arguments as instance variables

class PID:
    def __init__(self, KP, KI, KD):
        self.KP = KP
        self.KI = KI
        self.KD = KD

        self.prevError = 0
        self.prevIntegral = 0
        
    def tick(self, error):

        integral = self.prevIntegral + error * STEP_TIME
        derivative = (error - self.prevError) / STEP_TIME
        self.prevError = error
        self.prevIntegral = integral

        return self.KP * error + self.KI * integral + self.KD * derivative

# Abstract
class GenericRobot:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.simulation = None
        self.error = -1
        self.prevPoints = None

    # should return simulation list and error
    def computeSimulation(self, points):
        raise NotImplementedError("Must implement this function")

    # By default, no calibration happens
    def autoCalibrate(self):
        return

    def restartSimulation(self, m, slider):
        self.startSimulation(m, slider, self.prevPoints)

    def startSimulation(self, m, slider, points):
        self.prevPoints = points
        slider.reset()

        m.simulating = True
        m.playingSimulation = False
        m.poseDragged = None
        m.poseSelectHeading = None

        # Calculate curvature of each point
        points[0].curve = 0
        points[-1].curve = 0
        for i in range(1, len(points) - 1):
            angle = math.atan2(points[i+1].y - points[i-1].y, points[i+1].x - points[i-1].x) - math.atan2(points[i].y - points[i-1].y, points[i].x - points[i-1].x)
            if angle > math.pi:
                angle -= 2*math.pi
            points[i].curve = abs(angle)

        self.simulation, self.error = self.computeSimulation(points)
        slider.high =  len(self.simulation) - 1

    # return if animation is still going
    def simulationTick(self, screen, m, pointIndex):

        self.pointIndex = pointIndex

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

    def totalTime(self):
        return (len(self.simulation)-1) * STEP_TIME

    def drawPanel(self, screen):

        # Draw timestamp
        Utility.drawText(screen, Utility.getFont(30), "Avg. error: {}\"".format(round(self.error, 2)), Utility.BLACK, 865, 70, 0)
        Utility.drawText(screen, Utility.getFont(30), "Time: {:.2f}s / {:.2f}s".format(self.pointIndex * STEP_TIME, self.totalTime()), Utility.BLACK, 865, 100, 0)
        

class IdealRobot(GenericRobot):

    def __init__(self, width, height):
        super().__init__(width, height)

    # With an ideal robot, the robot's actual position in each timestep is what it is supposed to be
    def computeSimulation(self, points):
        return ([SimulationPoint(p.x, p.y, p.theta) for p in points], 0)

class PurePursuitRobot(GenericRobot):

    # lookahead in inches
    # acceleration limits in inches/seconds^2
    def __init__(self, width, height, defLookahead = 6, defKP = 30, defKD = 5):
        super().__init__(width, height)

        self.lookaheadSlider = Slider.Slider(830, 1070, 270, 1, 20, defLookahead, "Lookahead (inches)", 2)
        self.kpSlider = Slider.Slider(830, 1070, 350, 1, 100, defKP, "Translation KP", 2)
        self.kdSlider = Slider.Slider(830, 1070, 430, 0, 20, defKD, "Translation KD", 2)

    def handleSliders(self, m, slider):
        recalculate = self.lookaheadSlider.handleMouse() or self.kpSlider.handleMouse() or self.kdSlider.handleMouse()
        if recalculate:
            self.restartSimulation(m, slider)

    def evaluate(self, simulation, error):

        time = (len(simulation)-1) * STEP_TIME # in seconds
        errorImportance = 1
        return time + error * error * errorImportance

    # the lower the better
    def staticEvaluation(self, l, kp, kd):

        simulation, error = self.computeSimulation(self.prevPoints, lookaheadOffset = l, kpOffset = kp, kdOffset = kd) # in inches
        
        return self.evaluate(simulation, error)
        
    # stochastic gradient descent
    def autoCalibrate(self, m, slider):
        NUM_EPOCHS = 1
        NUM_SAMPLES = 5
        H = 0.75 # the amount to change the parameter by to calculate slope. As H -> 0, slope is theoretically more accurate but gets more influenced by variance
        LEARNING_RATE = 0.75

        startScore = self.evaluate(self.simulation, self.error)
        print("START:")
        print("{} -> look: {}\tkp: {}\tkd: {}\n".format(round(startScore, 2), self.lookaheadSlider.value, self.kpSlider.value, self.kdSlider.value))
        for epoch in range(NUM_EPOCHS):

            derivatives = []
            
            for l, kp, kd in [[1,0,0], [0,1,0], [0,0,1]]:

                score = sum([self.staticEvaluation(l, kp, kd) for i in range(NUM_SAMPLES)]) / NUM_SAMPLES # get average  eval over number of samples
                print("{} -> look: {}\tkp: {}\tkd: {}".format(round(score, 2), self.lookaheadSlider.value + l*H, self.kpSlider.value + kp*H, self.kdSlider.value + kd*H))
                
                derivatives.append((score - startScore) / H) # approximate derivative through slope

            # We want to DESCENT the gradient, so go the opposite the direction of the partial derivative
            self.lookaheadSlider.increment(-derivatives[0] * LEARNING_RATE) 
            self.kpSlider.increment(-derivatives[1] * LEARNING_RATE)
            self.kdSlider.increment(-derivatives[2] * LEARNING_RATE)
            print ("Change to: {}, {}, {}".format(self.lookaheadSlider.value, self.kpSlider.value, self.kdSlider.value))
            print("Derivatives: ", derivatives)

        self.restartSimulation(m, slider)
                
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
    def computeSimulation(self, points, lookaheadOffset = 0, kpOffset = 0, kdOffset = 0):

        MAX_TIMESTEPS = 10000
        timestep = 0

        simulation = []
        # Start pose, which has inbuilt noise
        x = points[0].x + 10 * random.triangular(-POSITION_NOISE, POSITION_NOISE)
        y = points[0].y + 10 * random.triangular(-POSITION_NOISE, POSITION_NOISE)
        theta = points[0].theta

        pidX = PID(self.kpSlider.value + kpOffset, 0, self.kdSlider.value + kdOffset)
        pidY = PID(self.kpSlider.value + kpOffset, 0, self.kdSlider.value + kdOffset)
        pidRot = PID(2, 0, 0)
        
        xvel = 0 # velocities in inches/second
        yvel = 0
        tvel = 0 # angular velocity
        li = 0 # lookahead index
        ci = 0 # closest index

        errorSum = 0

        while li != len(points) - 1 or Utility.distance(points[-1].x, points[-1].y, x, y) > STOP_DISTANCE_THRESHOLD:

            if timestep > MAX_TIMESTEPS:
                break

            # Find closest waypoint within 5 points of the current waypoint
            ci = self.findClosestPoint(points, x, y, ci, ci + 30)
        
            # Update lookahead distance
            li = ci
            while li < len(points) - 1 and Utility.distance(points[li].x, points[li].y, points[ci].x, points[ci].y) < self.lookaheadSlider.value + lookaheadOffset:
                li += 1

             # Calculate target velocities
            targetXVel = pidX.tick(points[li].x - x)
            targetYVel = pidY.tick(points[li].y - y)

            # Constrain maximum robot speed
            mag = Utility.hypo(targetXVel, targetYVel)
            scalar = min(1, MAX_SPEED / mag)
            targetXVel *= scalar
            targetYVel *= scalar
            
            # Calculate heading delta (turn the fastest way)
            dtheta = (points[li].theta - theta) % (2*math.pi)
            if dtheta > math.pi:
                dtheta -= 2*math.pi
            targetTVel = pidRot.tick(dtheta)

            # I'd constrain individual wheel accelerations here but I don't know mecanum kinematics yet

            # Update velocities given target velocities, and constrain with acceleration limits
            xvel += Utility.clamp(targetXVel - xvel, -MAX_TRANS_ACCEL, MAX_TRANS_ACCEL)
            yvel += Utility.clamp(targetYVel - yvel, -MAX_TRANS_ACCEL, MAX_TRANS_ACCEL)
            tvel += Utility.clamp(targetTVel - tvel, -MAX_ROT_ACCEL, MAX_ROT_ACCEL)

            # Update distance from actual velocity
            x += xvel * STEP_TIME + random.triangular(-POSITION_NOISE, POSITION_NOISE) # add positional noise to simulation for realism 
            y += yvel * STEP_TIME + random.triangular(-POSITION_NOISE, POSITION_NOISE)
            theta += tvel * STEP_TIME

            # Add timestep to simulation
            if ci == 0:
                ox, oy = points[ci+1].x, points[ci+1].y
            else:
               ox, oy = points[ci-1].x, points[ci-1].y

            error = Utility.distanceTwoPoints(x, y, points[ci].x, points[ci].y, ox, oy)
            errorSum += error
            sp = SimulationPoint(x, y, theta, xvel = xvel, yvel = yvel, tvel = tvel,
                                 cx = points[ci].x, cy = points[ci].y, lx = points[li].x, ly = points[li].y, curve = points[li].curve,
                                 error = error)
            simulation.append(sp)
            timestep += 1

        return [simulation, 0 if len(simulation) == 0 else (errorSum / len(simulation))]

    
    # Override generic simulationTick by drawing stats and lookahead line
    def simulationTick(self, screen, m, pointIndex):

        ret = super().simulationTick(screen, m, pointIndex)

        p = self.simulation[pointIndex]

        # Draw lookahead line

        lx, ly = m.inchToPixel(p.lx, p.ly)
        Utility.drawCircle(screen, *m.inchToPixel(p.cx, p.cy), Utility.ORANGE, 2)
        Utility.drawLine(screen, Utility.GREEN, *m.inchToPixel(p.x, p.y), lx, ly, 2)
        Utility.drawCircle(screen, lx, ly, Utility.GREEN, 2)
        
        return ret

    def drawPanel(self, screen):

        super().drawPanel(screen)

         # Draw position and velocity stats
        p = self.simulation[self.pointIndex]
        Utility.drawText(screen, Utility.getFont(40), "Pure Pursuit", Utility.BLACK, 865, 30, 0)
        Utility.drawText(screen, Utility.getFont(20), "xpos: {} inch".format(round(p.x, 2)), Utility.BLACK, 825, 150, 0)
        Utility.drawText(screen, Utility.getFont(20), "ypos: {} inch".format(round(p.y, 2)), Utility.BLACK, 825, 165, 0)
        Utility.drawText(screen, Utility.getFont(20), "theta: {} deg".format(round(p.theta * 180 / math.pi, 2)), Utility.BLACK, 825, 180, 0)
        Utility.drawText(screen, Utility.getFont(20), "xvel: {} inch/sec".format(round(p.xvel, 2)), Utility.BLACK, 955, 150, 0)
        Utility.drawText(screen, Utility.getFont(20), "yvel: {} inch/sec".format(round(p.yvel, 2)), Utility.BLACK, 955, 165, 0)
        Utility.drawText(screen, Utility.getFont(20), "tvel: {} deg/sec".format(round(p.tvel * 180 / math.pi, 2)), Utility.BLACK, 955, 180, 0)

        Utility.drawText(screen, Utility.getFont(20), "Curve: {}".format(round(p.curve, 3)), Utility.BLACK, 825, 195, 0)
        Utility.drawText(screen, Utility.getFont(20), "Error: {}\"".format(round(p.error, 3)), Utility.BLACK, 955, 195, 0)

        self.lookaheadSlider.draw(screen, True)
        self.kpSlider.draw(screen, True)
        self.kdSlider.draw(screen, True)        
    
