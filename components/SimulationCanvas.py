from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty

from .Customer import Customer
from .LaneServer import LaneServer
from .Globals import incrementGlobalTime, getGlobalTime, formatTimeDifference, getFrameCounter
from .ConsoleManager import ConsoleManager

from .SimulationMetrics import SimulationMetrics
from .GraphPanel import GraphPanel

import random

"""simulation specifications:"""
    # time: 1 second is equivalent to the variable time unit
    # > see globals.py to see time unit
    # customers arrive at different or same intervals (max of 2 mins)
    # customers draws a scenario card that determines how long their service will take (1-3 mins)
    # servers only server one customer

    # scenarios
    # 0 >> 1 server 
    # 1 >> 2 server 1 lane
    # 2 >> 2 server 2 lane (server is exclusive to one lane)
    # 3 >> server 2 self.lane (server can help if lane is free)
    
    # Simulation cycle summary:
    # 1 > Check if the customer arrival cooldown is over
    #   1.2 > Spawn a new customer if cooldown is over
    #   1.3 > Let the customer choose a lane
    # 2 > Process lane logic   
    # >> repeat cycle

class SimulationCanvas(Widget):
    scenario_label = StringProperty("Current Scenario: 1")
    avgWTText = StringProperty("Average Wait Time: 0s")
    avgTATText = StringProperty("Average Turnaround Time: 0s")
    aveThroughputText = StringProperty("Throughput: 0 customers/min")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.cooldown = 0
        self.lane1 = LaneServer(id=1, simulation=self)
        self.lane2 = LaneServer(id=2, simulation=self)

        self.metrics = SimulationMetrics()

        self.customerCount = 1
        self.customers = []
        self.lastCustomerArrivalTime = 0

        # refer to simulation specifications below 
        self.currentScenario = 0 

        # by default, self.lane 1 is always open
        #self.lane1.length = 0
        self.lane2.length = 0
        
        # by default, self.lane 2 has its queue and server inactive
        """ self.lane1.active = True
        self.lane2.active = True
        
        self.lane1.serverIsActive = True
        self.lane2.serverIsActive = True
        
        self.lane1.canHelp = True
        self.lane2.canHelp = True """

        self.lane1.id = 1
        self.lane2.id = 2

        self.setScenario(self.currentScenario)

        self.lane1.pos = (850, 430)
        self.lane2.pos = (850, 580)
        
        self.add_widget(self.lane1)
        self.add_widget(self.lane2)

         # label variables
        self.scenario_label = "Current Scenario: 1"
        self.avgWTText = "Average Wait Time: 0s"
        self.avgTATText = "Average Turnaround Time: 0s"
        self.aveThroughputText = "Throughput: 0 customers/min"
        Clock.schedule_interval(self.updateMetricsLabels, 1.0)

    """SIMULATION COMPONENT""" 
    
    def simulate(self):
        global globalCurrentTime
        if (self.cooldown <= 0):
            # find the when the new customer arrived relative to the last one
            currentTime = getGlobalTime()
            timeSinceLastCustomer = currentTime - self.lastCustomerArrivalTime
            
            timeGap = formatTimeDifference(timeSinceLastCustomer)
            ConsoleManager.log(f"Customer arrived (+{timeGap} since last arrival)", "#ff00dd")

            self.lastCustomerArrivalTime = currentTime

            # spawn a customer object
            newCustomer = Customer()
            newCustomer.arrivalTime = getGlobalTime()
            newCustomer.id = self.customerCount
            
            # let the customer choose a lane
            newCustomer.chooseLane(self.lane1, self.lane2)
            
            # Add a grapical object of the customer
            self.customers.append(newCustomer)
            self.add_widget(newCustomer)

            # Display a console log of the queue's status
            customerList1 = [customer.getID() for customer in self.lane1.customers] if self.lane1.customers else []
            customerList2 = [customer.getID() for customer in self.lane2.customers] if self.lane2.customers else []
            ConsoleManager.log(f"Lane {self.lane1.id} - Current Queue: {customerList1}" if self.lane1.serverIsActive else f"Lane {self.lane1.id} - Inactive", '#34eb49')
            ConsoleManager.log(f"Lane {self.lane2.id} - Current Queue: {customerList2}" if self.lane2.serverIsActive else f"Lane {self.lane2.id} - Inactive", '#34eb49')
            
            # generate a customer arrival cooldown between 30 seconds to 2 minutes
            newCooldown = round(random.uniform(0.5, 2.0), 1)
            ConsoleManager.log(f"Next customer will arrive in {newCooldown} minutes", '#ff00dd')
            self.cooldown = newCooldown * 60

            # increase global customer count
            self.customerCount += 1
        
        if (getFrameCounter() == 0):
            self.cooldown -= 1
            # ConsoleManager.log(f"Cooldown: {self.cooldown:.2f} seconds remaining", '#ff0000')
            self.lane1.processCustomers(self.lane2, self.currentScenario)
            self.lane2.processCustomers(self.lane1, self.currentScenario)
    
    """END OF SIMULATION COMPONENT"""

    def reset(self):
        for customer in self.customers:
            self.remove_widget(customer)
        self.customers = []
       
        self.lane1.reset()
        self.lane2.reset()
        
        self.metrics = SimulationMetrics()
        
        self.customerCount = 1
        self.lastCustomerArrivalTime = 0
        self.cooldown = 0

        self.avgWTText = "Average Wait Time: 0s"
        self.avgTATText = "Average Turnaround Time: 0s"
        self.aveThroughputText = "Throughput: 0 customers/min"
        
        #self.ids.scenarioValue.text = f"Scenario {self.scenario}"
    
    def setScenario(self, scenario):
        self.currentScenario = scenario
        
        scenario_names = [
            "1 Server : 1 Lane",
            "2 Servers : 1 Lane", 
            "2 Servers : 2 Lane (exclusive)", 
            "2 Servers : 2 Lane (shared)"
        ]

        self.scenario_label = f"Current Scenario: {scenario_names[scenario]}"

        if scenario == 0:
            self.lane1.active = True
            self.lane1.serverIsActive = True
            self.lane1.canHelp = False
            
            self.lane2.active = False
            self.lane2.serverIsActive = False
            self.lane2.canHelp = False
            
            ConsoleManager.log("Scenario 1: Single server, single lane activated", '#ffcc00')
            
        elif scenario == 1:
            self.lane1.active = True
            self.lane1.serverIsActive = True
            self.lane1.canHelp = False
            
            self.lane2.active = False
            self.lane2.serverIsActive = True
            self.lane2.canHelp = True
            
            ConsoleManager.log("Scenario 2: Two servers, single lane activated", '#ffcc00')
            
        elif scenario == 2: 
            self.lane1.active = True
            self.lane1.serverIsActive = True
            self.lane1.canHelp = False
            
            self.lane2.active = True
            self.lane2.serverIsActive = True
            self.lane2.canHelp = False
            
            ConsoleManager.log("Scenario 3: Two servers, two lanes (exclusive servers)", '#ffcc00')
            
        elif scenario == 3:
            self.lane1.active = True
            self.lane1.serverIsActive = True
            self.lane1.canHelp = True
            
            self.lane2.active = True
            self.lane2.serverIsActive = True
            self.lane2.canHelp = True
            
            ConsoleManager.log("Scenario 4: Two servers, two lanes (servers can help other lane)", '#ffcc00')

    def updateMetricsLabels(self, dt):
        if hasattr(self, 'metrics'):
            # Get metrics
            avg_wait = self.metrics.get_average_waiting_time()
            avg_turnaround = self.metrics.get_average_turnaround_time()
            
            elapsed_time = max(0.01, getGlobalTime() / 60)
            
            # Calculate throughput
            completed_count = getattr(self.metrics, 'completed_count', 0)
            throughput = completed_count / elapsed_time
            
            # Update the label texts
            self.avgWTText = f"Average Wait Time: {int(avg_wait)}s"
            self.avgTATText = f"Average Turnaround Time: {int(avg_turnaround)}s"
            self.aveThroughputText = f"Throughput: {throughput:.2f} customers/min"

        
        
