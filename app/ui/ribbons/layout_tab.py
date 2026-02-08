import customtkinter as ctk
from app.core.constants import COLORS, FONTS
from app.ui.widgets.common import create_ribbon_group, LargeRibbonButton

def setup_layout_tab(app, panel):
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
