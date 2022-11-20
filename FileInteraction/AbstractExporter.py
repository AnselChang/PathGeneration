from abc import abstractmethod
from VisibleElements.FullPath import FullPath

class AbstractExporter:
    def __init__(self, path: FullPath):
        self.path = path

    @abstractmethod
    def export(self, collection: list, location: str):
        pass

    @abstractmethod
    def getExtension(self) -> tuple[str,str]:
        pass

