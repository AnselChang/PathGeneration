from VisibleElements.FullPath import FullPath
from VisibleElements.PathPoint import PathPoint
from SingletonState.SoftwareState import SoftwareState
import pickle

def importFile(filename: str, state: SoftwareState, path: FullPath):
    with open(filename, "rb") as importFile:
        path.sections: list[PathPoint] = pickle.load(importFile)
        path.currentSection = 0
        state.rerunSimulation = True
