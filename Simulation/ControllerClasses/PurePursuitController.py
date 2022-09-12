from re import A
from Simulation.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotModelInput import RobotModelInput
from Simulation.RobotModelOutput import RobotModelOutput
from Sliders.Slider import Slider

from typing import Tuple

class PurePursuitController(AbstractController):

    def __init__(self):
        super().__init__("Pure Pursuit")
    

    def defineParameterSliders(self) -> list[Slider]:
        #TODO define the tunable parameters of this controller
        pass

    # Performs one timestep of the pure pursuit algorithm
    # Returns the list of RobotStates at each timestep, and whether the robot has reached the destination
    def simulateTick(self, output: RobotModelOutput) -> Tuple[RobotModelInput, bool]:
        #TODO implement this!
        pass