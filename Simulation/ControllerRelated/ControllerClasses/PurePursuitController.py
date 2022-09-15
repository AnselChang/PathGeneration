from re import A
from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Sliders.Slider import Slider

from typing import Tuple

"""
A simple path following controller. It computes the angular velocity command that moves the robot
from its current position to reach some look-ahead point in front of the robot
"""

class PurePursuitController(AbstractController):

    def __init__(self):
        super().__init__("Pure Pursuit")
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        pass

    # init whatever is needed at the start of each path
    def initController(self):
        pass
    
        """
        given current x, y, and theta;
        given desired x, y, and theta of each waypoint
        given list of waypoints

        find closest waypoint; might be given via order of stored data
        for (i>0, i<=maxi -1: i+=1):
            read current pos info
            read desired waypoint info
            find lookahead distance (l=sqrt(xerror^2 + yerror^2))
            
        """

    # Performs one timestep of the pure pursuit algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        #TODO implement this!
        pass