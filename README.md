# Bank Queue System

A bank line simulator made by Josefe Johnatan M. Gillego. Made with Python (Backend), Kivy (GUI) and Matplotlib (Graphing).

![image](https://github.com/user-attachments/assets/c50aa04f-6056-4672-b431-305515e4fa4a)


### Simulation Rules and Specifications:
1. Customers "arrive" at different intervals or same intervals (e.g., every 30 seconds). (max of 2mins)
2. Each customer draws a scenario card that determines how long their service will take (e.g., 1–3 minutes).
3. Tellers serve one customer at a time, using a timer to simulate service duration.

### Scenario Specifications:
1. Simulate using 1 server.
2. Simulate using 2 servers with one line.
3. Simulate using 2 servers with two line (server is exclusive to 1 line).
4. Simulate using 2 servers with two line (server is exclusive to 1 line but can serve other lane if free).

### Simulation Features:
1. **Customer-teller interaction visualization** - Visually see which line a customer would go, what's their position in the line, and how much time is left before their "task" is done)
2. **Simulation logging** - Built-in console that can display the status of each customer and teller, can show the passing of time, can print the metrics of each customer that has arrived and finished during the simulation duration.
3. **Real-time Metrics** - Visually see how different scenarios and simulation parameters affect metrics like average waiting time, turnaround time, and throughput. These metrics are plotted in a graph in real time to reflect the data.

### Future Improvements:
1. Responsive and resizeable window. (Animation is bound to an absolute position in the canvas.)
2. Front-end controls for simulation parameters. (Currently, the only way to change *arrival intervals*, *task time randomization range*, *simulation seed*, *time factr*, and *the states of the lines and tellers* are by editing the variables found in `SimulationCanvas.py` and `Globals.py`)
3. Upgrade matplotlib. (**CRITICAL ERROR** Any mouse inputs done inside the matplotlib graphs causes a crash).

### Other notes:
*You can change the random module's seed through `BankSim.py`*
