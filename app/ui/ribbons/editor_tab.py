import tkinter as tk
import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, RibbonButton, LargeRibbonButton

def setup_editor_tab(app, panel):
    # ==================== EDITOR TOOLS ====================
    
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

    # ==================== FROM AI TAB ====================

    cv_grp = create_ribbon_group(panel, "AI Enhancement")
    
    # Perspective
    app.ai_persp_btn = LargeRibbonButton(cv_grp, "📐", "Perspective", command=app.perspective_fix, 
                                        fg_color=COLORS["accent_violet"], text_color="white")
    app.ai_persp_btn.pack(side="left", padx=3)
    
    # Clean
    app.ai_clean_btn = LargeRibbonButton(cv_grp, "📝", "Clean Doc", command=app.clean_document, 
                                        fg_color=COLORS["accent_lime"], text_color="white")
    app.ai_clean_btn.pack(side="left", padx=3)
    
    # Privacy
    app.ai_blur_btn = LargeRibbonButton(cv_grp, "🕵️", "Privacy", command=app.privacy_blur, 
                                       fg_color=COLORS["accent_fuchsia"], text_color="white")
    app.ai_blur_btn.pack(side="left", padx=3)
    
    # Straighten
    app.ai_straight_btn = LargeRibbonButton(cv_grp, "📐", "Straighten", command=app.auto_straighten, 
                                           fg_color=COLORS["accent_sky"], text_color="white")
    app.ai_straight_btn.pack(side="left", padx=3)

    # OpenAI Group
    openai_grp = create_ribbon_group(panel, "OpenAI Intelligence")
    
    # Settings
    app.ai_settings_btn = LargeRibbonButton(openai_grp, "⚙️", "Settings", command=app.open_openai_settings,
                                           fg_color=COLORS["text_light"], text_color="white")
    app.ai_settings_btn.pack(side="left", padx=3)

    # OCR
    app.ai_ocr_btn = LargeRibbonButton(openai_grp, "📝", "OCR Text", command=app.perform_ocr,
                                      fg_color=COLORS["accent_lime"], text_color="white")
    app.ai_ocr_btn.pack(side="left", padx=3)

    # Smart Rename
    app.ai_rename_btn = LargeRibbonButton(openai_grp, "🏷️", "Rename", command=app.perform_smart_rename,
                                         fg_color=COLORS["accent_sky"], text_color="white")
    app.ai_rename_btn.pack(side="left", padx=3)

    # Analyze
    app.ai_analyze_btn = LargeRibbonButton(openai_grp, "📊", "Analyze", command=app.perform_analysis,
                                          fg_color=COLORS["accent_violet"], text_color="white")
    app.ai_analyze_btn.pack(side="left", padx=3)

    # Chat
    app.ai_chat_btn = LargeRibbonButton(openai_grp, "💬", "Chat AI", command=app.open_chat_window,
                                       fg_color=COLORS["accent_fuchsia"], text_color="white")
    app.ai_chat_btn.pack(side="left", padx=3)

    # ==================== FROM ANNOTATE TAB ====================
    
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

    # ==================== FROM LAYOUT TAB ====================
    
    # 1. Book Tools
    book_grp = create_ribbon_group(panel, "Book & Duplex")
    
    app.split_btn = LargeRibbonButton(book_grp, "📖", "Split Page", command=app.split_current_page,
                                     fg_color=COLORS["accent_sky"], text_color="white")
    app.split_btn.pack(side="left", padx=3)
    
    app.reverse_btn = LargeRibbonButton(book_grp, "🔄", "Reverse", command=app.reverse_pages,
                                       fg_color=COLORS["accent_violet"], text_color="white")
    app.reverse_btn.pack(side="left", padx=3)

    # 2. Collage Group
    grid_grp = create_ribbon_group(panel, "Collage & Grid")
    
    # Layout Selector
    sel_col = ctk.CTkFrame(grid_grp, fg_color="transparent")
    sel_col.pack(side="left", padx=5)
    
    ctk.CTkLabel(sel_col, text="Grid Layout", font=FONTS["small"], text_color="white").pack(anchor="w")
    app.grid_layout_var = ctk.StringVar(value="2x2")
    ctk.CTkOptionMenu(sel_col, variable=app.grid_layout_var,
                      values=["1x2", "2x1", "2x2", "3x2", "2x3", "3x3", "4x4"],
                      width=100, height=28, font=FONTS["small"]).pack(pady=5)
    
    app.collage_btn = LargeRibbonButton(grid_grp, "🖼️", "Create Grid", command=app.create_collage_grid,
                                       fg_color=COLORS["accent_lime"], text_color="white")
    app.collage_btn.pack(side="left", padx=10)

    # ==================== FROM LIBRARY TAB ====================
    
    # 1. Archives Group
    lib_grp = create_ribbon_group(panel, "Library")
    
    app.view_hist_btn = LargeRibbonButton(lib_grp, "📜", "History", command=app.show_scan_history,
                                         fg_color=COLORS["accent_violet"], text_color="white")
    app.view_hist_btn.pack(side="left", padx=5)
    
    app.open_folder_btn = LargeRibbonButton(lib_grp, "📂", "Open Folder", command=app.open_output_folder,
                                           fg_color=COLORS["accent_orange"], text_color="white")
    app.open_folder_btn.pack(side="left", padx=5)
    
    app.clear_hist_btn = LargeRibbonButton(lib_grp, "🗑️", "Clear Logs", command=app.clear_history_confirm,
                                          fg_color=COLORS["danger"], text_color="white")
    app.clear_hist_btn.pack(side="left", padx=5)
