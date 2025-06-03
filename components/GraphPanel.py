from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from .Globals import getGlobalTime

class GraphPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Data storage
        self.times = []
        self.wait_data = []
        self.turnaround_data = []
        self.throughput_data = []
        self.last_completed = 0
        
        # Create the plots immediately
        self.create_plots()
        
    def create_plots(self):
        # Create figure with subplots
        self.fig, self.axes = plt.subplots(3, 1, figsize=(8, 6))
        
        # Configure plots
        titles = ['Average Waiting Time', 'Average Turnaround Time', 'Throughput']
        ylabels = ['Time (seconds)', 'Time (seconds)', 'Customers/min']
        colors = ['blue', 'red', 'green']
        
        for i, ax in enumerate(self.axes):
            ax.set_title(titles[i], fontsize=9)
            ax.set_ylabel(ylabels[i], fontsize=8)
            ax.grid(True, linestyle='--', alpha=0.7)
            
        self.axes[2].set_xlabel('Time (minutes)', fontsize=8)
        
        # Create the lines
        self.lines = [
            self.axes[0].plot([], [], color=colors[0], linewidth=2)[0],
            self.axes[1].plot([], [], color=colors[1], linewidth=2)[0],
            self.axes[2].plot([], [], color=colors[2], linewidth=2)[0]
        ]
        
        # Adjust spacing
        plt.tight_layout()
        self.fig.subplots_adjust(hspace=0.5)
        
        # Create the canvas widget
        self.canvas_widget = FigureCanvasKivyAgg(figure=self.fig)
        self.add_widget(self.canvas_widget)
    
    def update_data(self, simulation):
        # Skip if there's no metrics
        if not hasattr(simulation, 'metrics'):
            return
            
        # Get simulation time in minutes
        current_time = getGlobalTime() / 60.0
        
        # Get metrics values
        wait_time = simulation.metrics.get_average_waiting_time()
        turnaround_time = simulation.metrics.get_average_turnaround_time()
        
        # Get completed count
        completed_count = getattr(simulation.metrics, 'completed_count', 0)
        
        # Calculate throughput (customers/minute)
        if current_time > 0:
            throughput = completed_count / current_time
        else:
            throughput = 0
            
        # Add data points - only at certain intervals or when customers complete
        should_update = False
        if len(self.times) == 0:
            should_update = True
        elif completed_count > self.last_completed:
            should_update = True 
        elif current_time - self.times[-1] >= 0.5:  # Update every 30 seconds
            should_update = True
            
        if should_update:
            # Store data
            self.times.append(current_time)
            self.wait_data.append(wait_time)
            self.turnaround_data.append(turnaround_time)
            self.throughput_data.append(throughput)
            self.last_completed = completed_count
            
            # Update the plots
            self.update_plots()
    
    def update_plots(self):
        if len(self.times) < 1:
            return
            
        # Update line data
        self.lines[0].set_data(self.times, self.wait_data)
        self.lines[1].set_data(self.times, self.turnaround_data)
        self.lines[2].set_data(self.times, self.throughput_data)
        
        # Update axes limits
        for i, data in enumerate([self.wait_data, self.turnaround_data, self.throughput_data]):
            self.axes[i].set_xlim(0, max(self.times) + 0.1)
            
            # Find max value, default to 10 if all are 0
            max_val = max(data) if any(d > 0 for d in data) else 10
            self.axes[i].set_ylim(0, max_val * 1.1)
        
        # Draw the updated figure
        try:
            self.canvas_widget.draw()
        except Exception as e:
            print(f"Error drawing canvas: {e}")

    def reset(self):
        # Clear all data points
        self.times = []
        self.wait_data = []
        self.turnaround_data = []
        self.throughput_data = []
        self.last_completed = 0
        
        # Reset the plot lines
        for line in self.lines:
            line.set_data([], [])
        
        # Reset axis limits
        for ax in self.axes:
            ax.set_xlim(0, 0.1)
            ax.set_ylim(0, 10)
        
        # Redraw the canvas
        self.canvas_widget.draw()
        
        # Log the reset
        from .ConsoleManager import ConsoleManager
        ConsoleManager.log("Graph data has been reset.")