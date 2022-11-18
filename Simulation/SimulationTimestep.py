from Simulation.RobotRelated.RobotModelInput import RobotModelInput
from Simulation.RobotRelated.RobotModelOutput import RobotModelOutput
from Simulation.HUDGraphics.HUDGraphics import HUDGraphics

"""
Stores all the information about a simulation timestep. Simulation.py stores a list of these objects
"""

class SimulationTimestep:

    # timecode in seconds elapsed since beginning of simulation
    def __init__(self, timecode: float, input: RobotModelInput, output: RobotModelOutput, graphics: HUDGraphics):
        self.timecode: float = timecode
        self.input: RobotModelInput = input
        self.output: RobotModelOutput = output
        self.graphics: HUDGraphics = graphics

    def __str__(self):
        return "RobotModelOutput: " + str(self.output)