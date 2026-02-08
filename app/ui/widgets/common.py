import customtkinter as ctk
from app.core.constants import COLORS, FONTS

def create_ribbon_group(parent, title):
    # Container for the group
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(side="left", fill="y", padx=5)
    
    # 1. Content Area
    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(side="top", fill="both", expand=True, pady=5)
    
    # 2. Label at bottom (Metadata style)
    ctk.CTkLabel(container, text=title, font=("Segoe UI", 10), text_color=COLORS["text_light"]).pack(side="bottom", pady=(0, 5))
    
    # Divider (Right side)
    sep = ctk.CTkFrame(parent, width=1, height=40, fg_color=COLORS["border"])
    sep.pack(side="left", pady=15, padx=5)
    
    return content

class RibbonButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        # Default Style: Secondary (Zinc-100)
        defaults = {
            "width": 100,
            "height": 34,
            "corner_radius": 6,
            "font": ("Segoe UI", 12),
            "fg_color": COLORS["secondary"],
            "text_color": COLORS["text"],
            "hover_color": COLORS["secondary_dark"]
        }
        for k, v in defaults.items():
            if k not in kwargs: kwargs[k] = v
        super().__init__(master, **kwargs)

class LargeRibbonButton(ctk.CTkFrame):
    def __init__(self, master, icon_text, label_text, command=None, **kwargs):
        self.command = command
        self.raw_fg = kwargs.pop("fg_color", "transparent")
        self.raw_hover = kwargs.pop("hover_color", COLORS["secondary"])
        self.state = "normal"
        
        # Primary Style Check
        is_primary = kwargs.pop("primary", False)
        if is_primary:
            self.raw_fg = COLORS["primary"]
            self.raw_hover = COLORS["primary_light"]
            text_color = "white"
        else:
            text_color = kwargs.pop("text_color", COLORS["text"])

        super().__init__(master, width=kwargs.get("width", 85), height=kwargs.get("height", 80), corner_radius=8, fg_color=self.raw_fg)
        self.pack_propagate(False)
        
        # Inner Layout
        self.icon_lbl = ctk.CTkLabel(self, text=icon_text, font=("Segoe UI Emoji", 26), text_color=text_color)
        self.icon_lbl.place(relx=0.5, rely=0.35, anchor="center")
        
        self.text_lbl = ctk.CTkLabel(self, text=label_text, font=("Segoe UI", 11, "bold"), text_color=text_color)
        self.text_lbl.place(relx=0.5, rely=0.75, anchor="center")
        
        # Events
        for w in [self, self.icon_lbl, self.text_lbl]:
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)

    def configure(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs.pop("state")
            self._update_state()
            
        if "fg_color" in kwargs:
            self.raw_fg = kwargs["fg_color"]
            super().configure(fg_color=self.raw_fg)
            kwargs.pop("fg_color")
            
        if kwargs: super().configure(**kwargs)

    def _update_state(self):
        # Visual dimming for disabled state
        if self.state == "disabled":
            self.icon_lbl.configure(text_color=COLORS["text_lighter"])
            self.text_lbl.configure(text_color=COLORS["text_lighter"])
            super().configure(cursor="")
        else:
            is_primary = (self.raw_fg == COLORS["primary"])
            col = "white" if is_primary else COLORS["text"]
            self.icon_lbl.configure(text_color=col)
            self.text_lbl.configure(text_color=col)
            super().configure(cursor="hand2")

    def _on_click(self, e):
        if self.state != "disabled" and self.command:
            self.command()

    def _on_enter(self, e):
        if self.state != "disabled":
            super().configure(fg_color=self.raw_hover)

    def _on_leave(self, e):
        if self.state != "disabled":
            super().configure(fg_color=self.raw_fg)
