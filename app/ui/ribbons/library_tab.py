import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, LargeRibbonButton

def setup_library_tab(app, panel):
    # 1. Archives Group
    hist_grp = create_ribbon_group(panel, "Archives")
    
    app.view_hist_btn = LargeRibbonButton(hist_grp, "📜", "History", command=app.show_scan_history,
                                         fg_color=COLORS["accent_violet"], text_color="white")
    app.view_hist_btn.pack(side="left", padx=5)
    
    app.open_folder_btn = LargeRibbonButton(hist_grp, "📂", "Open Folder", command=app.open_output_folder,
                                           fg_color=COLORS["accent_orange"], text_color="white")
    app.open_folder_btn.pack(side="left", padx=5)

    # 2. Maintenance Group
    maint_grp = create_ribbon_group(panel, "System")
    
    app.clear_hist_btn = LargeRibbonButton(maint_grp, "🗑️", "Clear Logs", command=app.clear_history_confirm,
                                          fg_color=COLORS["danger"], text_color="white")
    app.clear_hist_btn.pack(side="left", padx=5)
