from xml.etree.ElementTree import PI
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput

from SingletonState.ReferenceFrame import PointRef
from Sliders.Slider import Slider

from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState

from RobotSpecs import RobotSpecs
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics

from typing import Tuple

from Utility import *

"""
A more sophisticated controller that is theorized to follow lines better.
https://dingyan89.medium.com/three-methods-of-vehicle-lateral-control-pure-pursuit-stanley-and-mpc-db8cc1d32081
"""

class StanleyController(AbstractController):

    def __init__(self):
        super().__init__("Stanley")
        self.closestIndex = 0
        self.crossTrackKP = 3
        self.softeningConstant = 1
        self.tolerance = 0.5
        self.slowdownDistance = 7.5
    

    def defineParameterSliders(self) -> list[ControllerSliderState]:
        #TODO define the tunable parameters of this controller

        #pass
    

        return []


    # init whatever is needed at the start of each path
    def initController(self):
        self.ticks = 0

    def findClosestPoint(self, robot: RobotModelOutput) -> PointRef:
        """
        Finds closest point for use with Stanley Control
        """
        previousPointDistance = 145 # impossible init value given the field
        for i in range(self.closestIndex, len(self.waypoints)):
            pointPosition = self.waypoints[i].fieldRef
            robotPosition = robot.position.fieldRef
            pointDistance = distanceTuples(robotPosition,pointPosition)

            if pointDistance > previousPointDistance:
                # Iterates until the distance increases, then returns
                previousPointDistance = pointDistance
                self.closestIndex = i
            else:
                return self.waypoints[self.closestIndex]
        # If we run out of points, use the last valid one
        return self.waypoints[-1]

    def getCurrentPointHeading(self) -> float:
        """
            Returns the angle of the line at a given waypoint
            Uses the angle leaving the point normally, except for the last point where it uses the angle going into the point
        """
        if (self.closestIndex == len(self.waypoints)-1):
            # at last point, use previous point and current for heading
            dy = self.waypoints[self.closestIndex].fieldRef[1] - self.waypoints[self.closestIndex-1].fieldRef[1]
            dx = self.waypoints[self.closestIndex].fieldRef[0] - self.waypoints[self.closestIndex-1].fieldRef[0]
        else:
            # Normally just uses current and next
            dy = self.waypoints[self.closestIndex+1].fieldRef[1] - self.waypoints[self.closestIndex].fieldRef[1]
            dx = self.waypoints[self.closestIndex+1].fieldRef[0] - self.waypoints[self.closestIndex].fieldRef[0]
        return math.atan2(dy,dx)

        

    def simulateTick(self, output: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool]:
        """
            Performs one timestep of the stanley algorithm
            Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
        """
        # Get the closest waypoint to the robot (Starting from the previously found waypoint)
        closestPoint: PointRef = self.findClosestPoint(output)

        # One of the two controllers in Stanley Control is just a direct heading controller
        headingError = output.heading-self.getCurrentPointHeading()

        # Calculates the angle from the origin to the point
        angleOfClosestPointFromOrigin = math.atan2((closestPoint.fieldRef[1] - output.position.fieldRef[1]), (closestPoint.fieldRef[0] - output.position.fieldRef[0]))
        # Uses that to calculate the angle from the robot heading to the point
        angleBetweenRobotHeadingAndClosestPoint = angleOfClosestPointFromOrigin - output.heading

        # Finds the overall distance from the robot to the waypoint
        distToWaypoint = distanceTuples(output.position.fieldRef, closestPoint.fieldRef)   
        # Finds the perpindicular (cross-track) error from the robot to the waypoint
        crossTrackError = math.sin(angleBetweenRobotHeadingAndClosestPoint)*distToWaypoint

        # Snags the current velocity of the robot
        currentVelocity = (output.leftVelocity + output.rightVelocity)/2

        # Calculates the steering angle (the normal output of a Stanley controller)
        # The second controller is a crosstrack error-based controller, within an atan to convert to a steering angle by adjusting by the current velocity
        steeringAngle = headingError + math.atan2(self.crossTrackKP*crossTrackError,self.softeningConstant+currentVelocity)

        # Use basic trig to calculate the radius resulting from such a steering angle, and
        # converts that to a curvature that we can use to map the steering angle to a differential drive
        curvature = math.sqrt(2 - 2*math.cos(2*steeringAngle)) / self.robotSpecs.trackWidth

        # Slow down the robot linearly as it approaches the final waypoint
        #if (lastPointDist := distanceTuples(output.position.fieldRef, self.waypoints[-1].fieldRef)) < self.slowdownDistance:
        #    velocity = (lastPointDist/self.slowdownDistance)*self.robotSpecs.maximumVelocity
        #else:
        velocity = self.robotSpecs.maximumVelocity / 5

        # Curvature to robot wheel velocities, accounting for the aforementioned slowdown
        leftWheelVelocity = velocity * (2 + curvature*self.robotSpecs.trackWidth)/2
        rightWheelVelocity = velocity * (2 - curvature*self.robotSpecs.trackWidth)/2

        # Tells the system that this Stanley Control loop is done.
        isDone = distToWaypoint < self.tolerance and closestPoint==self.waypoints[-1]

        # Returns the desired wheel velocities to be used in RobotModelInput.
        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), isDone, None

