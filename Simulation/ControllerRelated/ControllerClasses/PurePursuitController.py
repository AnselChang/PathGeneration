from re import A
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation import Waypoint
from Sliders.Slider import Slider
from RobotSpecs import RobotSpecs

from typing import Tuple

from Utility import *

"""
A simple path following controller. It computes the angular velocity command that moves the robot
from its current position to reach some look-ahead point in front of the robot
"""

class PurePursuitController(AbstractController):

    def __init__(self):
        super().__init__("Pure Pursuit")
        self.lookaheadIndex = 0
        self.lookaheadDistance = 15
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        """
        lookAheadDistance
        """
        pass

    
    # Finding the lookahead point and information
        # Step 1: calc distance from point to robot
        # Step 2: if that is closest to lookahead distance, save it
        # Step 3: if farther than lookahead, break out of loop
    
    def findLookaheadPoint(self, robot: RobotModelOutput) -> Waypoint:
        if(self.lookaheadIndex < len(self.waypoints)-1):
            # Iterate    
            self.lookaheadIndex+=1
        return self.waypoints[self.lookaheadIndex]
        # Not sure if initialization values are necessary
        indexOfLookaheadPoint = self.lookaheadIndex # Sets current lookahead point to previous for the start of the next loop
        lookaheadPointDist = 0 # Index Of Point Closest To Lookahead 

        for i in range(self.lookaheadIndex, len(self.waypoints)-1):
            pointPosition = self.waypoints[i].position.fieldRef             # Finds position of the closest waypoint to the lookahead distance
            robotPosition = robot.position.fieldRef                         # Finds current robot position
            pointDistance = distanceTuples(robotPosition,pointPosition)  # Finds distance from robot to waypoint

            if pointDistance > lookaheadPointDist and pointDistance < self.lookaheadDistance: 
                # If the distance to the closest waypoint is further than the current lookahead point distance and shorter than the ideal 
                #   lookahead distance, it does the following. Basically, we want to find a waypoint as close to the lookahead distance as 
                #   possible, but will ALWAYS round down if possible.
                indexOfLookaheadPoint = i                                   # Sets the index of the lookahead point to i.
                lookaheadPointDist = pointDistance                          # Sets the distance to the lookahead point distance so we calculate
                self.lookaheadIndex = indexOfLookaheadPoint
                i+=1
                                                                            #   the wheel velocities based on the target waypoint.

            elif pointDistance > self.lookaheadDistance:        
                # If the distance of the new closest waypointis further than the lookahead distance, do the following.
                indexOfLookaheadPoint = self.lookaheadIndex                # Sets the lookahead index to be the index of the current lookahead 

                                                                            #   point so it doesn't change for this loop.
            return self.waypoints[indexOfLookaheadPoint]                # Returns the waypoint of the index of the lookahead point above.

        # If we run out of points, use the last valid one
        #return self.waypoints[indexOfLookaheadPoint]

    """def findLookaheadPoint2(self, robot: RobotModelOutput) -> Waypoint:

        # Not sure if initialization values are necessary
        innerLookaheadPointIndex = self.lookaheadIndex # Sets current lookahead point to previous for the start of the next loop
        prevLookaheadPointDist = 0                      # Index Of Point Closest To Lookahead 

        for i in range(self.lookaheadIndex, len(self.waypoints)-1):
            pointPosition = self.waypoints[i].position.fieldRef             # Finds position of the closest waypoint to the lookahead distance
            nextPointPosition = self.waypoints[i+1].position.fieldref
            lastPointPosition = self.waypoints(i-1).position.fieldref
            robotPosition = robot.position.fieldRef                         # Finds current robot position
            pointDistance = distanceTuples(robotPosition,pointPosition)  # Finds distance from robot to waypoint
            nextPointDistance = distanceTuples(robotPosition,nextPointPosition)
            lastPointDistance = distanceTuples(robotPosition,lastPointPosition)

            if (pointDistance > prevLookaheadPointDist and pointDistance < self.lookaheadDistance) and nextPointDistance > self.lookaheadDistance: 
                # If the distance to the closest waypoint is further than the current lookahead point disatnce and shorter than the ideal 
                #   lookahead distance, it does the following. Basically, we want to find a waypoint as close to the lookahead distance as 
                #   possible, but will ALWAYS round down if possible.
                innerLookaheadPointIndex = i
                outerLookaheadPointIndex = i + 1                                #
                prevLookaheadPointDist = nextPointDistance                          # Sets the distance to the lookahead point distance so we calculate
                                                                            #   the wheel velocities based on the target waypoint.

            elif pointDistance > self.lookaheadDistance:        
                # If the distance of the new closest waypointis further than the lookahead distance, do the following.
                self.lookaheadIndex = innerLookaheadPointIndex                 # Sets the lookahead index to be the index of the current lookahead 
                                                                            #   point so it doesn't change for this loop.
            return 1          # Returns the waypoint of the index of the lookahead point above.
            """
        # If we run out of points, use the last valid one
        #return self.waypoints[indexOfLookaheadPoint] """ Why is is gray, did I break it? It says the code is unreachable T.T"""

    # init whatever is needed at the start of each path
    def initController(self):
        pass
    

    def simulateTick(self, robotOutput: RobotModelOutput, robotSpecs: RobotSpecs) -> Tuple[RobotModelInput, bool]:

        chosenWaypoint: Waypoint = self.findLookaheadPoint(robotOutput)

        #point to line distance from robot's heading vector
        waypointXPos, waypointYPos = chosenWaypoint.position.fieldRef
        robotX, robotY = robotOutput.position.fieldRef
        angleOfLookaheadVectorFromXAxis = math.atan2((waypointYPos - robotY), (waypointXPos - robotX))
        angleBetweenRobotHeadingAndLookaheadPoint = angleOfLookaheadVectorFromXAxis - robotOutput.heading
        
        distToWaypoint = distanceTuples(robotOutput.position.fieldRef, chosenWaypoint.position.fieldRef)   #temporary arbitrary value so the code stops getting mad. Code is commented above
        horizontalDistToWaypoint = math.sin(angleBetweenRobotHeadingAndLookaheadPoint)*distToWaypoint
        
        if horizontalDistToWaypoint == 0:
            # This represents the case where the robot is either on the lookahead point (last point)
            # Or is already at the right heading and doesn't need to curve
            curvature = 0
        else:
            # Radius of curvature from robot to point
            radiusOfCurvature = (distToWaypoint)**2/(2*horizontalDistToWaypoint)

            # Curvature from robot to point
            curvature = 1/radiusOfCurvature

        # Curvature to robot wheel velocities:
        leftWheelVelocity = robotSpecs.maximumVelocity * (2 + curvature*robotSpecs.trackWidth)/2
        rightWheelVelocity = robotSpecs.maximumVelocity * (2 - curvature*robotSpecs.trackWidth)/2

        print(f"x: {waypointXPos} y: {waypointYPos} distFromBotToPoint: {distToWaypoint}")

        return RobotModelInput(leftWheelVelocity,rightWheelVelocity), False
        


        #distToWaypoint = distanceTwoPoints(self.waypoints[indexOfLookaheadPoint], pointOnLineClosestToPoint(self.robotOutput.robotHeading, self.waypoint(indexOfLookaheadPoint)))
        #radiusOfCurvature = (distance to lookahead point)^2/(2*distToWaypoint)
        #curvature = 1/radiusOfCurvature

        #leftVelocity = robotSpecs.maxVelocity * (2 + curvature*robotSpecs.trackWidth)/2
        #rightVelocity = robotSpecs.maxVelocity * (2 - curvature*robotSpecs.trackWidth)/2

        #return RobotModelInput(leftVelocity, rightVelocity)

        """
        find lookahead pt
        point to line distance from robot's heading vector
         -> distToWaypoint = distanceTwoPoints(chosenWaypoint, pointOnLineClosestToPoint([robotHeadingVector], chosenWaypoint.position.fieldRef))
        radius of curvature from robot to point
         -> r = (distance to lookahead point)^2/2x
         -> C = 1/r     # Curvature
        Curvature to robot wheel velocities:
         -> L = robotSpecs.maxVelocity * (2 + C*robotSpecs.trackWidth)/2
         -> R = robotSpecs.maxVelocity * (2 - C*robotSpecs.trackWidth)/2
        return RobotModelInput(L,R)
        """
    
    
        """
        given current x, y, and theta;
        given desired x, y, and theta of each waypoint
        given list of waypoints 

        find closest waypoint; might be given via order of stored data
        for (i>0, i<=maxi -1: i+=1):
            read current pos info
            read desired waypoint info
            find lookahead distance (l=sqrt(xerror^2 + yerror^2))

        GIVEN: 
            V = Max Speed
            C = curvature
            T = Track Width

        if (V >= maxSpeed - acceleration):
            V += acceleration

        L = V*(2 + CT)/2
        R = V*(2 - CT)/2
        """

        """

        waypointXPos, waypointYPos = waypointChosen.fieldRef


        angleOfLookaheadVectorFromXAxis = atan2((waypointYPos - robotOutput.yPosition.fieldRef), (waypointXPos - robotOutput.xPosition.fieldRef))
        angleBetweenRobotHeadingAndLookaheadPoint = angleOfLookaheadVectorFromXAxis - robotOutput.heading.fieldRef
        horizontalDistToWaypoint = cos(angleBetweenRobotHeadingAndLookaheadPoint)*distTwoPoints(robot.position.fieldRef, waypointChosen)


        verticalDistToWaypoint = sin(angleBetweenRobotHeadingAndLookaheadPoint)*distTwoPoints(robot.position.fieldRef, waypointChosen)
        """

        