import customtkinter as ctk
from tkinter import messagebox
import threading

class OpenAISettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, openai_service, close_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.openai_service = openai_service
        self.close_callback = close_callback
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header, text="SETTINGS", font=("Segoe UI", 12, "bold")).pack(side="left")
        if self.close_callback:
            ctk.CTkButton(header, text="✕", width=30, height=25, fg_color="transparent", text_color="gray", hover_color="#FEE2E2", 
                         command=self.close_callback).pack(side="right")
        
        # Scrollable Content
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # API Key
        ctk.CTkLabel(content, text="API Key:", font=("Segoe UI", 11)).pack(anchor="w", padx=5, pady=(10, 2))
        self.api_key_entry = ctk.CTkEntry(content, width=240, show="*")
        self.api_key_entry.pack(fill="x", padx=5, pady=2)
        
        # Base URL
        ctk.CTkLabel(content, text="Base URL:", font=("Segoe UI", 11)).pack(anchor="w", padx=5, pady=(10, 2))
        self.base_url_entry = ctk.CTkEntry(content, width=240, placeholder_text="https://api.openai.com/v1")
        self.base_url_entry.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(content, text="(Optional, for proxies/SumoPod)", font=("Arial", 9), text_color="gray").pack(anchor="w", padx=5)
        
        # Model
        ctk.CTkLabel(content, text="Model:", font=("Segoe UI", 11)).pack(anchor="w", padx=5, pady=(10, 2))
        self.model_entry = ctk.CTkComboBox(content, width=240, values=["gpt-4o", "gpt-4o-mini", "o1-mini"])
        self.model_entry.pack(fill="x", padx=5, pady=2)
        
        # Test Connection Button
        self.test_btn = ctk.CTkButton(content, text="Test Connection", command=self.test_connection, 
                                     fg_color="#3B82F6", hover_color="#2563EB")
        self.test_btn.pack(fill="x", padx=5, pady=(20, 5))
        
        self.status_label = ctk.CTkLabel(content, text="", text_color="gray", font=("Segoe UI", 10))
        self.status_label.pack(fill="x", padx=5, pady=2)
        
        # Save Button
        ctk.CTkButton(content, text="Save Settings", command=self.save_settings, 
                     fg_color="#10B981", hover_color="#059669").pack(fill="x", padx=5, pady=10)

    def load_settings(self):
        self.api_key_entry.insert(0, self.openai_service.api_key)
        self.base_url_entry.insert(0, self.openai_service.base_url)
        self.model_entry.set(self.openai_service.model)

    def test_connection(self):
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip()
        
        if not api_key:
            messagebox.showerror("Error", "API Key is required")
            return
            
        self.status_label.configure(text="Testing...", text_color="blue")
        self.test_btn.configure(state="disabled")
        
        def run_test():
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key, base_url=base_url if base_url else "https://api.openai.com/v1")
                client.models.list()
                success = True
                msg = "✅ Connection Successful"
            except Exception as e:
                success = False
                msg = f"❌ Failed: {str(e)[:30]}..."
            
            self.after(0, lambda: self.show_test_result(success, msg))

        threading.Thread(target=run_test, daemon=True).start()

    def show_test_result(self, success, msg):
        self.test_btn.configure(state="normal")
        self.status_label.configure(text=msg, text_color="green" if success else "red")

    def save_settings(self):
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip()
        model = self.model_entry.get().strip()
        
        if not model: model = "gpt-4o"
        
        self.openai_service.update_settings(api_key, base_url, model)
        messagebox.showinfo("Saved", "Settings saved successfully")
        if self.close_callback: self.close_callback()

