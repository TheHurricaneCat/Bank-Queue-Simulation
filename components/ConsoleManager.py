
from .Globals import getFormatTime

class ConsoleManager:
    _console = None
    
    @classmethod
    def initialize(cls, console_instance):
        cls._console = console_instance

    @classmethod
    def log(cls, message, color=None):
        if not color: 
            color = '#ffffff'
        
        if cls._console:

            timestamp = getFormatTime()
            formatted_msg = f"[color={color}][{timestamp}] {message}[/color]\n"
            
            # Update app property
            from kivy.app import App
            app = App.get_running_app()
            app.logText = formatted_msg + app.logText
        else:
            print("Warning: Console not initialized, message:", message)

    @classmethod
    def clear(cls):
        if cls._console:
            cls._console.clear_log()
        else:
            print("Warning: Console not initialized, cannot clear log.")