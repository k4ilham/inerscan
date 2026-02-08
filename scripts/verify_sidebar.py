import sys
import os
import customtkinter as ctk

# Mock current dir
sys.path.append(os.getcwd())

from app.ui.widgets.text_result_panel import TextResultPanel
from app.ui.widgets.ai_chat_window import AIChatWindow

app = ctk.CTk()
app.geometry("400x600")

# Test Chat Panel
class MockService:
    def chat_with_content(self, msg, h, img): return "Mock Response"

panel = AIChatWindow(app, MockService(), lambda: None, close_callback=lambda: print("Close"))
panel.pack(fill="both", expand=True)

# Test Text Result Panel in 2 seconds
def switch_to_text():
    panel.pack_forget()
    txt_panel = TextResultPanel(app, "TEST RESULTS", "This is a test result.", close_callback=lambda: print("Close Text"))
    txt_panel.pack(fill="both", expand=True)
    print("Switched to TextPanel")
    app.after(1000, app.destroy)

app.after(1000, switch_to_text)
app.mainloop()
print("Sidebar Verification Complete")
