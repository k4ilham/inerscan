import customtkinter as ctk
import os
from app.core.constants import COLORS

class SidebarPanel(ctk.CTkFrame):
    def __init__(self, parent, title, close_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.close_callback = close_callback
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header, text=title.upper(), font=("Segoe UI", 12, "bold")).pack(side="left")
        
        if self.close_callback:
            ctk.CTkButton(header, text="✕", width=30, height=25, fg_color="transparent", text_color="gray", hover_color="#FEE2E2", 
                         command=self.close_callback).pack(side="right")
        
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=5, pady=5)

class TextInputPanel(SidebarPanel):
    def __init__(self, parent, title, callback, prompt_text="Enter value:", close_callback=None):
        super().__init__(parent, title, close_callback)
        self.callback = callback
        
        ctk.CTkLabel(self.content, text=prompt_text, anchor="w").pack(fill="x", padx=5, pady=(10, 5))
        self.entry = ctk.CTkEntry(self.content)
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.apply)
        
        ctk.CTkButton(self.content, text="Confirm", command=self.apply, fg_color=COLORS["primary"]).pack(fill="x", padx=5, pady=10)
        
        self.entry.focus_set()
        
    def apply(self, event=None):
        text = self.entry.get().strip()
        if text:
            self.callback(text)
            if self.close_callback: self.close_callback()

class HistoryPanel(SidebarPanel):
    def __init__(self, parent, db_service, close_callback=None):
        super().__init__(parent, "Scan History", close_callback)
        
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        history = db_service.get_scan_history()
        if not history:
            ctk.CTkLabel(scroll, text="No history found.", text_color="gray").pack(pady=20)
            
        for item in history:
            f = ctk.CTkFrame(scroll, fg_color=COLORS["surface"])
            f.pack(fill="x", pady=2, padx=2)
            
            info = ctk.CTkFrame(f, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            
            # Truncate filename if too long
            fname = item['filename']
            if len(fname) > 20: fname = fname[:17] + "..."
                
            ctk.CTkLabel(info, text=fname, font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"{item['scan_date']}", font=("Segoe UI", 10), text_color="gray", anchor="w").pack(fill="x")
            
            if os.path.exists(item['filepath']):
                ctk.CTkButton(f, text="📂", width=30, height=30, fg_color="transparent", text_color=COLORS["primary"],
                             command=lambda p=item['filepath']: os.startfile(p)).pack(side="right", padx=5)

class HelpPanel(SidebarPanel):
    def __init__(self, parent, guide_service, close_callback=None):
        super().__init__(parent, "Interactive Help", close_callback)
        self.guide_service = guide_service
        self.steps = guide_service.get_steps()
        self.index = 0
        
        self.title_lbl = ctk.CTkLabel(self.content, text="", font=("Segoe UI", 14, "bold"), wraplength=220, justify="left")
        self.title_lbl.pack(pady=(10, 5), padx=5, anchor="w")
        
        self.text_lbl = ctk.CTkLabel(self.content, text="", font=("Segoe UI", 12), wraplength=220, justify="left")
        self.text_lbl.pack(pady=5, padx=5, anchor="w")
        
        nav = ctk.CTkFrame(self.content, fg_color="transparent")
        nav.pack(pady=20, fill="x")
        
        self.prev_btn = ctk.CTkButton(nav, text="<", width=40, command=self.prev_step)
        self.prev_btn.pack(side="left", padx=5)
        
        self.step_lbl = ctk.CTkLabel(nav, text="1/1")
        self.step_lbl.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(nav, text=">", width=40, command=self.next_step)
        self.next_btn.pack(side="right", padx=5)
        
        self.update_step()

    def update_step(self):
        step = self.steps[self.index]
        self.title_lbl.configure(text=step["title"])
        self.text_lbl.configure(text=step["text"])
        self.step_lbl.configure(text=f"{self.index+1}/{len(self.steps)}")
        self.guide_service.speak(step["text"])
        
        self.prev_btn.configure(state="normal" if self.index > 0 else "disabled")
        self.next_btn.configure(text="Finish" if self.index == len(self.steps)-1 else ">", 
                               fg_color=COLORS["success"] if self.index == len(self.steps)-1 else COLORS["primary"])

    def next_step(self):
        if self.index < len(self.steps) - 1:
            self.index += 1
            self.update_step()
        elif self.close_callback:
            self.guide_service.stop()
            self.close_callback()

    def prev_step(self):
        if self.index > 0:
            self.index -= 1
            self.update_step()
