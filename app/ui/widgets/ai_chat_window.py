import customtkinter as ctk
import threading
from tkinter import messagebox
from app.core.constants import COLORS, FONTS

class AIChatWindow(ctk.CTkFrame):
    def __init__(self, parent, openai_service, get_current_page_callback, close_callback=None):
        super().__init__(parent, fg_color="transparent")
        
        self.openai_service = openai_service
        self.get_current_page = get_current_page_callback
        self.close_callback = close_callback
        self.history = []
        
        self.init_ui()

    def init_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header, text="AI Assistant", font=("Segoe UI", 12, "bold")).pack(side="left")
        if self.close_callback:
            ctk.CTkButton(header, text="✕", width=30, height=25, fg_color="transparent", text_color="gray", hover_color="#FEE2E2", 
                         command=self.close_callback).pack(side="right")
        
        # 1. Chat Area (Scrollable)
        self.chat_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Welcome Message
        self.add_message("assistant", "Hello! I can help you analyze documents or answer questions. How can I assist you today?")

        # 2. Input Area
        input_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], height=60)
        input_frame.pack(fill="x", side="bottom")
        
        # Context Checkbox
        self.context_var = ctk.BooleanVar(value=True)
        self.context_chk = ctk.CTkCheckBox(input_frame, text="Include Current Page", variable=self.context_var, font=("Segoe UI", 10))
        self.context_chk.pack(anchor="w", padx=10, pady=(5,0))
        
        # Entry and Send
        input_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_row.pack(fill="x", padx=5, pady=5)
        
        self.msg_entry = ctk.CTkEntry(input_row, placeholder_text="Type a message...")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))
        self.msg_entry.bind("<Return>", self.send_message)
        
        self.send_btn = ctk.CTkButton(input_row, text="➤", width=40, command=self.send_message, fg_color=COLORS["primary"])
        self.send_btn.pack(side="right", padx=(0, 5))

    def add_message(self, role, text):
        align = "e" if role == "user" else "w"
        color = COLORS["primary"] if role == "user" else COLORS["secondary"]
        text_color = "white" if role == "user" else COLORS["text"]
        
        msg_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5)
        
        # Bubble
        lbl = ctk.CTkLabel(msg_frame, text=text, fg_color=color, text_color=text_color, 
                          corner_radius=12, wraplength=260, justify="left")
        lbl.pack(anchor=align, padx=10, pady=2, ipadx=10, ipady=5)
        
        # Scroll to bottom
        self.chat_scroll._parent_canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg: return
        
        self.msg_entry.delete(0, "end")
        self.add_message("user", msg)
        
        # Prepare context
        pil_image = None
        if self.context_var.get():
            pil_image = self.get_current_page()
        
        # Disable input while processing
        self.send_btn.configure(state="disabled")
        self.msg_entry.configure(state="disabled")
        
        # Threaded API call
        threading.Thread(target=self.process_chat, args=(msg, pil_image), daemon=True).start()

    def process_chat(self, msg, pil_image):
        response = self.openai_service.chat_with_content(msg, self.history, pil_image)
        
        # Update history (without image data to save tokens/complexity in local history for now)
        self.history.append({"role": "user", "content": msg})
        self.history.append({"role": "assistant", "content": response})
        
        self.after(0, lambda: self.finish_chat(response))

    def finish_chat(self, response):
        self.add_message("assistant", response)
        self.send_btn.configure(state="normal")
        self.msg_entry.configure(state="normal")
        self.msg_entry.focus()
