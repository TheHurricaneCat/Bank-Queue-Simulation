from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from .ConsoleManager import ConsoleManager
from .Globals import isRunning, incrementGlobalTime, resetGlobalTime
from kivy.app import App
from kivy.core.clipboard import Clipboard
import re


class ControlPanel(BoxLayout):        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation = None
        self.ids.scenarioSpinner.bind(text=self.on_scenario_selected)

    def setSimulation(self, simulationCanvas):
        self.simulation = simulationCanvas

    def startSimulation(self):
        global isRunning
        if not isRunning:
            isRunning = True
            self.ids.startButton.text = "Stop Simulation"
            ConsoleManager.log("Simulation started.")
            
            if self.simulation:
                self.simulation_event = Clock.schedule_interval(
                    lambda dt: self.simulation.simulate(), 1.0/60.0)
                self.time_event = Clock.schedule_interval(
                    lambda dt: incrementGlobalTime(), 1.0/60.0)
            else:
                ConsoleManager.log("Error: Simulation reference not set")
        else:
            isRunning = False
            if hasattr(self, 'simulation_event'):
                Clock.unschedule(self.simulation_event)
            if hasattr(self, 'time_event'):
                Clock.unschedule(self.time_event)
            self.ids.startButton.text = "Start Simulation"
            ConsoleManager.log("Simulation stopped.")

    def copyLog(self):
        app = App.get_running_app()
        log_text = app.logText
        
        clean_text = re.sub(r'\[color=[^\]]*\]|\[/color\]', '', log_text)
        Clipboard.copy(clean_text)
        ConsoleManager.log("Console log copied to clipboard.", '#ffff00')

    def printCompletedCustomers(self):
        """Print details of all completed customers in both lanes"""
        if not self.simulation:
            ConsoleManager.log("Error: No simulation reference set")
            return
            
        # Print a header
        ConsoleManager.log("--------- COMPLETED CUSTOMERS SUMMARY ---------", '#ffff00')
        
        # Call printCompletedCustomers on both lanes
        if hasattr(self.simulation, 'lane1'):
            self.simulation.lane1.printCompletedCustomers()
        
        if hasattr(self.simulation, 'lane2'):
            self.simulation.lane2.printCompletedCustomers()
        
        # Access metrics for summary statistics
        if hasattr(self.simulation, 'metrics'):
            metrics = self.simulation.metrics
            avg_wait = metrics.get_average_waiting_time()
            avg_turnaround = metrics.get_average_turnaround_time()
            completed_count = getattr(metrics, 'completed_count', 0)
            
            # Print summary statistics
            ConsoleManager.log("--------- SUMMARY STATISTICS ---------", '#ffff00')
            ConsoleManager.log(f"Total Completed Customers: {completed_count}")
            ConsoleManager.log(f"Average Waiting Time: {avg_wait:.2f} seconds")
            ConsoleManager.log(f"Average Turnaround Time: {avg_turnaround:.2f} seconds")
        
        ConsoleManager.log("-------------------------------------------", '#ffff00')

    def resetSimulation(self):
        global isRunning
        
        if isRunning:
            isRunning = False
            if hasattr(self, 'simulation_event'):
                Clock.unschedule(self.simulation_event)
            if hasattr(self, 'time_event'):
                Clock.unschedule(self.time_event)
            self.ids.startButton.text = "Start Simulation"
        
        resetGlobalTime()

        ConsoleManager.clear()
        
        # Reset the simulation state
        if self.simulation:
            self.simulation.reset()
            ConsoleManager.log("Simulation has been reset.", '#00ff00')
        else:
            ConsoleManager.log("Error: Simulation reference not set")

        app = App.get_running_app()
        if hasattr(app.root, 'graph_panel'):
            app.root.graph_panel.reset()
            ConsoleManager.log("Graphs have been reset.", '#00ff00')

    def on_scenario_selected(self, spinner, text):
        if not self.simulation:
            ConsoleManager.log("Error: No simulation reference set")
            return
            
        # Map spinner text to scenario number
        scenario_mapping = {
            '1 Server : 1 Lane': 0,
            '2 Servers : 1 Lane': 1,
            '2 Servers : 2 Lane (ex)': 2,
            '2 Servers : 2 Lane (sd)': 3
        }
        
        # Get scenario number from the mapping
        if text in scenario_mapping:
            scenario = scenario_mapping[text]
            self.simulation.setScenario(scenario)
            ConsoleManager.log(f"Changed to scenario: {text}", '#ffcc00')
        else:
            ConsoleManager.log(f"Unknown scenario: {text}", '#ff0000')
        