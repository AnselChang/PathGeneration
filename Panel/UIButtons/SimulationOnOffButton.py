from Panel.AbstractButtons.FlipFlopButton import FlipFlopButton
import Utility, Graphics
from SingletonState.SoftwareState import SoftwareState
from Simulation.Simulation import Simulation
from VisibleElements.Tooltip import Tooltip
from SingletonState.ReferenceFrame import PointRef
import pygame

"""
Play and pause the simulation. Also initiates simulation calculation
"""

class SimulationOnOffButton(FlipFlopButton):

    def __init__(self, state: SoftwareState, simulation: Simulation):

        self.state = state
        self.simulation = simulation

        self.tooltipPlay = Tooltip("Play simulation")
        self.tooltipPause = Tooltip("Pause simulation")

        imageOn = Graphics.getImage("Images/Buttons/pause.png", 0.08)
        imageHoveredOn = Graphics.getLighterImage(imageOn, 0.75)
        imageOff = Graphics.getImage("Images/Buttons/play.png", 0.08)
        imageHoveredOff = Graphics.getLighterImage(imageOff, 0.75)
        super().__init__((Utility.SCREEN_SIZE + 80, 170), imageOff, imageHoveredOff, imageOn, imageHoveredOn)

    # Draw right button tooltip
    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple) -> None:
        if self.state.playingSimulation:
            self.tooltipPause.draw(screen, mousePosition)
        else:
            self.tooltipPlay.draw(screen, mousePosition)

     # Return whether object is on
    def isOn(self) -> bool:
        return self.state.playingSimulation

  # The action to do when the button is toggled on
    def toggleButton(self) -> None:
        self.state.playingSimulation = not self.state.playingSimulation

        # Rerun simulation if it has changed
        if self.state.playingSimulation and (self.state.rerunSimulation or self.state.simulationController != self.simulation.controllers.getController()):
            
            print("rerunning simulation")
            print(self.state.simulationController)
            print(self.simulation.controllers.getController())
            print(self.state.simulationController != self.simulation.controllers.getController())
            print(self.state.rerunSimulation)

            self.state.rerunSimulation = False

            self.state.simulationController = self.simulation.controllers.getController()
            self.simulation.runSimulation()

        # restart recording if at end
        if self.state.playingSimulation and self.simulation.slider.getValue() == len(self.simulation.recordedSimulation) - 1:
            self.simulation.slider.setValue(0)
