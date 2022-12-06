from re import A
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState
from RobotSpecs import RobotSpecs
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics
from Simulation.HUDGraphics.AnselGraphics import AnselGraphics


from typing import Tuple

from Utility import *

"""
A simple path following controller. It computes the angular velocity command that moves the robot
from its current position to reach some look-ahead point in front of the robot
"""

class AnselPPController(AbstractController):

    def __init__(self):
        super().__init__("Ansel")
        

    def defineParameterSliders(self) -> list[ControllerSliderState]:
        #TODO define the tunable parameters of this controller

        return [
            ControllerSliderState("Target Delta", 10, 0, 30, 1),
            ControllerSliderState("Base Speed %", 0.2, 0.01, 1, 0.01),
            ControllerSliderState("Heading KP", 7, 0.1, 50, 0.1),
            ControllerSliderState("Tolerance (in.)", 5, 3, 10, 0.1)
        ]

    # Indexes through the lost of waypoints to find the one futher along the path closest to lookahead circle.
    def findClosestWaypointIndex(self, robot: RobotModelOutput) -> int:

        closestDistance = distanceTuples(self.waypoints[self.closestIndex].fieldRef, robot.position.fieldRef)

        for i in range(self.closestIndex, min(self.closestIndex + 10, len(self.waypoints))):     
            pointPosition = self.waypoints[i].fieldRef
            robotPosition = robot.position.fieldRef
            distanceToWaypoint = distanceTuples(robotPosition,pointPosition)
            if distanceToWaypoint < closestDistance:
                self.closestIndex = i
                closestDistance = distanceToWaypoint

        return self.closestIndex



    # init whatever is needed at the start of each path
    def initController(self):
        self.closestIndex = 0
        self.TARGET_INDEX_DELTA = self.getSliderValue("Target Delta")
        self.BASE_SPEED_PCT = self.getSliderValue("Base Speed %")
        self.HEADING_KP = self.getSliderValue("Heading KP")
        self.TOLERANCE = self.getSliderValue("Tolerance (in.)")

    def simulateTick(self, robotOutput: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool, HUDGraphics]:

        closestIndex = self.findClosestWaypointIndex(robotOutput)
        index = min(closestIndex + self.TARGET_INDEX_DELTA, len(self.waypoints) - 1)
        targetPosition: PointRef = self.waypoints[index]

        # Calculates the angle in which the robot needs to travel, then finds the distance between this 
        #   and the robot heading.
        headingToTarget = thetaTwoPoints(robotOutput.position.fieldRef, targetPosition.fieldRef)
        headingError = deltaInHeading(headingToTarget, robotOutput.heading)
        
        baseSpeed = robotSpecs.maximumVelocity * self.BASE_SPEED_PCT
        leftWheelVelocity = baseSpeed + self.HEADING_KP * headingError
        rightWheelVelocity = baseSpeed - self.HEADING_KP * headingError


        # Tells the system that the PP loop is done.
        distance = distanceTuples(robotOutput.position.fieldRef, self.waypoints[-1].fieldRef)
        isDone = distance < self.TOLERANCE and index == len(self.waypoints) - 1
        # Returns the desired wheel velocities to be used in RobotModelInput.
        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), isDone, AnselGraphics(self.waypoints[closestIndex], targetPosition)
        