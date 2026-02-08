import customtkinter as ctk
from app.core.constants import COLORS
from app.ui.widgets.common import create_ribbon_group, LargeRibbonButton

def setup_ai_tab(app, panel):
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
    app.ai_rename_btn = LargeRibbonButton(openai_grp, "🏷️", "Smart Rename", command=app.perform_smart_rename,
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
