from Panel.VelocityGUI import VelocityGUI
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from Simulation.RobotModels.ComplexRobotModel import ComplexRobotModel
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotDrawing import RobotDrawing
from SingletonState.FieldTransform import FieldTransform
from RobotSpecs import RobotSpecs
import pygame

"""
Using mouse to control the robot in Odom tab. Uses Velocity GUI for input which feeds into RobotModel
"""

class DriverSimulation:

    def __init__(self, robotSpecs: RobotSpecs):

        # Define starting position
        startPosition: RobotModelOutput = RobotModelOutput(72, 72, 0, 0, 0)

        # The current robot state to be drawn
        self.currentPose: RobotModelOutput = startPosition

        # Define robot model used
        self.robot: AbstractRobotModel = ComplexRobotModel(robotSpecs, startPosition)
        self.robotDrawing: RobotDrawing = RobotDrawing(robotSpecs.trackWidth)

        self.velocityGUI: VelocityGUI = VelocityGUI(robotSpecs, isInteractiveMode = True)

        
    # Simulate a tick of the robot kinematic model given the user input from self.velocityGUI.desired
    # Then, update self.velocityGUI.actual based on the model output
    def update(self):

        # Get the input velocities from VelocityGUI user input
        desiredVelocity = self.velocityGUI.getDesiredVelocity()
    
        # Generate the proper input format for RobotModel
        input: RobotModelInput = RobotModelInput(*desiredVelocity)

        # Simulate with robot model given input for one tick, and get robot model output
        # Also store the current pose from simulation to be drawn later
        self.currentPose = self.robot.simulateTick(input)

        # Update the VelocityGUI with what the actual velocities were
        self.velocityGUI.setActualVelocity(self.currentPose.leftVelocity, self.currentPose.rightVelocity)


    # Draw the robot at the current simulation timestep
    def draw(self, screen: pygame.Surface):

        self.robotDrawing.draw(screen, self.currentPose.position, self.currentPose.heading)
        self.velocityGUI.draw(screen)