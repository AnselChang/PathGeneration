import csv
from FileInteraction.AbstractExporter import AbstractExporter
from VisibleElements.FullPath import FullPath
from SingletonState.ReferenceFrame import PointRef

class CSVExporter(AbstractExporter):
    def __init__(self, path: FullPath):
        super().__init__(path)

    def export(self, location: str):
        with open(location, "w+", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for list in self.path.waypoints.points:
                for point in list:
                    writer.writerow(point.fieldRef)
                writer.writerow([])
