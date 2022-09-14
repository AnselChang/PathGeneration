from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
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
        self.ticks = 0

    # Performs one timestep of the stanley algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        #TODO implement this!
        self.ticks += 1
        kp = 0.01
        headingError = 45 - output.heading
        leftVelocity = 5 - kp*headingError
        rightVelocity = 5 + kp*headingError
        return RobotModelInput(leftVelocity, rightVelocity), self.ticks >= 1000 # repeat 100 times before done