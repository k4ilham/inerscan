import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, RibbonButton, LargeRibbonButton

def setup_editor_tab(app, panel):
    # 1. History Group (Undo / Redo)
    hist_grp = create_ribbon_group(panel, "History")
    app.undo_btn = LargeRibbonButton(hist_grp, "↶", "Undo", command=app.undo, 
                                    fg_color=COLORS["accent_sky"], text_color="white", width=70)
    app.undo_btn.pack(side="left", padx=2)
    app.redo_btn = LargeRibbonButton(hist_grp, "↷", "Redo", command=app.redo, 
                                    fg_color=COLORS["accent_teal"], text_color="white", width=70)
    app.redo_btn.pack(side="left", padx=2)

    # 2. Tools Group
    trans_grp = create_ribbon_group(panel, "Transform")
    btns = [("↺", lambda: app.rotate(-90)), ("↻", lambda: app.rotate(90)), 
            ("↔", app.toggle_flip_h), ("↕", app.toggle_flip_v)]
    
    grid = ctk.CTkFrame(trans_grp, fg_color="transparent")
    grid.pack(expand=True)
    colors_list = [COLORS["accent_violet"], COLORS["accent_fuchsia"], COLORS["accent_orange"], COLORS["accent_lime"]]
    for i, (txt, cmd) in enumerate(btns):
        ctk.CTkButton(grid, text=txt, command=cmd, width=45, height=35, 
                     fg_color=colors_list[i], text_color="white",
                     border_width=0,
                     hover_color=COLORS["button_hover"],
                     font=("Segoe UI", 14, "bold")).grid(row=i//2, column=i%2, padx=2, pady=2)

    # 3. Adjust Group
    adjust_grp = create_ribbon_group(panel, "Adjust")
    
    # Brightness
    b_frame = ctk.CTkFrame(adjust_grp, fg_color="transparent")
    b_frame.pack(fill="x", pady=2)
    ctk.CTkLabel(b_frame, text="☀️", font=("Segoe UI", 12)).pack(side="left", padx=2)
    app.bright_slider_editor = ctk.CTkSlider(b_frame, from_=0.5, to=2.0, command=app.update_brightness, 
                                            width=110, height=16, progress_color=COLORS["accent_orange"])
    app.bright_slider_editor.set(1.0)
    app.bright_slider_editor.pack(side="left", padx=5)
    
    # Contrast
    c_frame = ctk.CTkFrame(adjust_grp, fg_color="transparent")
    c_frame.pack(fill="x", pady=2)
    ctk.CTkLabel(c_frame, text="🌓", font=("Segoe UI", 12)).pack(side="left", padx=2)
    app.cont_slider_editor = ctk.CTkSlider(c_frame, from_=0.5, to=2.0, command=app.update_contrast, 
                                          width=110, height=16, progress_color=COLORS["accent_violet"])
    app.cont_slider_editor.set(1.0)
    app.cont_slider_editor.pack(side="left", padx=5)
    
    app.gray_switch_editor = ctk.CTkSwitch(adjust_grp, text="Black & White", command=app.toggle_grayscale, 
                                          font=FONTS["small"], progress_color=COLORS["accent_fuchsia"])
    app.gray_switch_editor.pack(pady=4)

    # 4. Operations Group
    ops_grp = create_ribbon_group(panel, "Refine")
    app.crop_btn = LargeRibbonButton(ops_grp, "✂️", "Crop Tool", command=app.toggle_crop_mode, 
                                    fg_color=COLORS["accent_orange"], text_color="white")
    app.crop_btn.pack(side="left", padx=4)
    
    app.resize_btn = LargeRibbonButton(ops_grp, "📏", "Resize", command=app.resize_to_paper_size, 
                                      fg_color=COLORS["accent_teal"], text_color="white")
    app.resize_btn.pack(side="left", padx=4)
