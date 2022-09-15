from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Sliders.Slider import Slider

from typing import Tuple

from Utility import map_range

"""
A dummy controller that sets the velocities of the wheels to something in order to test other features of the software
"""

class TestController(AbstractController):

    def __init__(self):
        super().__init__("Testing")
    

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
        if self.ticks <= 40: # first 100 ticks, go straight
            return [RobotModelInput(20, 20), False]
        elif self.ticks <=80: # then turn left but slowly come to a stop
            return [RobotModelInput(10, 30), False]
        elif self.ticks <= 200: # let the robot slide with no power
            return [RobotModelInput(-20, -20), False]
        elif self.ticks <= 250: # let the robot slide with no power
            return [RobotModelInput(0,0), False]
        else: # next 100 ticks, stop
            return [RobotModelInput(0, 0), True]
