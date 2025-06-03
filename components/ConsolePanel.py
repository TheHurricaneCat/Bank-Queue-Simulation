from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.app import App
from .Globals import isRunning, globalCurrentTime, getFormatTime

class ConsolePanel(BoxLayout):
    logText = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add a dark background
        from kivy.graphics import Color, Rectangle
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark color
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Create scrollable text label
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(
            size_hint=(0.9, 1.0),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10
        )
        self.log_label = Label(text=self.logText, size_hint_y=None, halign='left', valign='top')
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)
        
        # Bind the property
        self.bind(logText=self._update_label)
    
    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def _update_label(self, instance, value):
        self.log_label.text = value
    
    def clear_log(self):
        self.logText = ""  # Set the property to empty string
        
        # Force update the label directly as well
        if hasattr(self, 'log_label'):
            self.log_label.text = ""

        app = App.get_running_app()
        app.logText = ""