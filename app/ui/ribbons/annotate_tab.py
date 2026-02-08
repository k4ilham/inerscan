import tkinter as tk
import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, LargeRibbonButton

def setup_annotate_tab(app, panel):
    # 1. Text Group
    text_grp = create_ribbon_group(panel, "Text Content")
    app.add_text_btn = LargeRibbonButton(text_grp, "➕", "Add Text", command=app.open_text_dialog,
                                        fg_color=COLORS["accent_violet"], text_color="white")
    app.add_text_btn.pack(side="left", padx=5)
    
    # 2. Watermark Group
    wm_grp = create_ribbon_group(panel, "Watermark / Stamp")
    
    # Selection Controls
    sel_col = ctk.CTkFrame(wm_grp, fg_color="transparent")
    sel_col.pack(side="left", padx=5)
    
    ctk.CTkLabel(sel_col, text="Text", font=FONTS["small"], text_color="white").pack(anchor="w")
    app.watermark_text = tk.StringVar(value="COPY")
    ctk.CTkOptionMenu(sel_col, variable=app.watermark_text, 
                      values=["COPY", "DRAFT", "CONFIDENTIAL", "APPROVED", "SAMPLE", "VOID", "ORIGINAL"],
                      width=110, height=28, font=FONTS["small"]).pack(pady=(0, 5))
    
    ctk.CTkLabel(sel_col, text="Position", font=FONTS["small"], text_color="white").pack(anchor="w")
    app.watermark_position = tk.StringVar(value="center")
    ctk.CTkOptionMenu(sel_col, variable=app.watermark_position, 
                      values=["center", "top-right", "bottom-right", "top-left", "bottom-left"],
                      width=110, height=28, font=FONTS["small"]).pack()
                      
    # Apply
    app.apply_wm_btn = LargeRibbonButton(wm_grp, "🏷️", "Apply Stamp", command=app.apply_watermark,
                                        fg_color=COLORS["accent_orange"], text_color="white")
    app.apply_wm_btn.pack(side="left", padx=10)
