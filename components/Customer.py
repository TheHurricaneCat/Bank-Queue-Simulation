from kivy.uix.widget import Widget
from kivy.properties import ListProperty

from .ConsoleManager import ConsoleManager
from kivy.properties import StringProperty

import random

class Customer(Widget):
    color = ListProperty([1, 0, 1, 1])
    name_text = StringProperty("Customer")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = [
            random.random(),      # Random red (0.0-1.0)
            random.random(),      # Random green (0.0-1.0)
            random.random(),      # Random blue (0.0-1.0)
            1                     # Full opacity
        ]
        
        #self.pos = (750 + 110, 439) # <-- use as reference for lane 2
        #self.pos = (860, 439)
        self.pos = (10, 510) # <-- use as reference for customer spawning

        self.id = 0
        self.lane = 0
        
        self.hasTask = False
        self.taskTime = 0 # burst time essentially
        self.timeLeft = self.taskTime # decrement as if bank scenario is being processed
        self.arrivalTime = 0
        self.completionTime = 0

        self.turnaroundTime = 0
        self.waitingTime = 0

    def getID(self):
        self.name_text = f"Customer {self.id}"
        return f"Customer-{self.id}"
    
    def setPosition(self, newPosition, lane):
        if (newPosition > 6):
            self.color = self.color[:3] + [0]  # Set opacity to 0.5 if position is greater than 6
        else:
            self.color = self.color[:3] + [1]
        if (lane == 1):
            self.pos = (860 - 110 * newPosition, 439)
        elif (lane == 2):
            self.pos = (860 - 110 * newPosition, 590)

    def finish(self):
        # calculate for internal metrics
        self.calculatePostTime()
        ConsoleManager.log(f"Customer {self.id} finished processing. Arrival Time: {self.arrivalTime} Burst Time: {self.taskTime} Turnaround Time: {self.turnaroundTime}, Waiting Time: {self.waitingTime}", "#34eb34")
        # hide the graphic object
        self.color = [0, 0, 0, 0]
    
    def chooseLane(self, lane1, lane2):
        # if lane 2 is inactive, always go to the first lane
        if not lane2.active:
            self.lane = 1
            newPosition = lane1.addCustomer(self)
            self.setPosition(newPosition, self.lane)
            return self.lane

        if (lane1.length < lane2.length):
            self.lane = 1
            newPosition = lane1.addCustomer(self)
            self.setPosition(newPosition, self.lane)
        else:
            newPosition = lane2.addCustomer(self)
            self.lane = 2
            self.setPosition(newPosition, self.lane)
        
        ConsoleManager.log(f"Customer {self.id} chooses to go to Lane {self.lane}", "#e5eb34")
        return self.lane

    def calculatePostTime(self):
        # TAT = CT - AT
        self.turnaroundTime = int(self.completionTime - self.arrivalTime)
        # WT = TAT - BT
        self.waitingTime = int(self.turnaroundTime - self.taskTime)
        return (self.turnaroundTime, self.waitingTime)
