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
        self.lookaheadIndex = 0
        self.lookaheadDistance = 6.9 # Editable with slider
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        pass
    
    # init whatever is needed at the start of each path
    def initController(self):
        self.ticks = 0

    # Performs one timestep of the stanley algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
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

        # Not sure if initialization values are necessary
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