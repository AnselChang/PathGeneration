from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from Simulation.RobotModels.SimpleRobotModel import SimpleRobotModel
from Simulation.RobotModels.ComplexRobotModel import ComplexRobotModel
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from SingletonState.ReferenceFrame import PointRef
from Simulation.ControllerRelated.ControllerManager import ControllerManager
from Simulation.RobotRelated.RobotDrawing import RobotDrawing
from Simulation.SimulationTimestep import SimulationTimestep
from Panel.VelocityGUI import VelocityGUI
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

    def __init__(self, state: SoftwareState, controllers: ControllerManager, path: FullPath, robotSpecs: RobotSpecs):

        self.robotDrawing = RobotDrawing(robotSpecs.trackWidth)

        # Full simulations are stored as lists of RobotModelOutputs, which contain robot position and orientation
        self.recordedSimulation: list[SimulationTimestep] = []

        # simuation slider
        self.slider: Slider = Slider(Utility.SCREEN_SIZE + 150, 190, 115, 0, 1, 1, colors.LIGHTBLUE)

        self.state = state
        self.controllers = controllers
        self.path = path
        self.robotSpecs = robotSpecs

        self.velocityGUI: VelocityGUI = VelocityGUI(robotSpecs, isInteractiveMode = False)


    # Return whether there is a simulation stored in this object
    def exists(self) -> bool:
        return len(self.recordedSimulation) > 0

    # controller is of type AbstrfactController, i.e. like Pure Pursuit
    # when running the simulation, the controller object is created based on the corresponding class passed in
    def runSimulation(self):

        self.simulationIndex = 0
        timestep = 0

        # we're running a new simulation now, so delete the data from the old one
        self.recordedSimulation.clear()

        # Reset and run simulation for each section
        for section in self.path.sections:
            print("a")
            timestep = self.runSimulationSection(section.waypoints, timestep)

        # Now that running simulation is complete, adjust slider bounds
        self.slider.setBounds(0, len(self.recordedSimulation) - 1)
        self.slider.setValue(0)

    # Run robot simulation given one section of the entire path
    def runSimulationSection(self, waypoints: list[PointRef], timestepStart):

        # Set up the controller state machine that alternates between path following and point turn controllers
        controller: AbstractController = self.controllers.getController()
        controller.initSimulation(self.robotSpecs, waypoints)
        
        # Get the initial robot conditions by setting robot position to be at first waypoint, and aimed at second waypoint
        initialPosition: PointRef = waypoints[0]

        initialHeading: float =  Utility.thetaTwoPoints(waypoints[0].fieldRef, waypoints[1].fieldRef)
        robotOutput: RobotModelOutput = RobotModelOutput(*initialPosition.fieldRef, initialHeading, 0, 0)

        # Instantiate robot model with type AbstractRobotModel. This allows easy substitution of
        # different simulation implementations
        print("initial heading: ", initialHeading*180/3.1415, waypoints[0].fieldRef, waypoints[1].fieldRef)
        robot: AbstractRobotModel = ComplexRobotModel(self.robotSpecs, robotOutput)

        # Iterate until robot has reached the destination
        isDone = False
        timestep = timestepStart
        while timestep < timestepStart + 2000 and not isDone: # hard limit of 10000 in case of getting stuck in simulation

            # Input robot position to controller and obtain wheel velocities
            robotInput, isDone, graphics = controller.simulateTick(robotOutput, self.robotSpecs)

            # Take in wheel velocities from controller and simulate the robot model for a tick
            robotOutput: RobotModelOutput = robot.simulateTick(robotInput)

            # Store the robot position at each tick
            self.recordedSimulation.append(SimulationTimestep(timestep * self.robotSpecs.timestep, robotInput, robotOutput, graphics))

            # Increment number of timesteps elapsed
            timestep += 1

        return timestep



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

    # return the current SimulationTimestep based on where the slider indicates we are
    def getCurrent(self) -> SimulationTimestep:
        return self.recordedSimulation[self.slider.getValue()]

    # Called every tick before draw() to perform all update operations needed
    # Increments recorded simulation index if playing simulation
    # Syncs the actual and desired positions of self.velocityGUI
    def update(self):

        # go to next simulation frame if playing
        if self.state.playingSimulation:

            self.moveSlider(1)
            if self.slider.getValue() >= len(self.recordedSimulation) - 1:
                self.state.playingSimulation = False

        if len(self.recordedSimulation) > 0:

            current: SimulationTimestep = self.getCurrent()
            self.velocityGUI.setDesiredVelocity(current.input.leftVelocity, current.input.rightVelocity)
            self.velocityGUI.setActualVelocity(current.output.leftVelocity, current.output.rightVelocity)



    # Draw everything, but only if there is a simulation to draw
    def draw(self, screen: pygame.Surface):

        # If nothing to draw, exit
        if not self.exists():
            return

        self.drawSimulatedPathLine(screen)

        # Draw the robot and HUD graphics at current simulation timestep
        currentTimestep: SimulationTimestep = self.getCurrent()
        self.drawRobot(screen, currentTimestep.output)
        currentTimestep.graphics.draw(screen)
        
            
        
