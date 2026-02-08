import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
from PIL import Image, ImageTk, ImageEnhance

# Services
from app.services.scanner_service import ScannerService
from app.services.image_service import ImageProcessor
from app.services.db_service import DatabaseService
from app.services.guide_service import GuideService
from app.services.ai_openai_service import OpenAIService

# UI Components
from app.core.constants import COLORS, FONTS
from app.ui.widgets.openai_settings_dialog import OpenAISettingsPanel
from app.ui.widgets.ai_chat_window import AIChatWindow
from app.ui.widgets.text_result_panel import TextResultPanel
from app.ui.widgets.sidebar_panels import TextInputPanel, HistoryPanel, HelpPanel
from app.ui.widgets.animations import LoadingSpinner, ProgressOverlay, ToastNotification, AnimatedProgressBar
from app.ui.ribbons.scanner_tab import setup_scanner_tab
from app.ui.ribbons.editor_tab import setup_editor_tab
from app.ui.ribbons.ai_tab import setup_ai_tab
from app.ui.ribbons.annotate_tab import setup_annotate_tab
from app.ui.ribbons.layout_tab import setup_layout_tab
from app.ui.ribbons.library_tab import setup_library_tab

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Services
        self.db_service = DatabaseService()
        self.scanner_service = ScannerService()
        self.scanner_service = ScannerService()
        self.guide_service = GuideService()
        self.openai_service = OpenAIService(self.db_service)

        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Scans")
        saved_dir = self.db_service.get_setting("output_dir", default_dir)
        saved_prefix = self.db_service.get_setting("filename_prefix", "Scan")

        self.title("InerScan Pro")
        self.geometry("1400x900")
        self.configure(fg_color=COLORS["bg_gradient_start"])

        # Variables
        self.pages = []
        self.current_page_index = -1
        self.cropping_active = False
        self.crop_start = None
        self.crop_end = None
        self.display_scale = 1.0
        self.zoom_level = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.tk_image_ref = None
        self.output_dir = tk.StringVar(value=saved_dir)
        self.filename_prefix = tk.StringVar(value=saved_prefix)
        
        # Trace settings changes
        self.output_dir.trace_add("write", lambda *args: self.db_service.save_setting("output_dir", self.output_dir.get()))
        self.filename_prefix.trace_add("write", lambda *args: self.db_service.save_setting("filename_prefix", self.filename_prefix.get()))

        # UI State
        self.current_tab = "scanner"
        self.batch_scanning = False
        self.batch_count = 0
        self.batch_target = 0
        self.batch_delay = 2000

        self.init_ui()

    def init_ui(self):
        # 1. Top Section (Header + ribbon)
        self.top_section = ctk.CTkFrame(self, fg_color=COLORS["surface"], height=140, corner_radius=0)
        self.top_section.pack(fill="x", side="top")
        self.top_section.pack_propagate(False)
        
        # Bottom border for top section (simulated with a frame)
        border_line = ctk.CTkFrame(self.top_section, height=1, fg_color=COLORS["border"])
        border_line.pack(side="bottom", fill="x")

        # Header / Tabs
        self.header_bar = ctk.CTkFrame(self.top_section, fg_color="transparent", height=50)
        self.header_bar.pack(fill="x", padx=20, pady=10)
        
        # Logo/Title with professional blue color
        title_label = ctk.CTkLabel(self.header_bar, text="InerScan Pro", 
                                   font=("Segoe UI", 20, "bold"), 
                                   text_color=COLORS["primary"])
        title_label.pack(side="left", padx=(0, 20))

        # Tabs Container with colorful tabs
        self.nav_buttons = {}
        tabs = [("scanner", "Home"), ("editor", "Edit"), ("ai", "AI Tools"), ("annotate", "Annotate"), ("layout", "Layout"), ("library", "Library")]
        tab_colors = {
            "scanner": COLORS["accent_fuchsia"],
            "editor": COLORS["accent_orange"],
            "ai": COLORS["accent_violet"],
            "annotate": COLORS["accent_lime"],
            "layout": COLORS["accent_sky"],
            "library": COLORS["accent_teal"]
        }
        
        def make_cmd(tid):
            return lambda: self.switch_tab(tid)

        for tab_id, text in tabs:
            btn = ctk.CTkButton(self.header_bar, text=text, width=80, height=32, corner_radius=6,
                               command=make_cmd(tab_id),
                               fg_color="transparent", text_color=COLORS["primary"],
                               hover_color=tab_colors[tab_id], font=("Segoe UI", 13))
            btn.pack(side="left", padx=2)
            self.nav_buttons[tab_id] = btn
            # Store the tab color for later use
            btn.tab_color = tab_colors[tab_id]

        # Help Button with blue text
        ctk.CTkButton(self.header_bar, text="Help", width=60, height=32, corner_radius=6,
                     fg_color="transparent", text_color=COLORS["primary"],
                     hover_color=COLORS["button_hover"], font=("Segoe UI", 13),
                     command=self.show_help_guide).pack(side="right")

        # Ribbon Content Container (Sub-toolbar)
        self.ribbon_content = ctk.CTkFrame(self.top_section, fg_color="transparent", corner_radius=0)
        self.ribbon_content.pack(fill="both", expand=True, padx=20, pady=5)

        # 2. Session Bar (Removed or Merged? Let's remove to be cleaner and just put current file info in status bar or header)
        # Replacing Session Bar with a spacer line or just removing it for cleaner look.
        # Let's keep a thin separator if needed, but Shadcn is open.
        # We will skip the session bar and go straight to body.

        # 3. Main Body
        self.main_body = ctk.CTkFrame(self, fg_color="transparent")
        self.main_body.pack(fill="both", expand=True)

        # Right Sidebar (Thumbnails) - Clean white with left border
        # Container for Resize Handle + Sidebar Content
        self.sidebar_container = ctk.CTkFrame(self.main_body, fg_color="transparent")
        self.sidebar_container.pack(fill="y", side="right")
        
        # Resize Handle (Simulated with a thin frame)
        self.resize_handle = ctk.CTkFrame(self.sidebar_container, width=5, fg_color=COLORS["border"], cursor="sb_h_double_arrow")
        self.resize_handle.pack(side="left", fill="y")
        self.resize_handle.bind("<Button-1>", self.start_resize)
        self.resize_handle.bind("<B1-Motion>", self.do_resize)
        
        # Sidebar Content Area
        self.current_sidebar_width = 350
        self.right_sidebar = ctk.CTkFrame(self.sidebar_container, fg_color=COLORS["surface"], width=self.current_sidebar_width, corner_radius=0)
        self.right_sidebar.pack(side="right", fill="y")
        self.right_sidebar.pack_propagate(False) # Strict width
        
        self.setup_right_sidebar()

        # Center Preview
        self.center_area = ctk.CTkFrame(self.main_body, fg_color=COLORS["bg_gradient_end"], corner_radius=0)
        self.center_area.pack(fill="both", expand=True, side="left")
        
        # Grid layout for scrollbars
        self.center_area.grid_rowconfigure(0, weight=1)
        self.center_area.grid_columnconfigure(0, weight=1)

        self.preview_canvas = tk.Canvas(self.center_area, bg=COLORS["bg_gradient_end"], highlightthickness=0)
        self.preview_canvas.grid(row=0, column=0, sticky="nsew", padx=(20, 0), pady=(20, 0))
        
        self.v_scroll = ctk.CTkScrollbar(self.center_area, orientation="vertical", command=self.preview_canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=(20, 0))
        
        self.h_scroll = ctk.CTkScrollbar(self.center_area, orientation="horizontal", command=self.preview_canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew", padx=(20, 0), pady=(0, 20))
        
        self.preview_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        self.preview_canvas.bind("<Button-1>", self.on_mouse_down)
        self.preview_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # 4. Status Bar
        self.status_bar = ctk.CTkFrame(self, fg_color=COLORS["surface"], height=30, corner_radius=0, border_width=1, border_color=COLORS["border"])
        self.status_bar.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(self.status_bar, text="✅ Ready", font=("Segoe UI", 10))
        self.status_label.pack(side="left", padx=15)
        
        # Animated Progress Bar
        self.progress_bar = AnimatedProgressBar(self.status_bar, width=200, height=8, corner_radius=4, progress_color=COLORS["primary"])
        self.progress_bar.set(0)
        self.progress_bar.pack(side="right", padx=15)

        # Zoom Slider
        zoom_frame = ctk.CTkFrame(self.status_bar, fg_color="transparent")
        zoom_frame.pack(side="right", padx=10)
        ctk.CTkLabel(zoom_frame, text="🔍", font=("Segoe UI", 10)).pack(side="left")
        self.zoom_slider = ctk.CTkSlider(zoom_frame, from_=0.2, to=3.0, width=120, height=16, command=self.on_zoom_change)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(side="left", padx=5)
        self.zoom_label = ctk.CTkLabel(zoom_frame, text="100%", width=40, font=FONTS["micro"])
        self.zoom_label.pack(side="left")

        # Initialize Ribbon Panels
        self.ribbon_panels = {}
        for tab_id in ["scanner", "editor", "ai", "annotate", "layout", "library"]:
            self.ribbon_panels[tab_id] = ctk.CTkFrame(self.ribbon_content, fg_color="transparent")
        
        # Setup each tab's content
        setup_scanner_tab(self, self.ribbon_panels["scanner"])
        setup_editor_tab(self, self.ribbon_panels["editor"])
        setup_ai_tab(self, self.ribbon_panels["ai"])
        setup_annotate_tab(self, self.ribbon_panels["annotate"])
        setup_layout_tab(self, self.ribbon_panels["layout"])
        setup_library_tab(self, self.ribbon_panels["library"])
        
        self.switch_tab("scanner")
        
        # Loading Overlay (hidden by default)
        self.loading_overlay = ProgressOverlay(self, message="Processing...")
        
        # Loading spinner for status bar
        self.loading_spinner = LoadingSpinner(self.status_bar, size=20, color=COLORS["primary"])
        # Don't pack it yet, will show when needed

    def setup_right_sidebar(self):
        # Header (generic)
        self.sidebar_header = ctk.CTkFrame(self.right_sidebar, fg_color="transparent", height=40)
        self.sidebar_header.pack(fill="x", padx=5, pady=5)
        self.sidebar_title = ctk.CTkLabel(self.sidebar_header, text="PAGE THUMBNAILS", font=("Segoe UI", 11, "bold"))
        self.sidebar_title.pack(side="left", padx=5)
        
        # Close/Back button (hidden by default)
        self.sidebar_back_btn = ctk.CTkButton(self.sidebar_header, text="< Back", width=60, height=24, 
                                             fg_color="transparent", text_color=COLORS["primary"],
                                             command=self.show_thumbnails)
        
        # Content Container (Stack)
        self.sidebar_content = ctk.CTkFrame(self.right_sidebar, fg_color="transparent")
        self.sidebar_content.pack(fill="both", expand=True)
        
        # 1. Thumbnails Panel (Default)
        self.thumbnails_panel = ctk.CTkFrame(self.sidebar_content, fg_color="transparent")
        
        header_actions = ctk.CTkFrame(self.thumbnails_panel, fg_color="transparent", height=30)
        header_actions.pack(fill="x", padx=5, pady=0)
        self.page_badge = ctk.CTkLabel(header_actions, text="0", fg_color=COLORS["accent_fuchsia"], 
                                      text_color="white", corner_radius=10, width=25, font=("Segoe UI", 11, "bold"))
        self.page_badge.pack(side="right")

        self.thumb_scroll = ctk.CTkScrollableFrame(self.thumbnails_panel, fg_color="transparent")
        self.thumb_scroll.pack(fill="both", expand=True, padx=0)
        
        actions = ctk.CTkFrame(self.thumbnails_panel, fg_color="transparent", height=60)
        actions.pack(fill="x", padx=5, pady=10)
        self.delete_btn = ctk.CTkButton(actions, text="Delete", fg_color=COLORS["accent_orange"], 
                                       text_color="white", command=self.delete_current_page, 
                                       hover_color=COLORS["danger"], state="disabled")
        self.delete_btn.pack(side="left", fill="x", expand=True, padx=2)
        self.clear_all_btn = ctk.CTkButton(actions, text="Clear All", fg_color=COLORS["danger"], 
                                          text_color="white", command=self.clear_all_pages, state="disabled")
        self.clear_all_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        self.thumbnails_panel.pack(fill="both", expand=True) # default
        
        self.current_sidebar_panel = self.thumbnails_panel

    def switch_sidebar_to(self, panel_widget, title=None):
        # Hide current
        if self.current_sidebar_panel:
            self.current_sidebar_panel.pack_forget()
        
        # Show new
        panel_widget.pack(fill="both", expand=True)
        self.current_sidebar_panel = panel_widget
        
        # Update header
        if title:
            self.sidebar_title.configure(text=title.upper())
            self.sidebar_back_btn.pack(side="right", padx=5)
        else:
            self.sidebar_title.configure(text="")
            self.sidebar_back_btn.pack(side="right", padx=5)

    def show_thumbnails(self):
        # If returning from another panel, destroy it if it's not the thumbnails panel
        if self.current_sidebar_panel != self.thumbnails_panel:
            self.current_sidebar_panel.destroy()
        
        self.current_sidebar_panel = self.thumbnails_panel
        self.thumbnails_panel.pack(fill="both", expand=True)
        self.sidebar_title.configure(text="PAGE THUMBNAILS")
        self.sidebar_back_btn.pack_forget()

    # --- Core Logic ---
    def switch_tab(self, tab_id):
        self.current_tab = tab_id
        for tid, btn in self.nav_buttons.items():
            is_active = (tid == tab_id)
            if is_active:
                # Use the tab's unique color when active
                btn.configure(
                    fg_color=btn.tab_color if hasattr(btn, 'tab_color') else COLORS["primary"], 
                    text_color="white",
                    font=("Segoe UI", 13, "bold")
                )
            else:
                btn.configure(
                    fg_color="transparent", 
                    text_color=COLORS["primary"],
                    font=("Segoe UI", 13, "normal")
                )
        
        # Hide all, then show one
        for panel in self.ribbon_panels.values():
            panel.pack_forget()
        
        if tab_id in self.ribbon_panels:
            self.ribbon_panels[tab_id].pack(fill="both", expand=True)
            
        self.sync_editor_controls()

    def sync_editor_controls(self):
        if self.current_tab == "editor" and self.current_page_index != -1:
            p = self.pages[self.current_page_index]
            self.bright_slider_editor.set(p['brightness'])
            self.cont_slider_editor.set(p['contrast'])
            if p['grayscale']: self.gray_switch_editor.select()
            else: self.gray_switch_editor.deselect()

    def select_page(self, index):
        if 0 <= index < len(self.pages):
            self.current_page_index = index
            self.display_page(self.pages[index]['processed'])
            self.update_thumbnails()
            self.sync_editor_controls()
            # Enable buttons
            for b in [self.save_img_btn, self.save_pdf_btn, self.preview_pdf_btn, self.print_btn, self.delete_btn, self.clear_all_btn]:
                b.configure(state="normal")

    def display_page(self, pil_image):
        if not pil_image: return
        self.update_idletasks()
        cw, ch = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        if cw < 100: cw, ch = 800, 600
        
        # Base scale to fit screen
        fit_scale = min(cw / pil_image.width, ch / pil_image.height) * 0.95
        self.display_scale = fit_scale * self.zoom_level
        
        new_size = (int(pil_image.width * self.display_scale), int(pil_image.height * self.display_scale))
        if new_size[0] < 1 or new_size[1] < 1: return
        
        disp_img = pil_image.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_image_ref = ImageTk.PhotoImage(disp_img)
        self.preview_canvas.delete("all")
        
        # Center the image relative to the scrollregion
        # If smaller than canvas, we still want it centered
        self.preview_canvas.create_image(max(cw, new_size[0])/2, max(ch, new_size[1])/2, 
                                       image=self.tk_image_ref, tags="page_img", anchor="center")
        
        # Update scrollregion
        self.preview_canvas.config(scrollregion=(0, 0, max(cw, new_size[0]), max(ch, new_size[1])))

    def on_zoom_change(self, val):
        self.zoom_level = float(val)
        self.zoom_label.configure(text=f"{int(self.zoom_level * 100)}%")
        if self.current_page_index != -1:
            self.display_page(self.pages[self.current_page_index]['processed'])
        else:
            # If no page, just reset scrollregion
            self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))

    def update_thumbnails(self):
        for w in self.thumb_scroll.winfo_children(): w.destroy()
        for i, p in enumerate(self.pages):
            is_sel = (i == self.current_page_index)
            # Use colorful gradient for selected thumbnail
            sel_color = COLORS["accent_violet"] if is_sel else "transparent"
            f = ctk.CTkFrame(self.thumb_scroll, fg_color=sel_color, height=80, corner_radius=8)
            f.pack(fill="x", pady=2, padx=5)
            f.pack_propagate(False)
            
            thumb = p['processed'].copy()
            thumb.thumbnail((70, 60))
            tk_t = ImageTk.PhotoImage(thumb)
            l_img = tk.Label(f, image=tk_t, bg=sel_color if is_sel else COLORS["surface"])
            l_img.image = tk_t
            l_img.pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"Page {i+1}", text_color="white" if is_sel else COLORS["text"], 
                        font=("Segoe UI", 11, "bold" if is_sel else "normal")).pack(side="left", padx=5)
            
            for w in [f, l_img]: 
                w.bind("<Button-1>", lambda e, idx=i: self.select_page(idx))

    def create_page_data(self, pil_image):
        """Helper to create a standard page dictionary with all required keys"""
        return {
            'original': pil_image.copy(),
            'processed': pil_image.copy(),
            'rotation': 0,
            'flip_h': False,
            'flip_v': False,
            'brightness': 1.0,
            'contrast': 1.0,
            'grayscale': False,
            'undo_stack': [],
            'redo_stack': []
        }

    def apply_modifications(self, index):
        if not (0 <= index < len(self.pages)): return
        p = self.pages[index]
        img = p['original'].copy()
        if p['rotation'] != 0: img = img.rotate(p['rotation'], expand=True)
        if p['flip_h']: img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if p['flip_v']: img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if p['brightness'] != 1.0: img = ImageEnhance.Brightness(img).enhance(p['brightness'])
        if p['contrast'] != 1.0: img = ImageEnhance.Contrast(img).enhance(p['contrast'])
        if p['grayscale']: img = img.convert('L')
        p['processed'] = img
        self.display_page(img)
        self.update_thumbnails()

    def rotate(self, angle):
        if self.current_page_index == -1: return
        self.save_state()
        self.pages[self.current_page_index]['rotation'] = (self.pages[self.current_page_index]['rotation'] + angle) % 360
        self.apply_modifications(self.current_page_index)

    def toggle_flip_h(self):
        if self.current_page_index == -1: return
        self.save_state()
        self.pages[self.current_page_index]['flip_h'] = not self.pages[self.current_page_index]['flip_h']
        self.apply_modifications(self.current_page_index)

    def toggle_flip_v(self):
        if self.current_page_index == -1: return
        self.save_state()
        self.pages[self.current_page_index]['flip_v'] = not self.pages[self.current_page_index]['flip_v']
        self.apply_modifications(self.current_page_index)

    def update_brightness(self, val):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['brightness'] = float(val)
        self.apply_modifications(self.current_page_index)

    def update_contrast(self, val):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['contrast'] = float(val)
        self.apply_modifications(self.current_page_index)

    def toggle_grayscale(self):
        if self.current_page_index == -1: return
        self.save_state()
        self.pages[self.current_page_index]['grayscale'] = self.gray_switch_editor.get() == 1
        self.apply_modifications(self.current_page_index)

    def reset_edits(self, reload_ui=True, save_history=True):
        if self.current_page_index == -1: return
        if save_history: self.save_state()
        self.pages[self.current_page_index].update({'rotation':0, 'flip_h':False, 'flip_v':False, 'brightness':1.0, 'contrast':1.0, 'grayscale':False})
        if reload_ui: self.sync_editor_controls()
        self.apply_modifications(self.current_page_index)

    # --- Scanning ---
    def perform_scan(self):
        self.log_status("Scanning...")
        # Show animated progress
        self.progress_bar.animate_to(0.3, duration=300)
        self.loading_spinner.pack(side="left", padx=10)
        self.loading_spinner.start()
        
        try:
            new_img = self.scanner_service.scan_document()
            if new_img:
                # Animate progress to completion
                self.progress_bar.animate_to(0.7, duration=200)
                
                if ImageProcessor.detect_blank_page(new_img):
                    self.show_toast("Blank page skipped", "warning")
                    self.log_status("⚠️ Blank page skipped")
                    return
                
                self.pages.append(self.create_page_data(new_img))
                self.select_page(len(self.pages) - 1)
                self.page_badge.configure(text=str(len(self.pages)))
                
                # Complete progress
                self.progress_bar.animate_to(1.0, duration=200)
                self.show_toast("Page added successfully!", "success")
                self.log_status("✅ Page added")
            else: 
                self.show_toast("Scan cancelled", "info")
                self.log_status("Scan cancelled")
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")
            self.show_toast("Scan failed", "error")
            self.log_status("❌ Scan failed")
        finally:
            self.loading_spinner.stop()
            self.loading_spinner.pack_forget()
            # Reset progress after delay
            self.after(1000, lambda: self.progress_bar.animate_to(0, duration=300))

    def start_batch_scan(self):
        if self.batch_scanning: self.stop_batch_scan(); return
        
        def start_batch(res):
            try:
                self.batch_target = int(res)
                self.batch_count = 0
                self.batch_scanning = True
                self.batch_scan_btn.configure(text="⏹️ Stop", fg_color=COLORS["danger"])
                self.scan_btn.configure(state="disabled")
                self.show_thumbnails()
                self.after(500, self.do_batch_scan)
            except: 
                messagebox.showerror("Error", "Invalid number")

        panel = TextInputPanel(self.sidebar_content, "Batch Scan", start_batch, prompt_text="Pages to scan (0 = continuous):", close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Batch Setup")

    def do_batch_scan(self):
        if not self.batch_scanning: return
        if self.batch_target > 0 and self.batch_count >= self.batch_target:
            self.stop_batch_scan()
            messagebox.showinfo("Done", f"Scanned {self.batch_count} pages")
            return
        self.log_status(f"Scanning {self.batch_count+1}...")
        try:
            img = self.scanner_service.scan_document()
            if img:
                self.pages.append(self.create_page_data(img))
                self.batch_count += 1
                self.select_page(len(self.pages) - 1)
                self.page_badge.configure(text=str(len(self.pages)))
                self.after(self.batch_delay, self.do_batch_scan)
            else: self.stop_batch_scan()
        except: self.stop_batch_scan()

    def stop_batch_scan(self):
        self.batch_scanning = False
        self.batch_scan_btn.configure(text="📚 Batch Scan", fg_color="transparent")
        self.scan_btn.configure(state="normal")
        self.batch_status.configure(text="")

    # --- Mouse / Cropping ---
    def toggle_crop_mode(self):
        if self.current_page_index == -1: return
        self.cropping_active = not self.cropping_active
        self.preview_canvas.configure(cursor="cross" if self.cropping_active else "")
        if not self.cropping_active: self.preview_canvas.delete("crop_rect")

    def on_mouse_down(self, event):
        if self.cropping_active: 
            self.crop_start = (event.x, event.y)
        else:
            # Prepare for panning
            self.preview_canvas.scan_mark(event.x, event.y)

    def on_mouse_drag(self, event):
        if self.cropping_active and self.crop_start:
            self.preview_canvas.delete("crop_rect")
            self.preview_canvas.create_rectangle(self.crop_start[0], self.crop_start[1], event.x, event.y, outline="red", width=2, tags="crop_rect")
        else:
            # Panning logic
            self.preview_canvas.scan_dragto(event.x, event.y, gain=1)

    def on_mouse_release(self, event):
        if self.cropping_active and self.crop_start:
            self.crop_end = (event.x, event.y)
            if messagebox.askyesno("Crop", "Apply crop?"): self.perform_crop()
            self.preview_canvas.delete("crop_rect")
            self.crop_start = None

    def perform_crop(self):
        self.save_state()
        cw, ch = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        img = self.pages[self.current_page_index]['processed']
        dw, dh = img.width * self.display_scale, img.height * self.display_scale
        ox, oy = (cw - dw)/2, (ch - dh)/2
        x1 = (min(self.crop_start[0], self.crop_end[0]) - ox) / self.display_scale
        y1 = (min(self.crop_start[1], self.crop_end[1]) - oy) / self.display_scale
        x2 = (max(self.crop_start[0], self.crop_end[0]) - ox) / self.display_scale
        y2 = (max(self.crop_start[1], self.crop_end[1]) - oy) / self.display_scale
        cropped = img.crop((int(x1), int(y1), int(x2), int(y2)))
        self.pages[self.current_page_index]['original'] = cropped.copy()
        self.reset_edits(reload_ui=False, save_history=False)
        self.toggle_crop_mode()

    # --- AI Tools ---
    def perspective_fix(self):
        if self.current_page_index == -1: return
        self.save_state()
        try:
            img = self.pages[self.current_page_index]['processed']
            res = ImageProcessor.automatic_document_transform(img)
            self.pages[self.current_page_index]['original'] = res
            self.reset_edits(reload_ui=False, save_history=False)
        except: messagebox.showerror("Error", "Perspective fix failed")

    def clean_document(self):
        if self.current_page_index == -1: return
        self.save_state()
        try:
            img = self.pages[self.current_page_index]['processed']
            res = ImageProcessor.enhance_document_text(img)
            self.pages[self.current_page_index]['processed'] = res
            self.display_page(res)
        except: pass

    # --- OpenAI Features ---
    def open_openai_settings(self):
        panel = OpenAISettingsPanel(self.sidebar_content, self.openai_service, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Settings")

    def perform_ocr(self):
        if self.current_page_index == -1: return
        
        def run():
            self.log_status("⏳ Extracting text...")
            text = self.openai_service.extract_text_ocr(self.pages[self.current_page_index]['processed'])
            self.after(0, lambda: self.show_ocr_result(text))
            self.after(0, lambda: self.log_status("✅ Text extracted"))
        
        threading.Thread(target=run, daemon=True).start()

    def show_ocr_result(self, text):
        panel = TextResultPanel(self.sidebar_content, "EXTRACTED TEXT", text, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "OCR Results")

    def perform_smart_rename(self):
        if self.current_page_index == -1: return
        
        def run():
            self.log_status("⏳ Generating name...")
            name = self.openai_service.smart_rename(self.pages[self.current_page_index]['processed'])
            self.after(0, lambda: self.apply_rename(name))
        
        threading.Thread(target=run, daemon=True).start()

    def apply_rename(self, name):
        self.log_status(f"Renamed to: {name}")
        # Here we might update a label or actually rename a file if it was saved
        messagebox.showinfo("Smart Rename", f"Suggested Filename:\n\n{name}")
        self.filename_prefix.set(name)

    def perform_analysis(self):
        if self.current_page_index == -1: return
        
        def run():
            self.log_status("⏳ Analyzing document...")
            result = self.openai_service.analyze_document(self.pages[self.current_page_index]['processed'])
            self.after(0, lambda: self.show_analysis_result(result))
            self.after(0, lambda: self.log_status("✅ Analysis complete"))
        
        threading.Thread(target=run, daemon=True).start()

    def show_analysis_result(self, text):
        panel = TextResultPanel(self.sidebar_content, "DOCUMENT ANALYSIS", text, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Analysis")
        
    # --- Resizing Logic ---
    def start_resize(self, event):
        self.resize_start_x = event.x_root

    def do_resize(self, event):
        dx = self.resize_start_x - event.x_root
        new_width = self.current_sidebar_width + dx
        
        if 200 <= new_width <= 600:
            self.right_sidebar.configure(width=new_width)
            self.current_sidebar_width = new_width # Update tracking
            self.resize_start_x = event.x_root # Reset for continuous delta


    def open_chat_window(self):
        # Callback to get current page
        def get_page():
            if self.current_page_index != -1 and self.current_page_index < len(self.pages):
                return self.pages[self.current_page_index]['processed']
            return None
            
        # Check if chat is already open in sidebar?
        # For now, just create new instance
        panel = AIChatWindow(self.sidebar_content, self.openai_service, get_page, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "AI Chat")

    def privacy_blur(self):
        if self.current_page_index == -1: return
        self.save_state()
        try:
            img = self.pages[self.current_page_index]['processed']
            res = ImageProcessor.redact_faces(img)
            self.pages[self.current_page_index]['processed'] = res
            self.display_page(res)
        except: pass

    def auto_straighten(self):
        if self.current_page_index == -1: return
        self.save_state()
        try:
            img = self.pages[self.current_page_index]['processed']
            res = ImageProcessor.deskew_image(img)
            self.pages[self.current_page_index]['original'] = res
            self.reset_edits(reload_ui=False, save_history=False)
        except: pass

    def resize_to_paper_size(self):
        """Resize current page to selected paper size"""
        if self.current_page_index == -1:
            messagebox.showwarning("No Page", "Please scan a page first")
            return
        
        selected = self.paper_size_var.get()
        size = self.paper_sizes.get(selected)
        
        if size is None:
            messagebox.showwarning("No Size", "Please select a valid paper size first")
            return
        
        target_w, target_h = size
        current_img = self.pages[self.current_page_index]['processed']
        
        # Ask user for resize method
        choice = messagebox.askquestion(
            "Resize Method",
            f"Resize to {selected}?\n\nChoose method:\n• Yes = Fit (maintain aspect ratio)\n• No = Crop to center",
            icon='question'
        )
        
        if choice == 'yes':
            # Fit - maintain aspect ratio
            img_copy = current_img.copy()
            img_copy.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            new_img = Image.new('RGB', (target_w, target_h), 'white')
            paste_x = (target_w - img_copy.width) // 2
            paste_y = (target_h - img_copy.height) // 2
            new_img.paste(img_copy, (paste_x, paste_y))
        else:
            # Crop center
            img_w, img_h = current_img.size
            left = max(0, (img_w - target_w) // 2)
            top = max(0, (img_h - target_h) // 2)
            right = min(img_w, left + target_w)
            bottom = min(img_h, top + target_h)
            cropped = current_img.crop((left, top, right, bottom))
            if cropped.size != (target_w, target_h):
                new_img = Image.new('RGB', (target_w, target_h), 'white')
                paste_x = (target_w - cropped.width) // 2
                paste_y = (target_h - cropped.height) // 2
                new_img.paste(cropped, (paste_x, paste_y))
            else:
                new_img = cropped
        
        self.pages[self.current_page_index]['original'] = new_img
        self.pages[self.current_page_index]['processed'] = new_img.copy()
        self.reset_edits(reload_ui=False, save_history=False)
        self.apply_modifications(self.current_page_index)
        self.log_status(f"Resized to {selected}")

    # --- Annotate ---
    # --- Annotate ---
    def open_text_dialog(self):
        if self.current_page_index == -1: return
        
        def apply(txt):
            img = ImageProcessor.add_text(self.pages[self.current_page_index]['processed'], txt, (50,50))
            self.pages[self.current_page_index]['original'] = img
            self.reset_edits(reload_ui=False)
            self.show_thumbnails()

        panel = TextInputPanel(self.sidebar_content, "Add Text", apply, prompt_text="Enter text to add:", close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Annotate")

    def apply_watermark(self):
        if self.current_page_index == -1: return
        img = self.pages[self.current_page_index]['processed']
        res = ImageProcessor.add_watermark(img, self.watermark_text.get(), self.watermark_position.get())
        self.pages[self.current_page_index]['original'] = res
        self.reset_edits(reload_ui=False)

    # --- Layout ---
    def split_current_page(self):
        if self.current_page_index == -1: return
        img = self.pages[self.current_page_index]['processed']
        l, r = ImageProcessor.split_image_vertical(img)
        self.pages[self.current_page_index] = self.create_page_data(l)
        self.pages.insert(self.current_page_index+1, self.create_page_data(r))
        self.select_page(self.current_page_index)

    # --- Help & Guide ---
    def show_help_guide(self):
        panel = HelpPanel(self.sidebar_content, self.guide_service, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Help Guide")

    # --- Undo / Redo ---
    def save_state(self):
        """Save current page state to undo stack before a change"""
        if self.current_page_index == -1: return
        p = self.pages[self.current_page_index]
        # Store state as a dict snapshot
        state = {
            'original': p['original'].copy(),
            'rotation': p['rotation'],
            'flip_h': p['flip_h'],
            'flip_v': p['flip_v'],
            'brightness': p['brightness'],
            'contrast': p['contrast'],
            'grayscale': p['grayscale']
        }
        p['undo_stack'].append(state)
        # Limit stack size to save memory
        if len(p['undo_stack']) > 20:
            p['undo_stack'].pop(0)
        # Clear redo stack since we've made a new change
        p['redo_stack'].clear()

    def undo(self):
        if self.current_page_index == -1: return
        p = self.pages[self.current_page_index]
        if not p['undo_stack']: 
            self.log_status("Nothing to undo")
            return
        
        # Save current state to redo stack
        current_state = {
            'original': p['original'].copy(),
            'rotation': p['rotation'],
            'flip_h': p['flip_h'],
            'flip_v': p['flip_v'],
            'brightness': p['brightness'],
            'contrast': p['contrast'],
            'grayscale': p['grayscale']
        }
        p['redo_stack'].append(current_state)
        
        # Restore last state
        last_state = p['undo_stack'].pop()
        p.update(last_state)
        # We need to make sure we don't just reference the image
        p['original'] = last_state['original'].copy()
        
        self.apply_modifications(self.current_page_index)
        self.sync_editor_controls()
        self.log_status("Undo performed")

    def redo(self):
        if self.current_page_index == -1: return
        p = self.pages[self.current_page_index]
        if not p['redo_stack']:
            self.log_status("Nothing to redo")
            return
            
        # Save current state to undo stack
        current_state = {
            'original': p['original'].copy(),
            'rotation': p['rotation'],
            'flip_h': p['flip_h'],
            'flip_v': p['flip_v'],
            'brightness': p['brightness'],
            'contrast': p['contrast'],
            'grayscale': p['grayscale']
        }
        p['undo_stack'].append(current_state)
        
        # Restore next state
        next_state = p['redo_stack'].pop()
        p.update(next_state)
        p['original'] = next_state['original'].copy()
        
        self.apply_modifications(self.current_page_index)
        self.sync_editor_controls()
        self.log_status("Redo performed")

    def reverse_pages(self):
        self.pages.reverse(); self.select_page(0)

    def create_collage_grid(self):
        if len(self.pages) < 2: return
        cols, rows = map(int, self.grid_layout_var.get().split('x'))
        res = ImageProcessor.create_photo_grid([p['processed'] for p in self.pages], f"{cols}x{rows}")
        self.pages.append(self.create_page_data(res))
        self.select_page(len(self.pages)-1)

    # --- Library / Export ---
    def save_as_image(self):
        if self.current_page_index == -1: return
        folder = self.output_dir.get()
        if not os.path.exists(folder): os.makedirs(folder)
        path = os.path.join(folder, f"{self.filename_prefix.get()}_{self.current_page_index+1}.jpg")
        self.pages[self.current_page_index]['processed'].save(path, "JPEG")
        self.db_service.add_scan_history(os.path.basename(path), path, "JPEG", 1, os.path.getsize(path))
        messagebox.showinfo("Saved", f"Saved to {path}")

    def save_as_pdf(self):
        if not self.pages: return
        folder = self.output_dir.get()
        if not os.path.exists(folder): os.makedirs(folder)
        path = os.path.join(folder, f"{self.filename_prefix.get()}.pdf")
        imgs = [p['processed'].convert("RGB") for p in self.pages]
        imgs[0].save(path, "PDF", save_all=True, append_images=imgs[1:])
        self.db_service.add_scan_history(os.path.basename(path), path, "PDF", len(self.pages), os.path.getsize(path))
        messagebox.showinfo("Saved", f"PDF saved to {path}")

    def show_scan_history(self):
        panel = HistoryPanel(self.sidebar_content, self.db_service, close_callback=self.show_thumbnails)
        self.switch_sidebar_to(panel, "Scan History")

    def open_output_folder(self):
        if os.path.exists(self.output_dir.get()): os.startfile(self.output_dir.get())

    def clear_history_confirm(self):
        if messagebox.askyesno("Clear", "Clear history logs?"): self.db_service.clear_scan_history()

    def preview_pdf(self):
        if not self.pages: return
        try:
            path = os.path.join(os.environ.get('TEMP', '.'), "preview.pdf")
            imgs = [p['processed'].convert("RGB") for p in self.pages]
            imgs[0].save(path, "PDF", save_all=True, append_images=imgs[1:])
            os.startfile(path)
        except: pass

    def print_document(self):
        if not self.pages: return
        try:
            path = os.path.join(os.environ.get('TEMP', '.'), "print.pdf")
            imgs = [p['processed'].convert("RGB") for p in self.pages]
            imgs[0].save(path, "PDF", save_all=True, append_images=imgs[1:])
            os.startfile(path, "print")
        except: pass

    def delete_current_page(self):
        if self.current_page_index != -1:
            self.pages.pop(self.current_page_index)
            if not self.pages: self.current_page_index = -1; self.preview_canvas.delete("all")
            else: self.select_page(max(0, self.current_page_index-1))
            self.page_badge.configure(text=str(len(self.pages)))

    def clear_all_pages(self):
        if messagebox.askyesno("Clear", "Clear all pages?"):
            self.pages = []; self.current_page_index = -1; self.preview_canvas.delete("all"); self.page_badge.configure(text="0")

    def log_status(self, msg):
        self.status_label.configure(text=f"ℹ️ {msg}"); self.update_idletasks()
    
    def show_toast(self, message, type="info"):
        """Show a toast notification"""
        toast = ToastNotification(self, message, type=type)
        toast.show()
    
    def show_loading(self, message="Processing..."):
        """Show loading overlay"""
        self.loading_overlay.update_message(message)
        self.loading_overlay.show()
    
    def hide_loading(self):
        """Hide loading overlay"""
        self.loading_overlay.hide()

    def browse_folder(self):
        f = filedialog.askdirectory()
        if f: self.output_dir.set(f)

    def on_paper_size_change(self, choice):
        if choice == "Custom...":
            def set_custom_size(res):
                if res and 'x' in res:
                    try:
                        w, h = map(int, res.split('x'))
                        self.paper_sizes["Custom..."] = (w, h)
                        self.show_thumbnails()
                    except: pass
            
            panel = TextInputPanel(self.sidebar_content, "Custom Size", set_custom_size, prompt_text="Width x Height (px):", close_callback=self.show_thumbnails)
            self.switch_sidebar_to(panel, "Paper Setup")
