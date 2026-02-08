import sys
import os
sys.path.append(os.getcwd())

try:
    from app.ui.widgets.ai_chat_window import AIChatWindow
    # Mock dependencies
    class MockService:
        def chat_with_content(self, msg, h, img): return "Mock Response"

    def mock_get_page(): return None
    
    import customtkinter as ctk
    
    app = ctk.CTk()
    chat_win = AIChatWindow(app, MockService(), mock_get_page)
    print("Chat Window initialized successfully")
    chat_win.destroy()
    app.destroy()
except Exception as e:
    print(f"Chat verification failed: {e}")
    import traceback
    traceback.print_exc()
