from Simulation.ControllerRelated.ControllerClasses.AbstractController import AbstractController
from Simulation.ControllerRelated.ControllerClasses.PurePursuitController import PurePursuitController
from Simulation.ControllerRelated.ControllerClasses.StanleyController import StanleyController
from Simulation.ControllerRelated.ControllerClasses.AnselPPController import AnselPPController
from Simulation.ControllerRelated.ControllerSliderBuilder import ControllerSliderState, buildControllerSliders
from Sliders.Slider import Slider

"""
Store references to each controller, and manage which controller is currently selected
"""

class ControllerManager:

    def __init__(self):

        self.controllers: list[AbstractController] = [
            AnselPPController(),
            PurePursuitController(),
            #StanleyController()
        ]
        self.index = 0 # index of selected controller in controller list

    # return the currently-selected controller
    def getController(self) -> AbstractController:
        return self.controllers[self.index]
    
    # get the name of the currently-selected controller
    def getCurrentName(self) -> str:
        return self.controllers[self.index].name
    
    # get the list of sliders for the currently-selected controller
    def getCurrentSliders(self) -> list[Slider]:
        return self.controllers[self.index].sliders

    # Whether there is a controller before the currently-selected one
    def isPrevious(self) -> bool:
        return self.index > 0

    # Go to the previous controller, if it exists
    def previous(self) -> None:
        if self.isPrevious():
            self.index -= 1

    # Whether there is a controller after the currently-selected one
    def isNext(self) -> bool:
        return self.index < len(self.controllers) - 1

    # Go to the previous controller, if it exists
    def next(self) -> None:
        if self.isNext():
            self.index += 1