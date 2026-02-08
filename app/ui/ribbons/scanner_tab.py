import tkinter as tk
import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, RibbonButton, LargeRibbonButton

def setup_scanner_tab(app, panel):
    # 1. Capture Group
    cap_grp = create_ribbon_group(panel, "Capture")
    app.scan_btn = LargeRibbonButton(cap_grp, "🔴", "START SCAN", command=app.perform_scan, 
                                    fg_color=COLORS["accent_fuchsia"], text_color="white", width=100)
    app.scan_btn.pack(side="left", padx=4)
    
    app.batch_scan_btn = LargeRibbonButton(cap_grp, "📚", "Batch Scan", command=app.start_batch_scan, 
                                          fg_color=COLORS["accent_violet"], text_color="white", width=90)
    app.batch_scan_btn.pack(side="left", padx=4)
    
    app.batch_status = ctk.CTkLabel(cap_grp, text="", font=FONTS["micro"], text_color=COLORS["text"])
    app.batch_status.place(relx=0.5, rely=0.05, anchor="n")
    
    # 2. Settings Group
    set_grp = create_ribbon_group(panel, "Settings")
    ctk.CTkLabel(set_grp, text="Paper Size", font=FONTS["small"], text_color="white").pack(pady=(5, 0))
    
    app.paper_sizes = {
        "A4 (210×297mm)": (2480, 3508), "Letter (8.5×11in)": (2550, 3300),
        "A3 (297×420mm)": (3508, 4961), "Legal (8.5×14in)": (2550, 4200),
        "A5 (148×210mm)": (1748, 2480), "Custom...": None
    }
    app.paper_size_var = tk.StringVar(value="A4 (210×297mm)")
    size_menu = ctk.CTkOptionMenu(set_grp, variable=app.paper_size_var,
                                  values=list(app.paper_sizes.keys()),
                                  command=app.on_paper_size_change, width=160, height=32,
                                  fg_color=COLORS["accent_teal"], button_color=COLORS["accent_teal"],
                                  button_hover_color=COLORS["accent_sky"])
    size_menu.pack(pady=5)

    # 3. Export Group
    exp_grp = create_ribbon_group(panel, "Export")
    
    # Large Action Buttons for Export
    app.save_img_btn = LargeRibbonButton(exp_grp, "🖼️", "Save Image", command=app.save_as_image, 
                                        fg_color=COLORS["accent_sky"], text_color="white", width=95)
    app.save_img_btn.pack(side="left", padx=4)
    app.save_img_btn.configure(state="disabled")
    
    app.save_pdf_btn = LargeRibbonButton(exp_grp, "📄", "Save PDF", command=app.save_as_pdf,
                                       fg_color=COLORS["accent_orange"], text_color="white", width=95)
    app.save_pdf_btn.pack(side="left", padx=4)
    app.save_pdf_btn.configure(state="disabled")

    # Filename & Browse
    file_col = ctk.CTkFrame(exp_grp, fg_color="transparent")
    file_col.pack(side="left", padx=10)
    
    ctk.CTkLabel(file_col, text="File Prefix", font=FONTS["small"], text_color="white").pack(anchor="w")
    ctk.CTkEntry(file_col, textvariable=app.filename_prefix, width=130, height=28, font=FONTS["body"]).pack(pady=(0, 5))
    ctk.CTkButton(file_col, text="📁 Browse", command=app.browse_folder, width=130, height=24, 
                 font=FONTS["small"], fg_color="transparent", border_width=1, 
                 border_color="white", text_color="white").pack()

    # Utilities
    util_col = ctk.CTkFrame(exp_grp, fg_color="transparent")
    util_col.pack(side="left", padx=5)
    
    app.preview_pdf_btn = RibbonButton(util_col, text="🔍 Preview", command=app.preview_pdf,
                                      width=100, height=32, fg_color=COLORS["accent_violet"], text_color="white", state="disabled")
    app.preview_pdf_btn.pack(pady=2)
    
    app.print_btn = RibbonButton(util_col, text="🖨️ Print", command=app.print_document,
                                width=100, height=32, fg_color=COLORS["accent_lime"], text_color="white", state="disabled")
    app.print_btn.pack(pady=2)
