class SimulationMetrics:
    def __init__(self):
        # Data storage
        self.waiting_times = []  
        self.turnaround_times = []
        self.completed_count = 0
    
    def add_completed_customer(self, customer):
        if hasattr(customer, 'waitingTime') and customer.waitingTime >= 0:
            self.waiting_times.append(customer.waitingTime)
            
        if hasattr(customer, 'turnaroundTime') and customer.turnaroundTime >= 0:
            self.turnaround_times.append(customer.turnaroundTime)
            
        self.completed_count += 1
        
    def get_average_waiting_time(self):
        if not self.waiting_times:
            return 0
        return sum(self.waiting_times) / len(self.waiting_times)
    
    def get_average_turnaround_time(self):
        if not self.turnaround_times:
            return 0
        return sum(self.turnaround_times) / len(self.turnaround_times)