from Simulation.RobotModelOutput import RobotModelOutput
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from RobotSpecs import RobotSpecs
import math
import numpy as np

"""
Accurate kinematic model of robot that adheres to physics. We simulate the robot's position and velocity over time, given
left and right wheel velocities at each tick. We account for drift in both mesial and lateral directions specified by robotSpec
"""

class ComplexRobotModel(AbstractRobotModel):

    def __init__(self, robotSpecs: RobotSpecs, start: RobotModelOutput):

        # initialize robot sepcs and start pose in superclass
        super().__init__(robotSpecs, start)

        self.deltaX, self.deltaY = 0,0

    # We account for slipping from self.robotSpecs friction coefficients
    def simulateTick(self, input: RobotModelInput) -> RobotModelOutput:

        print("Starting position: ", self.xPosition, self.yPosition, self.heading)

        radius: float = 0
        omega: float = 0

        if(input.leftVelocity == input.rightVelocity):
            # Special case where we have no rotation
            # radius = "INFINITE"
            # omega = 0
            velocity = input.leftVelocity # left and right velocities are the same
            distance = velocity * self.robotSpecs.timestep
            return RobotModelOutput(self.xPosition+distance*math.cos(self.heading), self.yPosition+distance*math.sin(self.heading), self.heading)
            
        else:   
            # Normal case where we have rotation

            # Calculate the radius of the circle we are turning on
            radius = (self.robotSpecs.trackWidth)*((input.leftVelocity+input.rightVelocity)/
            (input.rightVelocity-input.leftVelocity))
            
            # Calculate the angular velocity of the robot about the center of the circle
            omega = (input.rightVelocity-input.leftVelocity)/self.robotSpecs.trackWidth
            # print("omega: ", omega)
        
            # Calculate the center of the circle we are turning on (Instantaneous center of curvature)
            icc = np.array([self.xPosition - radius*math.sin(self.heading),
            self.yPosition + radius*math.cos(self.heading)])
            # print(icc)

            # Calculate the new position of the robot after the timestep

            #TransformMat:
            #[cos(omega*t) -sin(omega*t) 0]
            #[sin(omega*t) cos(omega*t)  0]
            #[0            0             1]
            transformMat = np.array([math.cos(omega*self.robotSpecs.timestep),
             -math.sin(omega*self.robotSpecs.timestep),0, math.sin(omega*self.robotSpecs.timestep),
              math.cos(omega*self.robotSpecs.timestep),0,0,0,1]).reshape(3,3)
            # print(transformMat)

            #[x-ICCx, y-ICCy, heading]
            matrixB = np.array([self.xPosition-icc[0],self.yPosition-icc[1],self.heading]).reshape(3,1)

            #[ICCx, ICCy, omega*t]
            matrixC = np.array([icc[0],icc[1],omega*self.robotSpecs.timestep]).reshape(3,1)

            # The output is the new position of the robot after the timestep
            outputMatrix = np.matmul(transformMat,matrixB) + matrixC
            # print("Output: ",outputMatrix)

            # Set the new position of the robot
            self.xPosition = outputMatrix[0][0]
            self.yPosition = outputMatrix[1][0]
            self.heading = outputMatrix[2][0]

            return RobotModelOutput(self.xPosition, self.yPosition, self.heading)

        

