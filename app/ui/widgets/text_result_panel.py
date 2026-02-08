import customtkinter as ctk

class TextResultPanel(ctk.CTkFrame):
    def __init__(self, parent, title, text, close_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.close_callback = close_callback
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 12, "bold")).pack(side="left")
        
        if self.close_callback:
            ctk.CTkButton(header, text="✕", width=30, height=25, fg_color="transparent", text_color="gray", hover_color="#FEE2E2", 
                         command=self.close_callback).pack(side="right")
        
        # Text Area
        self.textbox = ctk.CTkTextbox(self, wrap="word", font=("Consolas", 11))
        self.textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.textbox.insert("1.0", text)
        
        # Copy Button
        ctk.CTkButton(self, text="Copy to Clipboard", command=self.copy_text, height=30).pack(fill="x", padx=10, pady=10)
        
    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get("1.0", "end-1c"))
