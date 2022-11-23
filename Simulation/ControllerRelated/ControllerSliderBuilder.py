from Sliders.Slider import Slider
import Utility, colors

"""
Class to store state regarding the creation of a controller slider
"""
class ControllerSliderState:
    def __init__(self, text: str, min: float, max: float, step: float):
        self.text = text
        self.min = min
        self.max = max
        self.step = step

    
# return a list of sliders based on the list of controller slider state
def buildControllerSliders(sliderStates: list[ControllerSliderState]) -> list[Slider]:
    
    sliders: list[Slider] = []

    x = Utility.SCREEN_SIZE + 125
    y = 250
    yOffset = 50
    for sliderState in sliderStates:
        sliders.append(Slider(
                x, y, 75, sliderState.min, sliderState.max, sliderState.step, colors.ORANGE, sliderState.text
        ))
    
        y += yOffset

    return sliders