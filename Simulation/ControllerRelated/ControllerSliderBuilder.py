from Sliders.Slider import Slider
from SingletonState.SoftwareState import SoftwareState
import Utility, colors

state: SoftwareState = None
def initState(stateObject: SoftwareState):
    global state
    state = stateObject

# used for slider onSet lambdas
def setRerunSimulationToTrue():
    print("slider set rerun to true")
    state.rerunSimulation = True

"""
Class to store state regarding the creation of a controller slider
"""
class ControllerSliderState:
    def __init__(self, text: str, default: float, min: float, max: float, step: float):
        self.default = default
        self.text = text
        self.min = min
        self.max = max
        self.step = step

    
# return a list of sliders based on the list of controller slider state
def buildControllerSliders(sliderStates: list[ControllerSliderState]) -> list[Slider]:
    
    sliders: list[Slider] = []

    x = Utility.SCREEN_SIZE + 160
    y = 250
    yOffset = 50
    for sliderState in sliderStates:
        sliders.append(Slider(
                x, y, 75, sliderState.min, sliderState.max, sliderState.step,
                colors.ORANGE, sliderState.text, sliderState.default, setRerunSimulationToTrue
        ))
    
        y += yOffset

    return sliders