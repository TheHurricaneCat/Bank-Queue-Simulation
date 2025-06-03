from kivy.properties import StringProperty
from kivy.event import EventDispatcher
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

isRunning = False
# aka a "simulation tick"
globalCurrentTime = 0
timeScale = 100
fps = 60 
frameCounter = 0

# essentially, 1 tick is 1/60th of a second
# so it takes 60 ticks to represent 1 second of real time
def incrementGlobalTime():
    global globalCurrentTime, frameCounter
    frameCounter += 1

    if frameCounter >= fps / timeScale:
        globalCurrentTime += 1 
        frameCounter = 0
    
    return globalCurrentTime

def getGlobalTime():
    return globalCurrentTime

def resetGlobalTime():
    global globalCurrentTime, frameCounter
    globalCurrentTime = 0
    frameCounter = 0

def getFormatTime():
    hours = globalCurrentTime // 3600
    minutes = (globalCurrentTime % 3600) // 60
    seconds = globalCurrentTime % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def getFrameCounter():
    return frameCounter

def formatTimeDifference(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

class ConsolePanel(BoxLayout):  # Change from Widget to BoxLayout for better layout
    logText = StringProperty("")
    maxLines = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_label = Label(text=self.logText, halign='left', valign='top')
        self.log_label.bind(size=self.log_label.setter('text_size'))
        self.add_widget(self.log_label)
        
        self.bind(logText=self.update_label)
        
    def update_label(self, instance, value):
        self.log_label.text = value

    def pushLog(self, text):
        timestamp = globalCurrentTime
        new_entry = f"[{timestamp}] {text}\n"

        self.logText = new_entry + self.logText
        
        lines = self.logText.split('\n')
        if len(lines) > self.maxLines:
            self.logText = '\n'.join(lines[:self.maxLines])
    
    def clear_log(self):
        self.logText = ""

consoleLog = ConsolePanel()