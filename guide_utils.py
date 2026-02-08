import pyttsx3
import threading

class GuideService:
    def __init__(self):
        self.engine = None
        self.stop_event = threading.Event()
        self.thread = None

    def init_engine(self):
        # Initialize engine only when needed to avoid blocking main thread on startup
        if not self.engine:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150) # Speed
            except:
                print("TTS Engine failed to initialize")

    def speak(self, text):
        """
         speaks the text in a separate thread to avoid freezing UI.
        """
        if self.thread and self.thread.is_alive():
             self.stop()
        
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._speak_thread, args=(text,))
        self.thread.start()

    def _speak_thread(self, text):
        self.init_engine()
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def stop(self):
        if self.engine:
            self.engine.stop()

    def get_steps(self):
        return [
            {
                "title": "Welcome to InerScan",
                "text": "Welcome! InerScan Pro allows you to scan, edit, and export documents easily. Let's take a quick tour.",
                "image": "guide_1.png" 
            },
            {
                "title": "Start Scanning",
                "text": "To begin, connect your scanner and click the 'START NEW SCAN' button at the top left. This will open the scanning dialog.",
                "image": "guide_2.png" 
            },
            {
                "title": "Edit Functions",
                "text": "Use the tools on the left to Rotate, Adjust Brightness, or Crop your image. You can also remove the background for a cleaner look.",
                "image": "guide_3.png" 
            },
            {
                "title": "Exporting",
                "text": "When you are done, use the 'Save All to PDF' button to create a single PDF file from all your scanned pages.",
                "image": "guide_4.png" 
            }
        ]
