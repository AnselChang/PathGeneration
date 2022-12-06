from re import A
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState
from RobotSpecs import RobotSpecs
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics
from Simulation.HUDGraphics.PurePursuitGraphics import PPGraphics


from typing import Tuple

from Utility import *

"""
A simple path following controller. It computes the angular velocity command that moves the robot
from its current position to reach some look-ahead point in front of the robot
"""

class PurePursuitController(AbstractController):

    def __init__(self):
        super().__init__("Pure Pursuit")

    def defineParameterSliders(self) -> list[ControllerSliderState]:
        #TODO define the tunable parameters of this controller
        return []
    
    # init whatever is needed at the start of each path
    def initController(self):
        self.lookaheadIndex = 0
        self.lookaheadDistance = 10
        self.tolerance = 2


    # Indexes through the lost of waypoints to find the one futher along the path closest to lookahead circle.
    def findLookaheadPoint(self, robot: RobotModelOutput) -> PointRef:  
        indexOfLookaheadPoint = self.lookaheadIndex                     # Sets current lookahead point to previous for the 
                                                                        #   start of the next loop.
        lookaheadPointDist = 0                                          # Initial value of the lookahead point distance is 0.

        # Looks at waypoints from the last lookahead point to the second to last point on the list
        for i in range(self.lookaheadIndex, len(self.waypoints)):     
            pointPosition = self.waypoints[i].fieldRef                  # Finds position of the waypoint currently being 
                                                                        #   looked at.
            robotPosition = robot.position.fieldRef                     # Calls current robot position
            pointDistance = distanceTuples(robotPosition,pointPosition) # Finds distance from robot to waypoint

            if pointDistance > lookaheadPointDist and pointDistance < self.lookaheadDistance: 
                # If the distance to the closest waypoint is further than the current lookahead point distance and shorter than the ideal 
                #   lookahead distance, it does the following. Basically, we want to find a waypoint as close to the lookahead distance as 
                #   possible, but will ALWAYS round down if possible.
                indexOfLookaheadPoint = i                                   # Sets the index of the lookahead point to i.
                lookaheadPointDist = pointDistance                          # Sets the distance to the lookahead point distance so we calculate
                self.lookaheadIndex = indexOfLookaheadPoint
                                                                            #   the wheel velocities based on the target waypoint.      
            # If the distance of the new closest waypointis further than the lookahead distance, do the following.
            elif pointDistance > self.lookaheadDistance:        
                indexOfLookaheadPoint = i - 1                           # Sets the lookahead index to be one option before the 
                                                                        #   current index. (Rounds down.)    
                return self.waypoints[indexOfLookaheadPoint] 
        return self.waypoints[indexOfLookaheadPoint]                    # Returns the waypoint of the index chosen above.


    def simulateTick(self, robotOutput: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool, HUDGraphics]:
        # Calls findLookaheadPoint function to find the desired lookahead 
        #   waypoint and saves it to chosenWayppint.
        chosenWaypoint: PointRef = self.findLookaheadPoint(robotOutput)   

        # Finds position of waypoint and robot respectively and separates them into X and Y components
        waypointXPos, waypointYPos = chosenWaypoint.fieldRef    # Waypoint
        robotX, robotY = robotOutput.position.fieldRef          # Robot

        # Calculates the angle in which the robot needs to travel, then finds the distance between this 
        #   and the robot heading.
        angleOfLookaheadVectorFromXAxis = math.atan2((waypointYPos - robotY), (waypointXPos - robotX))
        angleBetweenRobotHeadingAndLookaheadPoint = angleOfLookaheadVectorFromXAxis - robotOutput.heading
        
        # Finds the overall distance from the robot to the waypoint, then the horizontal distance between 
        #   the lookahead vector and the waypoint.
        distToWaypoint = distanceTuples(robotOutput.position.fieldRef, chosenWaypoint.fieldRef)   
        horizontalDistToWaypoint = math.sin(angleBetweenRobotHeadingAndLookaheadPoint)*distToWaypoint
        
        # This represents the case where the robot is either on the lookahead point (last point)
        #   or is already at the right heading and doesn't need to curve.
        if horizontalDistToWaypoint == 0:
            curvature = 0

        # If the robot needs to curve:
        else:
            # Radius of curvature from robot to point.
            radiusOfCurvature = (distToWaypoint)**2/(2*horizontalDistToWaypoint)

            # Curvature from robot to point.
            curvature = 1/radiusOfCurvature

        # Constant used to scale overall velocity up or down for tuning.
        kp = 1/3

        # Slows robot down around curves.
        kd = 1/(2*(1-curvature)) 

        # Calculates desired overall robot velocity.
        error = kp * (distToWaypoint/self.lookaheadDistance) * robotSpecs.maximumVelocity 

        # Curvature to robot wheel velocities:
        leftWheelVelocity = kd * error * (2 + curvature*robotSpecs.trackWidth)/2
        rightWheelVelocity = kd * error * (2 - curvature*robotSpecs.trackWidth)/2

        # Tells the system that the PP loop is done.
        isDone = distToWaypoint < self.tolerance and chosenWaypoint==self.waypoints[-1]
        # Returns the desired wheel velocities to be used in RobotModelInput.
        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), isDone, PPGraphics(robotOutput.position, chosenWaypoint, self.lookaheadDistance)
        