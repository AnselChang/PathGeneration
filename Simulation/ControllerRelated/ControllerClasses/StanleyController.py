from xml.etree.ElementTree import PI
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation import Waypoint
from Sliders.Slider import Slider

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
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        pass
    
    # init whatever is needed at the start of each path
    def initController(self):
        self.ticks = 0
       
    """
    Finds closest point for use with Stanley Control
    """
    def findClosestPoint(self, robot: RobotModelOutput) -> Waypoint:

        previousPointDistance = 145 # impossible init value given the field
        for i in range(self.closestIndex, self.waypoints.len()-1):
            pointPosition = self.waypoints[i].position.fieldRef
            robotPosition = robot.position.fieldRef
            pointDistance = distanceTwoPoints(robotPosition,pointPosition)

            if pointDistance > previousPointDistance:
                previousPointDistance = pointDistance
                self.closestIndex = i
            else:
                return self.waypoints[self.closestIndex]
        # If we run out of points, use the last valid one
        return self.waypoints[len(self.waypoints0)-1]

    def getCurrentPointHeading(self) -> float:
        if (self.closestIndex == len(self.waypoints)-1):
            # at last point, use previous point and current for heading
            dy = self.waypoints[self.closestIndex].position.fieldRef[1] - self.waypoints[self.closestIndex-1].position.fieldRef[1]
            dx = self.waypoints[self.closestIndex].position.fieldRef[0] - self.waypoints[self.closestIndex-1].position.fieldRef[0]
        else:
            dy = self.waypoints[self.closestIndex+1].position.fieldRef[1] - self.waypoints[self.closestIndex].position.fieldRef[1]
            dx = self.waypoints[self.closestIndex+1].position.fieldRef[0] - self.waypoints[self.closestIndex].position.fieldRef[0]
        return math.atan2(dy,dx)

        
    # Performs one timestep of the stanley algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        """
        find closest point
        calculate the heading of the line at that point
        find perpindicular distance from robot position to line
        correct for the two types of heading error
        """
        closestPoint: Waypoint = self.findClosestPoint(output)
        headingError = output.heading-self.getCurrentPointHeading()

        angleOfClosestPointFromXAxis = math.atan2((closestPoint.position.fieldRef[1] - output.position.fieldRef[1]), (closestPoint.position.fieldRef[1] - output.position.fieldRef[0]))
        angleBetweenRobotHeadingAndClosestPoint = angleOfClosestPointFromXAxis - output.heading

        # Finds the overall distance from the robot to the waypoint, then the perpindicular distance between 
        #   the lookahead vector and the waypoint.
        distToWaypoint = distanceTuples(output.position.fieldRef, closestPoint.fieldRef)   

        crossTrackError = math.sin(angleBetweenRobotHeadingAndClosestPoint)*distToWaypoint

        currentVelocity = (output.leftVelocity + output.rightVelocity)/2

        steeringAngle = headingError + math.atan2(self.crossTrackKP*crossTrackError,self.softeningConstant+currentVelocity)

        radius = self.robotSpecs.trackWidth / math.sqrt(2 - 2*math.cos(2*steeringAngle))
        curvature = 1 / radius

        if (lastPointDist := distanceTuples(output.position.fieldRef, self.waypoints[len(self.waypoints)-1])) < self.slowdownDistance:
            velocity = (lastPointDist/self.slowdownDistance)*self.robotSpecs.maximumVelocity
        else
            velocity = self.robotSpecs.maximumVelocity

        # Curvature to robot wheel velocities:
        leftWheelVelocity = velocity * (2 + curvature*self.robotSpecs.trackWidth)/2
        rightWheelVelocity = velocity * (2 - curvature*self.robotSpecs.trackWidth)/2

        # Tells the system that the PP loop is done.
        isDone = distToWaypoint < self.tolerance and closestPoint==self.waypoints[len(self.waypoints)-1]

        # Returns the desired wheel velocities to be used in RobotModelInput.
        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), isDone, PPGraphics(robotOutput.position, chosenWaypoint, self.lookaheadDistance)

