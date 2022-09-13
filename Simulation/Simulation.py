from Simulation.Waypoints import Waypoints
from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.ControllerClasses.PointTurnController import PointTurnController
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from Simulation.RobotModels.SimpleRobotModel import SimpleRobotModel
from Simulation.RobotModels.ComplexRobotModel import ComplexRobotModel
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Simulation.ControllerManager import ControllerManager
from SingletonState.FieldTransform import FieldTransform
from Simulation.RobotDrawing import RobotDrawing
from SingletonState.SoftwareState import SoftwareState
from VisibleElements.FullPath import FullPath
from RobotSpecs import RobotSpecs
from Sliders.Slider import Slider

import pygame

"""
A class that stores a complete simulation of the robot following path. This takes in a Waypoints object, a 
RobotMode, and some class that implements AbstractController.

It then runs a full simulation (not in real time), and ultimately generates a list of RobotOutputs, one for each timestep.
"""

class Simulation:

    def __init__(self, state: SoftwareState, transform: FieldTransform, controllers: ControllerManager, path: FullPath, robotSpecs: RobotSpecs):

        # Initialize RobotModelOutput class's transform reference
        RobotModelOutput.transform = transform

        self.robotDrawing = RobotDrawing(transform, robotSpecs.trackWidth)

        # Full simulations are stored as lists of RobotModelOutputs, which contain robot position and orientation
        self.recordedSimulation: list[RobotModelOutput] = []
        self.pointTurnController: PointTurnController = PointTurnController()

        # TODO uncomment this when slider is fully implemented
        #self.slider: Slider = Slider() # simuation slider

        self.state = state
        self.controllers = controllers
        self.path = path
        self.robotSpecs = robotSpecs

        self.simulationIndex = 0 # temporary, slider is replacement


    # controller is of type AbstrfactController, i.e. like Pure Pursuit
    # when running the simulation, the controller object is created based on the corresponding class passed in
    def runSimulation(self):

        self.simulationIndex = 0

        waypoints: Waypoints = self.path.waypoints

        # Get the controller algorithm we're running for this simulation
        controller: AbstractController = self.controllers.getController()
        
        # we're running a new simulation now, so delete the data from the old one
        self.recordedSimulation.clear() 

        # Get the initial robot conditions by setting robot position to be at first waypoint, and aimed at second waypoint
        initialPosition: PointRef = waypoints.get(0)
        initialHeading: float = (waypoints.get(1) - waypoints.get(0)).theta()
        output: RobotModelOutput = RobotModelOutput(*initialPosition.fieldRef, initialHeading)

        # Instantiate robot model with type AbstractRobotModel. This allows easy substitution of
        # different simulation implementations
        robot: AbstractRobotModel = SimpleRobotModel(self.robotSpecs, output)

        # Iterate through each subset of waypoints, and point turn in between
        i = 0
        for waypointSubset in waypoints.waypoints:

            controller.initSimulation(self.robotSpecs, waypointSubset)
            isReachPointTurn = False
            isDone = False

            while not isDone:

                if not isReachPointTurn: # follow the path

                    # Input robot position to controller and obtain wheel velocities
                    robotInput, isReachPointTurn = controller.simulateTick(output)

                    # If this condition is true, we've reached the end of the current path segment
                    # and are either about to point turn into the next segment or finish the simulation
                    if isReachPointTurn:
                        # If reached the last PathPoint, do not point turn and end simulation
                        if i >= len(waypoints.waypoints) - 1:
                            break 
                        else:
                            # Otherwise, prepare the point turn by initializing turn angle
                            heading: float = (waypoints.waypoints[i+1][1] - waypoints.waypoints[i+1][0]).theta()
                            self.pointTurnController.initSimulation(self.robotSpecs, heading)

                else: # point turn
                    robotInput, isDone = self.pointTurnController.simulateTick(output)

                # Take in wheel velocities from controller and simulate the robot model for a tick
                output: RobotModelOutput = robot.simulateTick(robotInput)

                # Store the robot position at each tick
                self.recordedSimulation.append(output)

                i += 1

        # Now that running simulation is complete, adjust slider bounds
        #self.slider.setBounds(0, len(self.recordedSimulation) - 1)


    # Draw the line the robot takes in the simulation when following the path on the field
    def drawSimulatedPathLine(self, screen: pygame.Surface):

        # If less than two timesteps, no line to draw
        if len(self.recordedSimulation) < 2:
            return

        # TODO draw a line connecting the robot's position at every single timestep. Have each segment change
        # color a little bit (so line looks like rainbow color) to get idea of how fast robot is moving
        # use Graphics.py draw methods
        pass

    # Draw the robot at the specified position and pose
    # TODO: actually point the direction of the robot given heading
    def drawRobot(self, screen: pygame.Surface, robotPose: RobotModelOutput):
        self.robotDrawing.draw(screen, robotPose.position)

    # Draw everything, but only if there is a simulation to draw
    def draw(self, screen: pygame.Surface):

        # If nothing to draw, exit
        if len(self.recordedSimulation) < 1:
            return

        self.drawSimulatedPathLine(screen)
        
        # draw the robot at the current timestep specified by slider
        #self.drawRobot(self.recordedSimulation[self.slider.getValue()])
        # temporary code before slider comes
        if len(self.recordedSimulation) > 0 and self.state.playingSimulation:
            
            self.drawRobot(screen, self.recordedSimulation[self.simulationIndex])
            self.simulationIndex += 1

            if self.simulationIndex >= len(self.recordedSimulation):
                self.state.playingSimulation = False
                self.simulationIndex = 0
            
        
