from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Sliders.Slider import Slider

from typing import Tuple

"""
A more sophisticated controller that is theorized to follow lines better.
https://dingyan89.medium.com/three-methods-of-vehicle-lateral-control-pure-pursuit-stanley-and-mpc-db8cc1d32081
"""

class StanleyController(AbstractController):

    def __init__(self):
        super().__init__("Stanley")
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        pass

    # init whatever is needed at the start of each path
    def initController(self):
        pass

    # Performs one timestep of the stanley algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        #TODO implement this!
        pass