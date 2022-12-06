import csv
from FileInteraction.AbstractExporter import AbstractExporter
from VisibleElements.FullPath import FullPath
from SingletonState.ReferenceFrame import PointRef

class CSVExporter(AbstractExporter):
    def __init__(self, path: FullPath):
        super().__init__(path)

    # Exports the list of InterpolatedPoints (list of list of PointRefs) to the specified location using the csv module
    def export(self, location: str):
        with open(location, "w+", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for section in self.path.sections:
                for point in section.waypoints:
                    # Each row just contains x,y
                    writer.writerow(point.fieldRef)
                # Black row to signify moving to a new segment
                writer.writerow([])

    # Returns some general information regarding the file extension this exporter uses
    def getExtension(self) -> tuple[str,str]:
        return "Comma-Separated Values Document",".csv"
