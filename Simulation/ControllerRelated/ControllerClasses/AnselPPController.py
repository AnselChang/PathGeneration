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

class AnselPPController(AbstractController):

    def __init__(self):
        super().__init__("Ansel")
        self.lookaheadIndex = 0
        self.lookaheadDistance = 10
        self.tolerance = 2

    def defineParameterSliders(self) -> list[ControllerSliderState]:
        #TODO define the tunable parameters of this controller

        return [
            ControllerSliderState("Param 1", 0, 10, 1),
            ControllerSliderState("Param 2", -5, 5, 0.1),
            ControllerSliderState("Param 3", 10, 20, 0.1)
        ]


    # Indexes through the lost of waypoints to find the one futher along the path closest to lookahead circle.
    def findLookaheadPoint(self, robot: RobotModelOutput) -> PointRef:  

        for i in range(self.lookaheadIndex, min(self.lookaheadIndex + 10, len(self.waypoints))):     
            pointPosition = self.waypoints[i].fieldRef                  # Finds position of the waypoint currently being 
                                                                        #   looked at.
            robotPosition = robot.position.fieldRef                     # Calls current robot position
            pointDistance = distanceTuples(robotPosition,pointPosition) # Finds distance from robot to waypoint

            if pointDistance > self.lookaheadDistance:
                break

        self.lookaheadIndex = i
        return self.waypoints[i]                    # Returns the waypoint of the index chosen above.



    # init whatever is needed at the start of each path
    def initController(self):
        pass

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
        
        baseSpeed = robotSpecs.maximumVelocity * 0.3
        kp = 3
        leftWheelVelocity = baseSpeed + kp * angleBetweenRobotHeadingAndLookaheadPoint
        rightWheelVelocity = baseSpeed - kp * angleBetweenRobotHeadingAndLookaheadPoint


        # Tells the system that the PP loop is done.
        distance = distanceTuples((robotX, robotY), self.waypoints[-1].fieldRef)
        isDone = distance < self.tolerance and chosenWaypoint==self.waypoints[-1]
        # Returns the desired wheel velocities to be used in RobotModelInput.
        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), isDone, PPGraphics(robotOutput.position, chosenWaypoint, self.lookaheadDistance)
        