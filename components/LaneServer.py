
from kivy.uix.widget import Widget
from .Globals import isRunning, getGlobalTime, getFormatTime, timeScale

from .ConsoleManager import ConsoleManager
from kivy.properties import StringProperty

import random

class LaneServer(Widget):
    timer_text = StringProperty("")
    laneCount_text = StringProperty("")
    
    def __init__(self, id=0, simulation=None, **kwargs):
        super().__init__(**kwargs)

        self.timer_text = "[X] Inactive"
        self.laneCount_text = "0"

        self.id = 0
        self.simulation = simulation  # reference to the simulation canvas

        self.active = False # defines if the lane is active or not
        self.serverIsActive = False # defines if the server is active or not
        self.canHelp = False # defines if the server can help the other lane
        self.isWorking = False
        self.customers = [] # line queue
        self.completedCustomers = []
        self.length = -1 # defines the length of the line, default -1 for inactive lanes

    """SIMULATION COMPONENT"""
    # handle logic for "handling" tasks to a customer
    def processCustomers(self, secondLane, scenario):
        if (not self.serverIsActive): 
            self.timer_text = "[X] Inactive"
            return
        
        if (len(self.customers) <= 0 and self.canHelp):
            self.timer_text = "[-] Idle"
            
        # if the current server is free, process the first customer in the open queue
        if (not self.isWorking and self.canHelp and len(self.customers) < 2 and len(secondLane.customers) > 1):
            self.customers.append(secondLane.customers.pop(1))
            self.isWorking = True
            self.updateCustomerVisualPosition()
            ConsoleManager.log(f"Server in {self.getID()} is trying to help", '#34eb34')
        
        else:
            if (len(self.customers) <= 0): return
            # check if there's anyone waiting in line
            # check if the current customer has a task assigned
            if (not self.customers[0].hasTask):
                self.updateCustomerVisualPosition()
                
                # if the current customer has just arrived then...
                # assign a task to the customer based on specification #3 (intervals of 1-3 minutes)
                self.customers[0].hasTask = True
                
                # simulate a new task with a burst time of 30 seconds to 3 minutes
                newTaskTime = round(random.uniform(1.5, 3.0) * 60, 1)
                self.customers[0].taskTime = newTaskTime  
                self.customers[0].timeLeft = newTaskTime
                self.timer_text = "[O] Assigning Task"
                ConsoleManager.log(f"Customer {self.customers[0].id} assigned with a task of {self.customers[0].taskTime:.1f} seconds in {self.getID()}")
            
            # if the current customer is done, remove them from the queue
            # second check ensures that the customer actually had a task
            if (self.customers[0].timeLeft <= 0 and self.customers[0].hasTask):
                self.customers[0].completionTime = getGlobalTime()
                self.customers[0].calculatePostTime()
                
                ConsoleManager.log(f"Customer {self.customers[0].id} completed in {self.getID()} at time {getFormatTime()}", '#34ebe5')
                self.customers[0].finish()

                # append the customer to the graphing metrics
                self.simulation.metrics.add_completed_customer(self.customers[0])
                
                # remove the customer from the queue and add them to the completed list
                self.completedCustomers.append(self.customers[0])
                self.customers.pop(0)
                self.isWorking = False
            
            # "serve" the customer
            else:
                formattedTimeLeft = int(round(self.customers[0].timeLeft, 0))
                self.timer_text = f"[O] Time left: {formattedTimeLeft}s"
                self.isWorking = True
                self.customers[0].timeLeft -= 1
        
        # update current size
        self.length = len(self.customers) if self.active else -1

    """END OF SIMULATION COMPONENT """
    ############# HELPER FUNCTIONS #############

    def getID(self):
        return f"Lane {self.id}"
    
    def addCustomer(self, customer):
        if customer:
            self.customers.append(customer)
            self.length = len(self.customers) if self.active else -1
            self.laneCount_text = str(self.length)

        # return the position of the added customer
        # necessary to tell the customer which spot in the line it should go
        return self.length - 1 

    def updateCustomerVisualPosition(self):
        index = 0
        for customer in self.customers:
            customer.setPosition(index, self.id)
            index += 1    

    def reset(self):
        # Clear all customers
        self.customers = []
        self.completedCustomers = []
        
        # Reset state variables
        self.isWorking = False
        self.length = 0 if self.active else -1
        self.laneCount_text = str(self.length)
        self.timer_text = "[-] Idle"

    def printCompletedCustomers(self):
        if len(self.completedCustomers) > 0:
            ConsoleManager.log(f"Completed Customers in {self.getID()}:")
            for customer in self.completedCustomers:
                ConsoleManager.log(f"Customer {customer.id} | Finished at lane: {self.id} | Arrival Time: {customer.arrivalTime} | Burst Time: {customer.taskTime} | Turnaround Time: {customer.turnaroundTime}s | Waiting Time: {customer.waitingTime}s")
        else:
            ConsoleManager.log(f"No completed customers in {self.getID()}.")
            
