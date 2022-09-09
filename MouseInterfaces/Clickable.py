from MouseInterfaces.Hoverable import Hoverable
from abc import ABC, abstractmethod


"""Python "Interface" for objects that are clickable by the mouse. If an object that is Hoverable is clicked, we check
if that object is also Clickable, and if so, call the click() function


Useful for Button."""

class Clickable(Hoverable):

    def __init__(self):
        super().__init__()

    # Called the first frame the mouse is down on a hovered object
    @abstractmethod
    def click():
        pass