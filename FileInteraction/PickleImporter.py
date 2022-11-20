from FileInteraction.AbstractExporter import AbstractExporter
from VisibleElements.FullPath import FullPath
from VisibleElements.PathPoint import PathPoint
from SingletonState.SoftwareState import SoftwareState
import pickle

class PickleImporter:
    def __init__(self, state: SoftwareState, path: FullPath):
        self.path = path
        self.state = state

    def importFile(self, location: str):
        with open(location, "w+", newline='') as importFile:
            self.path.pathPoints: list[PathPoint] = pickle.load(importFile)
            self.state.recomputeInterpolation = True
            
    def getExtension(self) -> tuple[str,str]:
        return "Path Document",".path"
