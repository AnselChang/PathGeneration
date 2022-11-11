from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput

"""
Stores all the information about a simulation timestep. Simulation.py stores a list of these objects
"""

class SimulationTimestep:

    # timecode in seconds elapsed since beginning of simulation
    def __init__(self, timecode: float, input: RobotModelInput, output: RobotModelOutput):
        self.timecode: float = timecode
        self.input: RobotModelInput = input
        self.output: RobotModelOutput = output

    def __str__(self):
        return "RobotModelOutput: " + str(self.output)