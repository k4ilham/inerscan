import pyttsx3
import threading

class GuideService:
    def __init__(self):
        self.engine = None
        self.stop_event = threading.Event()
        self.thread = None

    def init_engine(self):
        # Initialize engine only when needed
        if not self.engine:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 160)
            except:
                pass

    def speak(self, text):
        if self.thread and self.thread.is_alive():
             self.stop()
        
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._speak_thread, args=(text,))
        self.thread.start()

    def _speak_thread(self, text):
        self.init_engine()
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass

    def stop(self):
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

    def get_steps(self):
        return [
            {
                "title": "Welcome to InerScan v3.0",
                "text": "Welcome! We have upgraded the interface to a modern ribbon style. Features are now organized into tabs at the top of the window."
            },
            {
                "title": "The Home Tab",
                "text": "The Home tab is where you start. Use the large rocket icon to Start a Scan, or the Library icon for Batch Scanning multi-paged documents."
            },
            {
                "title": "AI & Editor Tabs",
                "text": "Switch to the Edit tab for cropping and rotation, or use AI TOOLS for automatic perspective fixing and document cleaning."
            },
            {
                "title": "Exporting Results",
                "text": "When finished, return to the Home tab. You can save all your pages as a single PDF or export individual pages as Images."
            }
        ]
