from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotModels.AbstractRobotModel import AbstractRobotModel
from RobotSpecs import RobotSpecs
import math, Utility
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
        self.xVelocity, self.yVelocity = 0,0
        self.angularVelocity = 0
        self.leftVelocity, self.rightVelocity = 0,0

    # We account for slipping from self.robotSpecs friction coefficients
    # SHOULD NOT MODIFY input
    def simulateTick(self, input: RobotModelInput) -> RobotModelOutput:

        # Clamp velocities within realistic range
        clampedLeftVelocity = Utility.clamp(input.leftVelocity, -self.robotSpecs.maximumVelocity, self.robotSpecs.maximumVelocity)
        clampedRightVelocity = Utility.clamp(input.rightVelocity, -self.robotSpecs.maximumVelocity, self.robotSpecs.maximumVelocity)

        # Limit the acceleration of the robot to robotSpecs.maximumAcceleration
        clampedLeftVelocity = Utility.clamp(clampedLeftVelocity, self.leftVelocity - 
        self.robotSpecs.maximumAcceleration, self.leftVelocity + self.robotSpecs.maximumAcceleration)
        clampedRightVelocity = Utility.clamp(clampedRightVelocity, self.rightVelocity - 
        self.robotSpecs.maximumAcceleration, self.rightVelocity + self.robotSpecs.maximumAcceleration)

        # Store the left and right velocities for the next tick
        self.leftVelocity = clampedLeftVelocity
        self.rightVelocity = clampedRightVelocity

        # Save the start locations to calculate the change in position later
        prevX, prevY = self.xPosition, self.yPosition
        
        if(clampedLeftVelocity == clampedRightVelocity):
            # Special case where we have no rotation
            # radius = "INFINITE"
            omega = 0
            velocity = clampedLeftVelocity # left and right velocities are the same
            distance = velocity * self.robotSpecs.timestep

            self.xPosition = self.xPosition + distance * math.cos(self.heading)
            self.yPosition = self.yPosition + distance * math.sin(self.heading)
            self.heading = self.heading # no change in heading
            
        else:   
            # Normal case where we have rotation

            # Calculate the radius of the circle we are turning on
            radius = (self.robotSpecs.trackWidth)*((clampedLeftVelocity+clampedRightVelocity)/
            (clampedLeftVelocity-clampedRightVelocity))
            
            # Calculate the angular velocity of the robot about the center of the circle
            omega = (clampedLeftVelocity-clampedRightVelocity)/self.robotSpecs.trackWidth
        
            # Calculate the center of the circle we are turning on (Instantaneous center of curvature)
            icc = np.array([self.xPosition - radius*math.sin(self.heading),
            self.yPosition + radius*math.cos(self.heading)])

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

        # Unit vector in the direction of the robot's heading
        robotHeadingVector = np.array([math.cos(self.heading), math.sin(self.heading)])

        # Vector for the robot's velocity from the last timestep
        robotVelocityVector = np.array([self.xVelocity, self.yVelocity])

        # Calculate the lateral velocity of the robot
        lateralVelocity = np.cross(robotHeadingVector, robotVelocityVector)
        
        #Find the x and y components of the lateral velocity
        lateralX = lateralVelocity * math.cos(self.heading + math.pi/2)
        lateralY = lateralVelocity * math.sin(self.heading + math.pi/2)
        
        # Add the slip multiplied by friction coefficient
        self.xPosition += lateralX * (1-self.robotSpecs.lateralFriction)
        self.yPosition += lateralY * (1-self.robotSpecs.lateralFriction)

        # Calculate the velocity of the robot after the timestep
        self.xVelocity = self.xPosition - prevX
        self.yVelocity = self.yPosition - prevY
        self.angularVelocity = omega

        # TEMPORARY: wraparound
        self.xPosition = Utility.wrap(self.xPosition, 144)
        self.yPosition = Utility.wrap(self.yPosition, 144)

        return RobotModelOutput(self.xPosition, self.yPosition, self.heading, self.leftVelocity, self.rightVelocity, self.xVelocity, self.yVelocity, self.angularVelocity)

        

