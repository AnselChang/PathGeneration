from Panel.AbstractButtons.ToggleButton import ToggleButton
import Utility

class LeftButton(ToggleButton):

    def __init__(self):
        super().__init__((Utility.SCREEN_SIZE+100, 100), "")