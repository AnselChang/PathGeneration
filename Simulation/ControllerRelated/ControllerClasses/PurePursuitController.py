from re import A
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation import Waypoint
from Sliders.Slider import Slider

from typing import Tuple

from Utility import *

"""
A simple path following controller. It computes the angular velocity command that moves the robot
from its current position to reach some look-ahead point in front of the robot
"""

class PurePursuitController(AbstractController):

    def __init__(self):
        super().__init__("Pure Pursuit")
        self.lookaheadIndex = 0
        self.lookaheadDistance = 4.20
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        """
        lookAheadDistance
        """
        pass

    # init whatever is needed at the start of each path
    def initController(self):
        pass
    
        """
        given current x, y, and theta;
        given desired x, y, and theta of each waypoint
        given list of waypoints

        find closest waypoint; might be given via order of stored data
        for (i>0, i<=maxi -1: i+=1):
            read current pos info
            read desired waypoint info
            find lookahead distance (l=sqrt(xerror^2 + yerror^2))

        GIVEN: 
            V = Max Speed
            C = curvature
            T = Track Width

        if (V >= maxSpeed - acceleration):
            V += acceleration

        L = V*(2 + CT)/2
        R = V*(2 - CT)/2
        """

    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        """
        find lookahead pt
        point to line distance from robot's heading vector
         -> x = distanceTwoPoints(lookahead pt, pointOnLineClosestToPoint([robotHeadingVector], lookahead pt position))
        radius of curvature from robot to point
         -> r = (distance to lookahead point)^2/2x
         -> C = 1/r     # Curvature
        Curvature to robot wheel velocities:
         -> L = robotSpecs.maxVelocity * (2 + C*robotSpecs.trackWidth)/2
         -> R = robotSpecs.maxVelocity * (2 - C*robotSpecs.trackWidth)/2
        return RobotModelInput(L,R)
        """
        pass
        

    """
    Step 1: calc distance from point to robot
    Step 2: if that is closest to lookahead distance, save it
    Step 3: if farther than lookahead, break out of loop
    """
    def findLookaheadPoint(self, robot: RobotModelOutput) -> Waypoint:

        # Note sure if initialization values are necessary
        indexOfLookaheadPoint = self.lookaheadIndex
        lookaheadPointDist = 0      # Index Of Point Closest To Lookahead

        for i in range(self.lookaheadIndex, self.waypoints.len()-1):
            pointPosition = self.waypoints[i].position.fieldRef
            robotPosition = robot.position.fieldRef
            pointDistance = distanceTwoPoints(robotPosition,pointPosition)

            if pointDistance > lookaheadPointDist and pointDistance < self.lookaheadDistance:
                indexOfLookaheadPoint = i
                lookaheadPointDist = pointDistance

            elif pointDistance > self.lookaheadDistance:
                self.lookaheadIndex = indexOfLookaheadPoint
                return self.waypoints[indexOfLookaheadPoint]
        # If we run out of points, use the last valid one
        return self.waypoints[indexOfLookaheadPoint]