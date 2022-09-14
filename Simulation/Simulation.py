from Simulation.InterpolatedPoints import InterpolatedPoints
from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from Simulation.RobotModels.SimpleRobotModel import SimpleRobotModel
from Simulation.RobotModels.ComplexRobotModel import ComplexRobotModel
from Simulation.ControllerStateMachine import ControllerStateMachine
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Simulation.ControllerManager import ControllerManager
from SingletonState.FieldTransform import FieldTransform
from Simulation.RobotDrawing import RobotDrawing
from Simulation.Waypoint import Waypoint
from SingletonState.SoftwareState import SoftwareState
from VisibleElements.FullPath import FullPath
from RobotSpecs import RobotSpecs
from Sliders.Slider import Slider
import Utility, colors

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

        # simuation slider
        self.slider: Slider = Slider(Utility.SCREEN_SIZE + 120, 190, 115, 0, 1, 1, colors.LIGHTBLUE)

        self.state = state
        self.controllers = controllers
        self.path = path
        self.robotSpecs = robotSpecs


    # Return whether there is a simulation stored in this object
    def exists(self) -> bool:
        return len(self.recordedSimulation) > 0

    # controller is of type AbstrfactController, i.e. like Pure Pursuit
    # when running the simulation, the controller object is created based on the corresponding class passed in
    def runSimulation(self):

        self.simulationIndex = 0

        # we're running a new simulation now, so delete the data from the old one
        self.recordedSimulation.clear() 

        waypoints: list[list[Waypoint]] = self.path.waypoints.convertToWaypoints()

        # Set up the controller state machine that alternates between path following and point turn controllers
        controllerSM = ControllerStateMachine(self.robotSpecs, waypoints, self.controllers.getController())
        

        # Get the initial robot conditions by setting robot position to be at first waypoint, and aimed at second waypoint
        initialPosition: PointRef = waypoints.get(0)
        initialHeading: float = waypoints[0][0].heading
        output: RobotModelOutput = RobotModelOutput(*initialPosition.fieldRef, initialHeading)

        # Instantiate robot model with type AbstractRobotModel. This allows easy substitution of
        # different simulation implementations
        robot: AbstractRobotModel = ComplexRobotModel(self.robotSpecs, output)

        # Iterate until robot has reached the destination
        timesteps = 0
        isDone = False
        while timesteps < 10000 and not isDone: # hard limit of 10000 in case of getting stuck in simulation

            # Input robot position to controller and obtain wheel velocities
            robotInput, isDone = controllerSM.runController(output)

            # Take in wheel velocities from controller and simulate the robot model for a tick
            output: RobotModelOutput = robot.simulateTick(robotInput)

            # Store the robot position at each tick
            self.recordedSimulation.append(output)

            # Increment number of timesteps elapsed
            timesteps += 1


        # Now that running simulation is complete, adjust slider bounds
        self.slider.setBounds(0, len(self.recordedSimulation) - 1)


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
        self.robotDrawing.draw(screen, robotPose.position, robotPose.heading)

    # move slider by delta
    def moveSlider(self, amount: int):
        index = self.slider.getValue()
        self.slider.setValue(index + amount)

    # Draw everything, but only if there is a simulation to draw
    def draw(self, screen: pygame.Surface):

        # If nothing to draw, exit
        if not self.exists():
            return

        self.drawSimulatedPathLine(screen)
        
        # draw the robot at the current timestep specified by slider
        self.drawRobot(screen, self.recordedSimulation[self.slider.getValue()])
            
        # go to next simulation frame if playing
        if self.state.playingSimulation:
            self.moveSlider(1)
            if self.slider.getValue() >= len(self.recordedSimulation) - 1:
                self.state.playingSimulation = False
                self.slider.setValue(0)
            
        
