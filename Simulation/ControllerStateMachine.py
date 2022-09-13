from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.ControllerClasses.PointTurnController import PointTurnController
from Simulation.Waypoints import Waypoints
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
from RobotSpecs import RobotSpecs

from typing import Tuple

"""
This class is used when running simulations.
Waypoint segments can be seperated by point turns. This class operates as a state machine encapsulating
all the logic switching between the selected controller and the point turn controller.
"""

class ControllerStateMachine:

    def __init__(self, robotSpecs: RobotSpecs, waypoints: Waypoints, pathController: AbstractController):

        self.robotSpecs = robotSpecs
        self.waypoints: Waypoints =  waypoints
        self.pathController: AbstractController = pathController
        self.pointTurnController: PointTurnController = PointTurnController()

        self.segmentIndex = 0 # which segment of waypoints the controller is on

        # Initialize path controller with first path segment
        self.pathController.initSimulation(self.robotSpecs, self.waypoints.waypoints[0])

        self.isPointTurn = False

    
    # Run either the path or point turn controller depending on whether the robot just finished a segment
    # Return the RobotModelInput (the velocities of the wheels), and whether the entire path was finished
    def runController(self, robotOutput: RobotModelOutput) -> Tuple[RobotModelInput, bool]:

        
        if self.isPointTurn:
            # Point turn controller

            robotInput, isDone = self.pointTurnController.simulateTick(robotOutput)

            # If done with point turn, go onto next segment
            # (there is always a next segment in this case, we never end on point turn)
            if isDone:
                self.isPointTurn = False
                

            return (robotInput, False)

        else:
            # Path following controller

            robotInput, isDone = self.pathController.simulateTick(robotOutput)

            # If at last waypoint segment, then return true for exiting. Otherwise, go on to point turn
            if isDone:

                if self.segmentIndex == len(self.waypoints.waypoints) - 1: # last waypoint segment
                    return (robotInput, True)

                else: # not last, go to point turn
                    self.isPointTurn = True

                    # Get ready for next path segment once point turn ends
                    self.segmentIndex += 1
                    nextSubset = self.waypoints.waypoints[self.segmentIndex]
                    self.pathController.initSimulation(self.robotSpecs, nextSubset)

                    # Set heading for upcoming point turn
                    heading = (nextSubset[1] - nextSubset[0]).theta()
                    self.pointTurnController.initSimulation(self.robotSpecs, heading)

                    return (robotInput, False)