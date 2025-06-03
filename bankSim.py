from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label

from components import SimulationCanvas, ControlPanel, ConsolePanel
from components.ConsoleManager import ConsoleManager
from components.GraphPanel import GraphPanel
from kivy.properties import StringProperty
from kivy.clock import Clock

from kivy.core.window import Window

import random

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # set a seed for reproducibility
        random.seed(42)
        
        self.simulation = SimulationCanvas()
        self.simulation.size_hint_y = 0.5
        self.add_widget(self.simulation)

        console = ConsolePanel()
        console.size_hint_y = 0.1
        ConsoleManager.initialize(console)
        self.add_widget(console)

        ConsoleManager.log("Simulation started.")

        control_info_panel = BoxLayout(size_hint_y=0.4)
        control_panel = ControlPanel()
        control_panel.size_hint_x = 0.2
        control_panel.size_hint_y = 1
        control_panel.setSimulation(self.simulation)

        self.graph_panel = GraphPanel()
        self.graph_panel.size_hint_x = 0.8
        
        control_info_panel.add_widget(control_panel)
        control_info_panel.add_widget(self.graph_panel)

        self.add_widget(control_info_panel)
        
        Clock.schedule_interval(self.update_graphs, 1.0)

    def update_graphs(self, dt):
        if hasattr(self, 'graph_panel') and hasattr(self, 'simulation'):
            self.graph_panel.update_data(self.simulation)

    def reset_simulation(self):
        if hasattr(self, 'simulation'):
            self.simulation.reset()
        
        if hasattr(self, 'graph_panel'):
            self.graph_panel.reset()

class MyApp(App):
    logText = StringProperty("")
    
    def build(self):
        #Window.size = (800, 700)
        
        Builder.load_file('bankSim.kv')
        return MainWidget()
            
if __name__ == '__main__':
    MyApp().run()