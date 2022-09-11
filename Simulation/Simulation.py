from Simulation.Waypoints import Waypoints
from Simulation.AbstractController import AbstractController
from Simulation.PointTurnController import PointTurnController
from Simulation.RobotModel import RobotModel
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Sliders.Slider import Slider

import pygame

"""
A class that stores a complete simulation of the robot following path. This takes in a Waypoints object, a 
RobotMode, and some class that implements AbstractController.

It then runs a full simulation (not in real time), and ultimately generates a list of RobotOutputs, one for each timestep.
"""

class Simulation:

    def __init__(self):
        # Full simulations are stored as lists of RobotModelOutputs, which contain robot position and orientation
        self.recordedSimulation: list[RobotModelOutput] = []
        self.pointTurnController: PointTurnController = PointTurnController()
        self.slider: Slider = Slider() # simuation slider

    # controller is of type AbstrfactController, i.e. like Pure Pursuit
    # when running the simulation, the controller object is created based on the corresponding class passed in
    def runSimulation(self, waypoints: Waypoints, controller: AbstractController, robot: RobotModel):

        self.recordedSimulation.clear() # we're running a new simulation now, so delete the data from the old one


        # Get the initial robot conditions by setting robot position to be at first waypoint, and aimed at second waypoint
        initialPosition: PointRef = waypoints.get(0)
        initialHeading: float = (waypoints.get(1) - waypoints.get(0)).theta()
        output: RobotModelOutput = RobotModelOutput(initialPosition, initialHeading)

        robot: RobotModel = RobotModel(output)

        # Iterate through each subset of waypoints, and point turn in between
        for waypointSubset in waypoints.waypoints:

            controller.initSimulation(waypointSubset)
            isReachPointTurn = False
            isDone = False

            while not isDone:
                if not isReachPointTurn:
                    # Input robot position to controller and obtain wheel velocities
                    robotInput, isReachPointTurn = controller.simulateTick(output)
                else: 
                    robotInput, isDone = controller.simulateTick(output)

                # Take in wheel velocities from controller and simulate the robot model for a tick
                output: RobotModelOutput = robot.simulateTick(robotInput)

                # Store the robot position at each tick
                self.recordedSimulation.append(output)


    # Draw the line the robot takes in the simulation when following the path on the field
    def drawSimulatedPathLine(self, screen: pygame.Surface):
        # TODO
        pass
