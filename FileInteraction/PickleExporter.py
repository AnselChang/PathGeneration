from FileInteraction.AbstractExporter import AbstractExporter
from VisibleElements.FullPath import FullPath
import pickle

class PickleExporter(AbstractExporter):
    def __init__(self, path: FullPath):
        super().__init__(path)

    # Exports the list of PathPoints to the specified location using the pickle library
    def export(self, location: str):
        with open(location, "wb") as exportFile:
            # use self.path.pathPoints
            pickle.dump(self.path.sections, exportFile)

    # Returns some general information regarding the file extension this exporter uses
    def getExtension(self) -> tuple[str,str]:
        return "Path Document",".path"
