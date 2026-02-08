import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageTk
from scanner_utils import ScannerService
from image_utils import ImageProcessor
from database_utils import DatabaseService
from guide_utils import GuideService
import webbrowser

# Premium Cockpit-Style Theme
COLORS = {
    "bg_gradient_start": "#EEF2FF",
    "bg_gradient_end": "#E0E7FF", 
    "surface": "#FFFFFF",
    "primary": "#3B82F6",
    "primary_dark": "#2563EB",
    "primary_light": "#93C5FD",
    "secondary": "#8B5CF6",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "text": "#1E293B",
    "text_light": "#64748B",
    "text_lighter": "#94A3B8",
    "border": "#E2E8F0",
    "shadow": "#00000010"
}

ctk.set_appearance_mode("Light")

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Services
        self.db_service = DatabaseService()
        self.scanner_service = ScannerService()
        self.guide_service = GuideService()

        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Scans")
        saved_dir = self.db_service.get_setting("output_dir", default_dir)
        saved_prefix = self.db_service.get_setting("filename_prefix", "Scan")

        self.title("InerScan Pro")
        self.geometry("1280x800")
        self.configure(fg_color=COLORS["bg_gradient_start"])

        # Variables
        self.pages = []
        self.current_page_index = -1
        self.cropping_active = False
        self.crop_start = None
        self.crop_end = None
        self.tk_image_ref = None
        self.display_image_ref = None
        self.display_scale = 1.0
        self.output_dir = tk.StringVar(value=saved_dir)
        self.filename_prefix = tk.StringVar(value=saved_prefix)
        
        self.output_dir.trace_add("write", lambda *args: self.db_service.save_setting("output_dir", self.output_dir.get()))
        self.filename_prefix.trace_add("write", lambda *args: self.db_service.save_setting("filename_prefix", self.filename_prefix.get()))

        # Tab state
        self.current_tab = "scanner"

        # Batch scanning state
        self.batch_scanning = False
        self.batch_count = 0
        self.batch_target = 0
        self.batch_delay = 2000  # ms between scans

        self.init_ui()

    def init_ui(self):
        # Main container with padding
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(1, weight=1)
        
        # Top Navigation Pills
        nav_frame = ctk.CTkFrame(main, fg_color=COLORS["surface"], corner_radius=50, height=60)
        nav_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        nav_frame.grid_propagate(False)
        
        nav_inner = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_inner.pack(expand=True)
        
        # Navigation buttons with commands
        self.nav_buttons = {}
        tabs = [("scanner", "📄 Scanner"), ("editor", "🎨 Editor"), ("library", "📚 Library")]
        
        for tab_id, text in tabs:
            btn = ctk.CTkButton(nav_inner, text=text, width=140, height=40, corner_radius=25,
                               command=lambda t=tab_id: self.switch_tab(t),
                               fg_color=COLORS["primary"] if tab_id == "scanner" else "transparent",
                               hover_color=COLORS["primary_light"],
                               text_color="white" if tab_id == "scanner" else COLORS["text_light"],
                               font=("Segoe UI", 13, "bold"))
            btn.pack(side="left", padx=5)
            self.nav_buttons[tab_id] = btn
        
        # Left Panel - Controls Card
        self.left_card = self._create_card(main, 320)
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        self.scroll = ctk.CTkScrollableFrame(self.left_card, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create all sections (we'll show/hide based on tab)
        self.create_scanner_controls()
        self.create_editor_controls()
        self.create_library_controls()
        
        # Show only scanner controls by default
        self.show_tab_controls("scanner")

    def create_scanner_controls(self):
        """Create Scanner tab controls"""
        self.scanner_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        
        # Scan Button with Badge
        scan_frame = ctk.CTkFrame(self.scanner_frame, fg_color="transparent")
        scan_frame.pack(fill="x", pady=(0, 10))
        
        self.scan_btn = ctk.CTkButton(scan_frame, text="🚀 Start Scan", height=50, corner_radius=12,
                                     fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
                                     font=("Segoe UI", 15, "bold"), command=self.perform_scan)
        self.scan_btn.pack(fill="x")
        
        # Batch Scan Button
        self.batch_scan_btn = ctk.CTkButton(scan_frame, text="📚 Batch Scan", height=50, corner_radius=12,
                                           fg_color="#10B981", hover_color="#059669",
                                           font=("Segoe UI", 15, "bold"), command=self.start_batch_scan)
        self.batch_scan_btn.pack(fill="x", pady=(10, 0))
        
        # Batch status label
        self.batch_status = ctk.CTkLabel(scan_frame, text="", font=("Segoe UI", 10),
                                        text_color=COLORS["text_light"])
        self.batch_status.pack(pady=(5, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self.scanner_frame, height=8, corner_radius=4, 
                                               progress_color=COLORS["success"])
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(5, 20))
        
        # Tools Section
        self._section_header(scroll, "✨ Image Tools")
        
        # Tool Grid
        tool_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tool_frame.pack(fill="x", pady=(0, 15))
        tool_frame.grid_columnconfigure((0, 1), weight=1)
        
        tools = [
            ("↺ Rotate L", lambda: self.rotate(-90)),
            ("↻ Rotate R", lambda: self.rotate(90)),
            ("↔ Flip H", self.toggle_flip_h),
            ("↕ Flip V", self.toggle_flip_v)
        ]
        
        for i, (text, cmd) in enumerate(tools):
            btn = ctk.CTkButton(tool_frame, text=text, command=cmd, height=40,  corner_radius=10,
                               fg_color=COLORS["bg_gradient_end"], text_color=COLORS["text"],
                               hover_color=COLORS["border"], font=("Segoe UI", 12))
            btn.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
        
        # Sliders with labels
        self._slider_control(scroll, "💡 Brightness", self.update_brightness)
        self.bright_slider = scroll.winfo_children()[-1]
        self.bright_slider.set(1.0)
        
        self._slider_control(scroll, "🎭 Contrast", self.update_contrast)
        self.cont_slider = scroll.winfo_children()[-1]
        self.cont_slider.set(1.0)
        
        # Advanced Actions
        self._section_header(scroll, "🔧 Advanced")
        
        actions = [
            ("📐 Auto-Straighten", self.auto_straighten, "#06B6D4"),
            ("✂️ Crop Tool", self.toggle_crop_mode, COLORS["warning"]),
            ("🧹 Remove Background", self.remove_white_bg, COLORS["secondary"]),
            ("📐 Auto Crop", self.perform_auto_crop, COLORS["success"])
        ]
        
        for text, cmd, color in actions:
            self._action_button(scroll, text, cmd, color)
        
        self.gray_switch = ctk.CTkSwitch(scroll, text="⚫ Black & White", 
                                        command=self.toggle_grayscale, font=("Segoe UI", 12))
        self.gray_switch.pack(anchor="w", pady=(10, 20))
        
        # Watermark / Stamp Section
        self._section_header(scroll, "🏷️ Watermark / Stamp")
        
        # Watermark text templates
        self.watermark_text = tk.StringVar(value="COPY")
        watermark_templates = ["COPY", "DRAFT", "CONFIDENTIAL", "APPROVED", 
                              "SAMPLE", "VOID", "ORIGINAL", "Custom..."]
        
        watermark_menu = ctk.CTkOptionMenu(scroll, variable=self.watermark_text,
                                          values=watermark_templates,
                                          command=self.on_watermark_template_change,
                                          height=38, corner_radius=10,
                                          fg_color=COLORS["surface"], 
                                          button_color="#DC2626",
                                          button_hover_color="#B91C1C",
                                          dropdown_fg_color=COLORS["surface"],
                                          font=("Segoe UI", 12))
        watermark_menu.pack(fill="x", pady=(0, 10))
        
        # Watermark position
        self.watermark_position = tk.StringVar(value="center")
        position_options = ["center", "top-right", "bottom-right", "top-left", "bottom-left"]
        
        position_menu = ctk.CTkOptionMenu(scroll, variable=self.watermark_position,
                                         values=position_options,
                                         height=38, corner_radius=10,
                                         fg_color=COLORS["surface"],
                                         button_color=COLORS["text_light"],
                                         dropdown_fg_color=COLORS["surface"],
                                         font=("Segoe UI", 11))
        position_menu.pack(fill="x", pady=(0, 10))
        
        # Watermark opacity slider
        self._slider_control(scroll, "💧 Opacity", self.update_watermark_preview)
        self.watermark_opacity_slider = scroll.winfo_children()[-1]
        self.watermark_opacity_slider.set(0.5)  # 50% opacity
        
        # Apply watermark button
        ctk.CTkButton(scroll, text="🏷️ Add Watermark", command=self.apply_watermark,
                     height=40, corner_radius=10, fg_color="#DC2626",
                     hover_color="#B91C1C", font=("Segoe UI", 12, "bold")).pack(fill="x", pady=(0, 20))
        
        # Paper Size Section
        self._section_header(scroll, "📏 Paper Size")
        
        self.paper_sizes = {
            # A-Series (ISO 216)
            "A0 (841×1189mm)": (9933, 14043),
            "A1 (594×841mm)": (7016, 9933),
            "A2 (420×594mm)": (4961, 7016),
            "A3 (297×420mm)": (3508, 4961),
            "A4 (210×297mm)": (2480, 3508),
            "A5 (148×210mm)": (1748, 2480),
            "A6 (105×148mm)": (1240, 1748),
            
            # B-Series (ISO 216)
            "B4 (250×353mm)": (2953, 4169),
            "B5 (176×250mm)": (2079, 2953),
            
            # North American Sizes
            "Letter (8.5×11in)": (2550, 3300),
            "Legal (8.5×14in)": (2550, 4200),
            "Executive (7.25×10.5in)": (2175, 3150),
            "Ledger/Tabloid (11×17in)": (3300, 5100),
            "Folio (8.5×13in)": (2550, 3900),
            
            # Photo Sizes
            "Photo 3×5 (3×5in)": (900, 1500),
            "Photo 4×6 (4×6in)": (1204, 1795),
            "Photo 5×7 (5×7in)": (1500, 2100),
            "Photo 8×10 (8×10in)": (2400, 3000),
            
            # Card Sizes
            "Business Card (3.5×2in)": (1050, 600),
            "ATM/Credit Card": (1011, 638),
            "ID Card (85.6×53.98mm)": (1011, 637),
            "Passport Photo (35×45mm)": (413, 531),
            
            # Custom
            "Custom...": None
        }
        
        self.paper_size_var = tk.StringVar(value="A4 (210×297mm)")
        
        size_menu = ctk.CTkOptionMenu(scroll, variable=self.paper_size_var,
                                      values=list(self.paper_sizes.keys()),
                                      command=self.on_paper_size_change,
                                      height=38, corner_radius=10,
                                      fg_color=COLORS["surface"], button_color=COLORS["primary"],
                                      button_hover_color=COLORS["primary_dark"],
                                      dropdown_fg_color=COLORS["surface"],
                                      font=("Segoe UI", 12))
        size_menu.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(scroll, text="✂️ Resize to Selected", command=self.resize_to_paper_size,
                     height=40, corner_radius=10, fg_color="#0891B2",
                     hover_color="#0E7490", font=("Segoe UI", 12, "bold")).pack(fill="x", pady=(0, 20))
        
        # Book Tools
        self._section_header(scroll, "📚 Book & Duplex")
        book_actions = [
            ("Split Page (L/R)", self.split_current_page),
            ("Reverse Order", self.reverse_pages),
            ("Interleave Stacks", self.interleave_pages)
        ]
        for text, cmd in book_actions:
            self._action_button(scroll, text, cmd, "#6366F1")
        
        # Collage & Photo Grid
        self._section_header(scroll, "🎨 Collage & Photo Grid")
        
        self.grid_layout_var = tk.StringVar(value="2x2")
        grid_layouts = ["1x2", "2x1", "2x2", "3x2", "2x3", "3x3", "4x4"]
        
        grid_menu = ctk.CTkOptionMenu(scroll, variable=self.grid_layout_var,
                                      values=grid_layouts, height=38, corner_radius=10,
                                      fg_color=COLORS["surface"], button_color=COLORS["secondary"],
                                      button_hover_color="#7C3AED",
                                      dropdown_fg_color=COLORS["surface"],
                                      font=("Segoe UI", 12))
        grid_menu.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(scroll, text="🖼️ Create Grid from All Pages", 
                     command=self.create_collage_grid, height=40, corner_radius=10,
                     fg_color="#EC4899", hover_color="#DB2777",
                     font=("Segoe UI", 12, "bold")).pack(fill="x", pady=(0, 20))
        
        # Export
        self._section_header(scroll, "💾 Export")
        
        self._input_field(scroll, "Filename", self.filename_prefix)
        self._input_field(scroll, "Location", self.output_dir)
        
        ctk.CTkButton(scroll, text="📁 Browse...", command=self.browse_folder, height=36,
                     fg_color="transparent", border_width=2, border_color=COLORS["border"],
                     text_color=COLORS["text"], hover_color=COLORS["bg_gradient_end"],
                     corner_radius=10, font=("Segoe UI", 11)).pack(fill="x", pady=(0, 15))
        
        self.save_img_btn = ctk.CTkButton(scroll, text="🖼️ Save as Image", 
                                         command=self.save_as_image, state="disabled",
                                         height=45, corner_radius=12, fg_color=COLORS["primary"],
                                         font=("Segoe UI", 13, "bold"))
        self.save_img_btn.pack(fill="x", pady=3)
        
        self.save_pdf_btn = ctk.CTkButton(scroll, text="📄 Save as PDF",
                                         command=self.save_as_pdf, state="disabled",
                                         height=45, corner_radius=12, fg_color=COLORS["primary"],
                                         font=("Segoe UI", 13, "bold"))
        self.save_pdf_btn.pack(fill="x", pady=(3, 20))
        
        # History & File Manager
        self._section_header(scroll, "📂 History & Files")
        
        history_actions = [
            ("📜 View Scan History", self.show_scan_history),
            ("📁 Open File Location", self.open_output_folder),
            ("🗑️ Clear History", self.clear_history_confirm)
        ]
        
        for text, cmd in history_actions:
            ctk.CTkButton(scroll, text=text, command=cmd, height=38, corner_radius=10,
                         fg_color="transparent", border_width=2, border_color=COLORS["border"],
                         text_color=COLORS["text"], hover_color=COLORS["bg_gradient_end"],
                         font=("Segoe UI", 11)).pack(fill="x", pady=3)
        
        # About
        self._section_header(scroll, "ℹ️ About")
        ctk.CTkLabel(scroll, text="Developed by Ilham Maulana", 
                    font=("Segoe UI", 11), text_color=COLORS["text"], anchor="w").pack(fill="x")
        ctk.CTkLabel(scroll, text="k4ilham@gmail.com",
                    font=("Segoe UI", 10), text_color=COLORS["text_light"], anchor="w").pack(fill="x")
        
        link = ctk.CTkLabel(scroll, text="🌐 inercorp.com", font=("Segoe UI", 11, "underline"),
                           text_color=COLORS["primary"], cursor="hand2", anchor="w")
        link.pack(fill="x", pady=(3, 10))
        link.bind("<Button-1>", lambda e: webbrowser.open("https://inercorp.com"))
        
        ctk.CTkButton(scroll, text="🎧 User Guide", command=self.start_interactive_guide,
                     height=40, corner_radius=10, fg_color=COLORS["secondary"],
                     font=("Segoe UI", 12, "bold")).pack(fill="x")
        
        # Center Preview Card
        center_card = self._create_card(main, min_width=500)
        center_card.grid(row=1, column=1, sticky="nsew", padx=5)
        center_card.grid_rowconfigure(0, weight=1)
        center_card.grid_columnconfigure(0, weight=1)
        
        self.preview_canvas = tk.Canvas(center_card, bg="#FAFBFC", highlightthickness=0)
        self.preview_canvas.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.preview_canvas.bind("<Button-1>", self.on_mouse_down)
        self.preview_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.preview_canvas.create_text(400, 300, text="📄 No Document\n\nClick 'Start Scan' to begin",
                                       fill=COLORS["text_lighter"], font=("Segoe UI", 18), 
                                       tags="placeholder", justify="center")
        
        # Right Panel - Pages Card
        right_card = self._create_card(main, 280)
        right_card.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
        right_card.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(right_card, fg_color="transparent", height=50)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        header.grid_propagate(False)
        
        ctk.CTkLabel(header, text="📑 Pages", font=("Segoe UI", 16, "bold"),
                    text_color=COLORS["text"]).pack(side="left")
        
        self.page_badge = ctk.CTkLabel(header, text="0", font=("Segoe UI", 11, "bold"),
                                      fg_color=COLORS["primary"], text_color="white",
                                      corner_radius=12, width=30, height=24)
        self.page_badge.pack(side="left", padx=10)
        
        self.thumb_scroll = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        self.thumb_scroll.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))
        
        self.delete_btn = ctk.CTkButton(right_card, text="🗑️ Delete", command=self.delete_current_page,
                                       state="disabled", height=45, corner_radius=12,
                                       fg_color=COLORS["danger"], font=("Segoe UI", 13, "bold"))
        self.delete_btn.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Status Bar
        status = ctk.CTkFrame(main, fg_color=COLORS["surface"], height=40, corner_radius=15)
        status.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        status.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(status, text="✅ Ready", font=("Segoe UI", 11),
                                        text_color=COLORS["text_light"], anchor="w")
        self.status_label.pack(side="left", padx=20)

    def _create_card(self, parent, width=300, min_width=None):
        """Create a card with shadow effect"""
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=16,
                           border_width=1, border_color=COLORS["border"])
        if min_width:
            card.grid_propagate(False)
        else:
            card.configure(width=width)
            card.grid_propagate(False)
        return card

    def _section_header(self, parent, text):
        """Create a section header with icon"""
        lbl = ctk.CTkLabel(parent, text=text, font=("Segoe UI", 13, "bold"),
                          text_color=COLORS["primary"], anchor="w")
        lbl.pack(fill="x", pady=(20, 10))

    def _action_button(self, parent, text, cmd, color):
        """Create an action button"""
        btn = ctk.CTkButton(parent, text=text, command=cmd, height=40, corner_radius=10,
                           fg_color=color, hover_color=color, font=("Segoe UI", 12))
        btn.pack(fill="x", pady=3)

    def _slider_control(self, parent, label, command):
        """Create a slider with label"""
        ctk.CTkLabel(parent, text=label, font=("Segoe UI", 12),
                    text_color=COLORS["text"], anchor="w").pack(fill="x", pady=(10, 3))
        slider = ctk.CTkSlider(parent, from_=0.5, to=2.0, command=command, height=18,
                              button_color=COLORS["primary"], progress_color=COLORS["primary_light"])
        slider.pack(fill="x", pady=(0, 5))

    def _input_field(self, parent, label, variable):
        """Create an input field with label"""
        ctk.CTkLabel(parent, text=label, font=("Segoe UI", 11),
                    text_color=COLORS["text_light"], anchor="w").pack(fill="x", pady=(0, 3))
        entry = ctk.CTkEntry(parent, textvariable=variable, height=38, corner_radius=10,
                            border_width=1, border_color=COLORS["border"])
        entry.pack(fill="x", pady=(0, 10))

    def switch_tab(self, tab_id):
        """Switch between Scanner, Editor, and Library tabs"""
        self.current_tab = tab_id
        
        # Update button styles
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.configure(fg_color=COLORS["primary"], text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_light"])
        
        # Switch UI controls
        self.show_tab_controls(tab_id)

    # Event Handlers (keeping existing logic)
    def log_status(self, msg):
        self.status_label.configure(text=f"ℹ️ {msg}")
        self.update_idletasks()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder: self.output_dir.set(folder)

    def perform_scan(self):
        self.log_status("Scanning...")
        self.progress_bar.start()
        try:
            new_img = self.scanner_service.scan_document()
            if new_img:
                page_data = {
                    'original': new_img.copy(), 'processed': new_img.copy(),
                    'rotation': 0, 'flip_h': False, 'flip_v': False,
                    'brightness': 1.0, 'contrast': 1.0, 'grayscale': False
                }
                self.pages.append(page_data)
                self.select_page(len(self.pages) - 1)
                self.save_img_btn.configure(state="normal")
                self.save_pdf_btn.configure(state="normal")
                self.delete_btn.configure(state="normal")
                self.page_badge.configure(text=str(len(self.pages)))
                self.log_status(f"Page {len(self.pages)} added")
            else:
                self.log_status("Scan cancelled")
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")
            self.log_status("Scan failed")
        finally:
            self.progress_bar.stop()
            self.progress_bar.set(0)

    def start_batch_scan(self):
        """Start batch scanning mode"""
        if self.batch_scanning:
            # Stop batch scanning
            self.stop_batch_scan()
            return
        
        # Dialog to configure batch scan
        dialog = ctk.CTkInputDialog(
            text="Batch Scan Settings\n\nEnter number of pages to scan:\n(Enter 0 for continuous until stopped)",
            title="Batch Scan Setup"
        )
        result = dialog.get_input()
        
        if result is None:
            return
        
        try:
            num_pages = int(result)
            if num_pages < 0:
                raise ValueError("Must be 0 or positive")
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid number (0 for continuous)")
            return
        
        self.batch_target = num_pages
        self.batch_count = 0
        self.batch_scanning = True
        
        # Update UI
        self.batch_scan_btn.configure(text="⏹️ Stop Batch", fg_color=COLORS["danger"])
        self.scan_btn.configure(state="disabled")
        
        if num_pages == 0:
            self.batch_status.configure(text="Continuous scan mode - Click Stop to end")
            self.log_status("Batch scan started (continuous)")
        else:
            self.batch_status.configure(text=f"Scanning 0/{num_pages} pages...")
            self.log_status(f"Batch scan started ({num_pages} pages)")
        
        # Start first scan
        self.after(500, self.do_batch_scan)

    def do_batch_scan(self):
        """Perform one scan in batch mode"""
        if not self.batch_scanning:
            return
        
        # Check if we've reached target (if not continuous)
        if self.batch_target > 0 and self.batch_count >= self.batch_target:
            self.stop_batch_scan()
            messagebox.showinfo("✅ Batch Complete", 
                              f"Successfully scanned {self.batch_count} page(s)!")
            return
        
        self.log_status(f"Scanning page {self.batch_count + 1}...")
        
        try:
            new_img = self.scanner_service.scan_document()
            if new_img:
                page_data = {
                    'original': new_img.copy(), 'processed': new_img.copy(),
                    'rotation': 0, 'flip_h': False, 'flip_v': False,
                    'brightness': 1.0, 'contrast': 1.0, 'grayscale': False
                }
                self.pages.append(page_data)
                self.batch_count += 1
                
                # Update UI
                self.select_page(len(self.pages) - 1)
                self.save_img_btn.configure(state="normal")
                self.save_pdf_btn.configure(state="normal")
                self.delete_btn.configure(state="normal")
                self.page_badge.configure(text=str(len(self.pages)))
                
                if self.batch_target == 0:
                    self.batch_status.configure(text=f"Scanned {self.batch_count} pages (continuous)")
                else:
                    self.batch_status.configure(text=f"Scanning {self.batch_count}/{self.batch_target} pages...")
                
                self.log_status(f"Page {self.batch_count} added")
                
                # Schedule next scan
                if self.batch_scanning:
                    self.after(self.batch_delay, self.do_batch_scan)
            else:
                # User cancelled scan
                self.stop_batch_scan()
                self.log_status("Batch scan stopped by user")
        
        except Exception as e:
            messagebox.showerror("Scan Error", f"Error during batch scan:\n{e}\n\nBatch scan stopped.")
            self.stop_batch_scan()

    def stop_batch_scan(self):
        """Stop batch scanning"""
        self.batch_scanning = False
        self.batch_scan_btn.configure(text="📚 Batch Scan", fg_color="#10B981")
        self.scan_btn.configure(state="normal")
        
        if self.batch_count > 0:
            self.batch_status.configure(text=f"✅ Completed: {self.batch_count} pages scanned")
            self.log_status(f"Batch scan completed - {self.batch_count} pages")
        else:
            self.batch_status.configure(text="")
            self.log_status("Batch scan cancelled")

    def process_image(self):
        if self.current_page_index == -1: return
        page = self.pages[self.current_page_index]
        page['processed'] = ImageProcessor.process_page(page)
        self.show_preview(page['processed'])
        self.update_thumbnails()

    def rotate(self, angle):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['rotation'] = (self.pages[self.current_page_index]['rotation'] + angle) % 360
        self.process_image()

    def toggle_flip_h(self):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['flip_h'] = not self.pages[self.current_page_index]['flip_h']
        self.process_image()

    def toggle_flip_v(self):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['flip_v'] = not self.pages[self.current_page_index]['flip_v']
        self.process_image()

    def update_brightness(self, value):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['brightness'] = float(value)
        self.process_image()

    def update_contrast(self, value):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['contrast'] = float(value)
        self.process_image()

    def toggle_grayscale(self):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index]['grayscale'] = self.gray_switch.get() == 1
        self.process_image()

    def remove_white_bg(self):
        if self.current_page_index == -1: return
        img = self.pages[self.current_page_index]['processed']
        new_img = ImageProcessor.remove_white_background(img)
        self.pages[self.current_page_index]['original'] = new_img
        self.reset_edits(reload_ui=False)
        self.process_image()

    def perform_auto_crop(self):
        if self.current_page_index == -1: return
        img = self.pages[self.current_page_index]['processed']
        if img.mode != 'RGBA':
            if messagebox.askyesno("Auto Crop", "Remove white background first?"):
                self.remove_white_bg()
                img = self.pages[self.current_page_index]['processed']
            else:
                return
        new_img = ImageProcessor.perform_auto_crop(img)
        self.pages[self.current_page_index]['original'] = new_img
        self.reset_edits(reload_ui=False)
        self.process_image()

    def reset_edits(self, reload_ui=True):
        if self.current_page_index == -1: return
        self.pages[self.current_page_index].update({
            'rotation': 0, 'flip_h': False, 'flip_v': False,
            'brightness': 1.0, 'contrast': 1.0, 'grayscale': False
        })
        if reload_ui:
            self.bright_slider.set(1.0)
            self.cont_slider.set(1.0)
            self.gray_switch.deselect()
            self.process_image()

    def toggle_crop_mode(self):
        if self.current_page_index == -1: return
        self.cropping_active = not self.cropping_active
        self.preview_canvas.config(cursor="crosshair" if self.cropping_active else "")
        if not self.cropping_active:
            self.preview_canvas.delete("crop_rect")

    def on_mouse_down(self, event):
        if not self.cropping_active: return
        self.crop_start = (event.x, event.y)
        self.preview_canvas.delete("crop_rect")

    def on_mouse_drag(self, event):
        if not self.cropping_active or not self.crop_start: return
        self.preview_canvas.delete("crop_rect")
        self.preview_canvas.create_rectangle(
            self.crop_start[0], self.crop_start[1], event.x, event.y,
            outline=COLORS["primary"], width=3, dash=(8, 4), tags="crop_rect")

    def on_mouse_release(self, event):
        if not self.cropping_active or not self.crop_start: return
        self.crop_end = (event.x, event.y)
        if messagebox.askyesno("Crop", "Apply this crop?"):
            self.apply_crop()
        else:
            self.preview_canvas.delete("crop_rect")

    def auto_straighten(self):
        """Automatically straighten skewed/tilted images"""
        if self.current_page_index == -1:
            messagebox.showwarning("No Page", "Please scan a page first.")
            return
        
        # Ask user preferences
        response = messagebox.askyesnocancel(
            "Auto-Straighten", 
            "Automatically detect and fix image tilt?\n\n"
            "• Yes = Straighten + Remove background + Auto crop\n"
            "• No = Only straighten (keep background)\n"
            "• Cancel = Abort"
        )
        
        if response is None:  # Cancel
            return
        
        auto_clean = response  # True = clean, False = keep background
        
        self.log_status("Analyzing image angle...")
        
        try:
            img = self.pages[self.current_page_index]['processed']
            
            # Try OpenCV method first (more accurate)
            try:
                straightened = ImageProcessor.deskew_image(img)
                method = "Edge Detection"
            except Exception as e:
                # Fallback to simple method (no OpenCV needed)
                straightened = ImageProcessor.auto_straighten_simple(img)
                method = "Projection Analysis"
            
            # Auto-clean if requested
            if auto_clean:
                self.log_status("Removing background...")
                
                # Remove white background
                straightened = ImageProcessor.remove_white_background(straightened, threshold=240)
                
                # Auto crop to content
                straightened = ImageProcessor.perform_auto_crop(straightened)
                
                method += " + Auto Clean"
            
            # Update the page
            self.pages[self.current_page_index]['original'] = straightened
            self.reset_edits(reload_ui=False)
            self.process_image()
            
            self.log_status(f"✅ Image straightened ({method})")
            
            if auto_clean:
                messagebox.showinfo("✅ Success", 
                    f"Image has been straightened and cleaned!\n\n"
                    f"Method: {method}\n"
                    f"• Background removed\n"
                    f"• Auto-cropped to content")
            else:
                messagebox.showinfo("✅ Success", f"Image has been straightened!\n\nMethod: {method}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to straighten image:\n{e}")
            self.log_status("Straighten failed")

    def on_watermark_template_change(self, choice):
        """Handle watermark template selection"""
        if choice == "Custom...":
            # Prompt for custom text
            dialog = ctk.CTkInputDialog(
                text="Enter custom watermark text:",
                title="Custom Watermark"
            )
            custom_text = dialog.get_input()
            
            if custom_text:
                self.watermark_text.set(custom_text)
            else:
                # Revert to COPY if cancelled
                self.watermark_text.set("COPY")

    def update_watermark_preview(self, value):
        """Update watermark preview (could add live preview in future)"""
        # For now, just store the value
        pass

    def apply_watermark(self):
        """Apply watermark/stamp to current page"""
        if self.current_page_index == -1:
            messagebox.showwarning("No Page", "Please scan a page first.")
            return
        
        text = self.watermark_text.get()
        if not text or text == "Custom...":
            messagebox.showwarning("No Text", "Please select or enter watermark text.")
            return
        
        position = self.watermark_position.get()
        opacity_percent = self.watermark_opacity_slider.get()
        opacity = int(opacity_percent * 255)  # Convert 0-1 to 0-255
        
        self.log_status(f"Adding watermark: {text}...")
        
        try:
            img = self.pages[self.current_page_index]['processed']
            
            # Add watermark
            watermarked = ImageProcessor.add_watermark(
                img, 
                text=text,
                position=position,
                opacity=opacity,
                rotation=-45,  # Diagonal watermark
                color=(220, 38, 38)  # Red color
            )
            
            # Update the page
            self.pages[self.current_page_index]['original'] = watermarked
            self.reset_edits(reload_ui=False)
            self.process_image()
            
            self.log_status(f"✅ Watermark added: {text}")
            messagebox.showinfo("✅ Success", 
                              f"Watermark '{text}' has been added!\n\n"
                              f"Position: {position}\n"
                              f"Opacity: {int(opacity_percent * 100)}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add watermark:\n{e}")
            self.log_status("Watermark failed")

    def apply_crop(self):
        if not self.crop_start or not self.crop_end: return
        frame_w, frame_h = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        disp_w, disp_h = self.display_image_ref.size
        off_x, off_y = (frame_w - disp_w) // 2, (frame_h - disp_h) // 2
        
        x1 = (self.crop_start[0] - off_x) / self.display_scale
        y1 = (self.crop_start[1] - off_y) / self.display_scale
        x2 = (self.crop_end[0] - off_x) / self.display_scale
        y2 = (self.crop_end[1] - off_y) / self.display_scale
        
        box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        current_img = self.pages[self.current_page_index]['processed']
        cropped = current_img.crop(box)
        self.pages[self.current_page_index]['original'] = cropped
        self.reset_edits(reload_ui=False)
        self.process_image()
        self.toggle_crop_mode()

    def show_preview(self, pil_image):
        self.preview_canvas.delete("all")
        fw, fh = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        if fw < 50: fw = 600
        if fh < 50: fh = 600
        
        scale = min(fw / pil_image.width, fh / pil_image.height)
        new_w, new_h = int(pil_image.width * scale), int(pil_image.height * scale)
        self.display_scale = scale
        
        self.display_image_ref = pil_image.copy()
        self.display_image_ref.thumbnail((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_image_ref = ImageTk.PhotoImage(self.display_image_ref)
        self.preview_canvas.create_image(fw//2, fh//2, image=self.tk_image_ref, anchor="center")

    def update_thumbnails(self):
        for w in self.thumb_scroll.winfo_children(): w.destroy()
        for i, page in enumerate(self.pages):
            thumb = page['processed'].copy()
            thumb.thumbnail((220, 280))
            ctk_thumb = ctk.CTkImage(light_image=thumb, dark_image=thumb,
                                     size=(220, int(220*thumb.height/thumb.width)))
            
            is_selected = (i == self.current_page_index)
            
            # Card for thumbnail
            card = ctk.CTkFrame(self.thumb_scroll, fg_color=COLORS["surface" if not is_selected else "primary"],
                               corner_radius=12, border_width=2,
                               border_color=COLORS["primary"] if is_selected else COLORS["border"])
            card.pack(pady=8, padx=5, fill="x")
            
            btn = ctk.CTkButton(card, text="", image=ctk_thumb, compound="top", height=200,
                               fg_color="transparent", hover_color=COLORS["bg_gradient_end"],
                               corner_radius=10, command=lambda x=i: self.select_page(x))
            btn.pack(padx=5, pady=5)
            
            label = ctk.CTkLabel(card, text=f"Page {i+1}",
                                font=("Segoe UI", 12, "bold" if is_selected else "normal"),
                                text_color="white" if is_selected else COLORS["text"])
            label.pack(pady=(0, 10))

    def select_page(self, index):
        if 0 <= index < len(self.pages):
            self.current_page_index = index
            page = self.pages[index]
            self.bright_slider.set(page['brightness'])
            self.cont_slider.set(page['contrast'])
            if page['grayscale']: self.gray_switch.select()
            else: self.gray_switch.deselect()
            self.show_preview(page['processed'])
            self.update_thumbnails()
            if self.cropping_active: self.toggle_crop_mode()

    def delete_current_page(self):
        if 0 <= self.current_page_index < len(self.pages):
            del self.pages[self.current_page_index]
            if not self.pages:
                self.current_page_index = -1
                self.preview_canvas.delete("all")
                self.preview_canvas.create_text(400, 300, text="📄 Ready to Scan",
                                              fill=COLORS["text_lighter"], font=("Segoe UI", 18))
                self.save_img_btn.configure(state="disabled")
                self.save_pdf_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
                self.page_badge.configure(text="0")
                self.update_thumbnails()
            else:
                self.page_badge.configure(text=str(len(self.pages)))
                self.select_page(max(0, self.current_page_index - 1))

    def save_as_image(self):
        if self.current_page_index == -1: return
        folder = self.output_dir.get()
        prefix = self.filename_prefix.get() or "Scan"
        if not os.path.exists(folder): os.makedirs(folder, exist_ok=True)
        fname = f"{prefix}_{self.current_page_index+1}.jpg"
        path = os.path.join(folder, fname)
        try:
            self.pages[self.current_page_index]['processed'].save(path)
            messagebox.showinfo("✅ Saved", f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as_pdf(self):
        if not self.pages: return
        folder = self.output_dir.get()
        prefix = self.filename_prefix.get() or "Scan"
        if not os.path.exists(folder): os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{prefix}_Full.pdf")
        try:
            images = [p['processed'].convert("RGB") for p in self.pages]
            images[0].save(path, "PDF", save_all=True, append_images=images[1:])
            messagebox.showinfo("✅ Saved", f"PDF saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def split_current_page(self):
        if self.current_page_index == -1:
            messagebox.showwarning("No Page", "Scan a page first")
            return
        if not messagebox.askyesno("Split", "Split into L/R?"):
            return
        
        current = self.pages[self.current_page_index]
        img = current['processed']
        left_img, right_img = ImageProcessor.split_image_vertical(img)
        
        p1 = {'original': left_img, 'processed': left_img, 'rotation': 0, 'flip_h': False,
              'flip_v': False, 'brightness': 1.0, 'contrast': 1.0, 'grayscale': False}
        p2 = {'original': right_img, 'processed': right_img, 'rotation': 0, 'flip_h': False,
              'flip_v': False, 'brightness': 1.0, 'contrast': 1.0, 'grayscale': False}
        
        self.pages[self.current_page_index] = p1
        self.pages.insert(self.current_page_index + 1, p2)
        self.page_badge.configure(text=str(len(self.pages)))
        self.update_thumbnails()
        self.select_page(self.current_page_index)

    def reverse_pages(self):
        if not self.pages:
            messagebox.showwarning("No Pages", "Scan pages first")
            return
        if messagebox.askyesno("Reverse", "Reverse ALL pages?"):
            self.pages.reverse()
            self.update_thumbnails()
            self.select_page(0)

    def interleave_pages(self):
        if len(self.pages) < 2:
            messagebox.showwarning("Not Enough", "Need 2+ pages")
            return
        
        mid = len(self.pages) // 2
        fronts, backs = self.pages[:mid], self.pages[mid:]
        
        if messagebox.askyesno("Interleave", "Are backs in REVERSE order?"):
            backs.reverse()
        
        import itertools
        new_order = []
        for f, b in itertools.zip_longest(fronts, backs):
            if f: new_order.append(f)
            if b: new_order.append(b)
        
        self.pages = new_order
        self.update_thumbnails()
        self.select_page(0)

    # === Paper Size Functions ===
    def on_paper_size_change(self, choice):
        """Handle paper size selection"""
        if choice == "Custom...":
            self.ask_custom_size()
    
    def ask_custom_size(self):
        """Prompt user for custom paper size"""
        dialog = ctk.CTkInputDialog(
            text="Enter custom size in pixels:\nFormat: WIDTH x HEIGHT\nExample: 2480 x 3508",
            title="Custom Paper Size"
        )
        result = dialog.get_input()
        
        if result:
            try:
                parts = result.replace('×', 'x').split('x')
                if len(parts) == 2:
                    width = int(parts[0].strip())
                    height = int(parts[1].strip())
                    if width > 0 and height > 0:
                        self.paper_sizes["Custom..."] = (width, height)
                        messagebox.showinfo("✅ Success", f"Custom size set to {width}×{height}px")
                    else:
                        raise ValueError("Size must be positive")
                else:
                    raise ValueError("Invalid format")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid size format: {e}")
                self.paper_size_var.set("A4 (210×297mm)")
    
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
        methods = ["Fit (maintain aspect)", "Stretch (exact size)", "Crop Center"]
        choice = messagebox.askquestion(
            "Resize Method",
            f"Resize to {selected}?\n\nChoose method:\n• Yes = Fit (maintain aspect ratio)\n• No = Crop to center",
            icon='question'
        )
        
        if choice == 'yes':
            # Fit - maintain aspect ratio
            img_copy = current_img.copy()
            img_copy.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Create new image with white background
            new_img = Image.new('RGB', (target_w, target_h), 'white')
            paste_x = (target_w - img_copy.width) // 2
            paste_y = (target_h - img_copy.height) // 2
            new_img.paste(img_copy, (paste_x, paste_y))
        else:
            # Crop center
            img_w, img_h = current_img.size
            
            # Calculate crop box to center
            left = max(0, (img_w - target_w) // 2)
            top = max(0, (img_h - target_h) // 2)
            right = min(img_w, left + target_w)
            bottom = min(img_h, top + target_h)
            
            cropped = current_img.crop((left, top, right, bottom))
            
            # If cropped is smaller than target, pad with white
            if cropped.size != (target_w, target_h):
                new_img = Image.new('RGB', (target_w, target_h), 'white')
                paste_x = (target_w - cropped.width) // 2
                paste_y = (target_h - cropped.height) // 2
                new_img.paste(cropped, (paste_x, paste_y))
            else:
                new_img = cropped
        
        # Update page
        self.pages[self.current_page_index]['original'] = new_img
        self.pages[self.current_page_index]['processed'] = new_img.copy()
        self.reset_edits(reload_ui=False)
        self.process_image()
        self.log_status(f"Resized to {selected}")

    # === Collage & Photo Grid ===
    def create_collage_grid(self):
        """Create a photo grid collage from all scanned pages"""
        if len(self.pages) < 2:
            messagebox.showwarning("Not Enough Pages", "You need at least 2 pages to create a collage.\nScan more pages first.")
            return
        
        layout = self.grid_layout_var.get()
        
        # Confirm action
        if not messagebox.askyesno("Create Collage", 
                                   f"Create a {layout} photo grid from {len(self.pages)} page(s)?\n\nThis will add a new page with the collage."):
            return
        
        try:
            # Get processed images from all pages
            all_images = [page['processed'] for page in self.pages]
            
            # Create the grid
            self.log_status("Creating collage...")
            grid_image = ImageProcessor.create_photo_grid(
                all_images, 
                grid_layout=layout,
                spacing=20,
                bg_color=(255, 255, 255)
            )
            
            # Add as new page
            new_page = {
                'original': grid_image,
                'processed': grid_image.copy(),
                'rotation': 0,
                'flip_h': False,
                'flip_v': False,
                'brightness': 1.0,
                'contrast': 1.0,
                'grayscale': False
            }
            
            self.pages.append(new_page)
            self.page_badge.configure(text=str(len(self.pages)))
            self.update_thumbnails()
            self.select_page(len(self.pages) - 1)
            
            self.log_status(f"✅ Collage created ({layout})")
            messagebox.showinfo("✅ Success", f"Photo grid created!\n\nLayout: {layout}\nTotal images: {len(all_images)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create collage:\n{e}")
            self.log_status("Collage failed")

    # === User Guide ===
    def start_interactive_guide(self):
        steps = self.guide_service.get_steps()
        self.current_guide_step = 0
        self.show_guide_step(steps[0])

    def show_guide_step(self, step):
        self.preview_canvas.delete("all")
        fw, fh = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        self.preview_canvas.create_text(fw//2, fh//2 - 50, text=step["title"],
                                       font=("Segoe UI", 26, "bold"), fill=COLORS["primary"])
        self.preview_canvas.create_text(fw//2, fh//2 + 30, text=step["text"],
                                       font=("Segoe UI", 15), fill=COLORS["text"], 
                                       width=500, justify="center")
        self.guide_service.speak(step["text"])
        
        btn_tag = "next_btn"
        self.preview_canvas.create_rectangle(fw//2 - 60, fh//2 + 110, fw//2 + 60, fh//2 + 155,
                                            fill=COLORS["primary"], outline="", tags=btn_tag, width=0)
        self.preview_canvas.create_text(fw//2, fh//2 + 132, text="Next →", fill="white",
                                       font=("Segoe UI", 14, "bold"), tags=btn_tag)
        self.preview_canvas.tag_bind(btn_tag, "<Button-1>", lambda e: self.next_guide_step())

    def next_guide_step(self):
        self.current_guide_step += 1
        steps = self.guide_service.get_steps()
        if self.current_guide_step < len(steps):
            self.show_guide_step(steps[self.current_guide_step])
        else:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(400, 300, text="✅ Tour Complete!\nHappy Scanning",
                                          fill=COLORS["success"], font=("Segoe UI", 22, "bold"), justify="center")
            self.guide_service.speak("Tour complete!")

    # History & File Manager Methods
    def save_as_image(self):
        """Save current page as image and record in history"""
        if self.current_page_index == -1:
            messagebox.showwarning("No Page", "Please scan a page first.")
            return
        
        filename = f"{self.filename_prefix.get()}_{len(self.pages)}.jpg"
        filepath = os.path.join(self.output_dir.get(), filename)
        
        try:
            self.pages[self.current_page_index]['processed'].save(filepath, "JPEG", quality=95)
            
            # Add to history
            file_size = os.path.getsize(filepath)
            self.db_service.add_scan_history(
                filename=filename,
                filepath=filepath,
                file_type="JPEG",
                page_count=1,
                file_size=file_size,
                notes=f"Single page export"
            )
            
            messagebox.showinfo("✅ Saved", f"Image saved:\n{filepath}")
            self.log_status(f"Saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")

    def save_as_pdf(self):
        """Save all pages as PDF and record in history"""
        if not self.pages:
            messagebox.showwarning("No Pages", "Please scan some pages first.")
            return
        
        filename = f"{self.filename_prefix.get()}.pdf"
        filepath = os.path.join(self.output_dir.get(), filename)
        
        try:
            images = [page['processed'].convert('RGB') for page in self.pages]
            images[0].save(filepath, "PDF", save_all=True, append_images=images[1:])
            
            # Add to history
            file_size = os.path.getsize(filepath)
            self.db_service.add_scan_history(
                filename=filename,
                filepath=filepath,
                file_type="PDF",
                page_count=len(self.pages),
                file_size=file_size,
                notes=f"{len(self.pages)} pages combined"
            )
            
            messagebox.showinfo("✅ Saved", f"PDF saved with {len(self.pages)} page(s):\n{filepath}")
            self.log_status(f"PDF saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

    def show_scan_history(self):
        """Show scan history window"""
        history_window = ctk.CTkToplevel(self)
        history_window.title("📜 Scan History")
        history_window.geometry("800x600")
        
        # Header
        header_frame = ctk.CTkFrame(history_window, fg_color=COLORS["primary"], height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text="📜 Scan History", 
                    font=("Segoe UI", 20, "bold"), text_color="white").pack(pady=15)
        
        # Content frame
        content_frame = ctk. CTkScrollableFrame(history_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get history from database
        history = self.db_service.get_scan_history(limit=100)
        
        if not history:
            ctk.CTkLabel(content_frame, text="No scan history yet.\n\nSave some scans to see them here!",
                        font=("Segoe UI", 14), text_color=COLORS["text_light"]).pack(pady=50)
            return
        
        # Display history items
        for item in history:
            self._create_history_item(content_frame, item)

    def _create_history_item(self, parent, item):
        """Create a history item widget"""
        item_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], 
                                 border_width=1, border_color=COLORS["border"], corner_radius=10)
        item_frame.pack(fill="x", pady=5)
        
        # Left side - info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Filename
        ctk.CTkLabel(info_frame, text=item['filename'], font=("Segoe UI", 13, "bold"),
                    anchor="w").pack(fill="x")
        
        # Details
        file_size_mb = item['file_size'] / (1024 * 1024)
        details = f"📄 {item['file_type']} | 📑 {item['page_count']} page(s) | 💾 {file_size_mb:.2f} MB"
        ctk.CTkLabel(info_frame, text=details, font=("Segoe UI", 10),
                    text_color=COLORS["text_light"], anchor="w").pack(fill="x")
        
        # Date
        ctk.CTkLabel(info_frame, text=f"🕒 {item['scan_date']}", font=("Segoe UI", 9),
                    text_color=COLORS["text_lighter"], anchor="w").pack(fill="x", pady=(3, 0))
        
        # Right side - actions
        action_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=10, pady=10)
        
        # Open button
        if os.path.exists(item['filepath']):
            ctk.CTkButton(action_frame, text="📂 Open", width=80, height=30,
                         command=lambda p=item['filepath']: os.startfile(p),
                         fg_color=COLORS["primary"], corner_radius=8).pack(side="left", padx=3)
            
            ctk.CTkButton(action_frame, text="📁 Folder", width=80, height=30,
                         command=lambda p=os.path.dirname(item['filepath']): os.startfile(p),
                         fg_color=COLORS["secondary"], corner_radius=8).pack(side="left", padx=3)
        else:
            ctk.CTkLabel(action_frame, text="❌ File not found", 
                        text_color=COLORS["danger"]).pack()

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        folder = self.output_dir.get()
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showwarning("Not Found", f"Folder does not exist:\n{folder}")

    def clear_history_confirm(self):
        """Confirm and clear scan history"""
        if messagebox.askyesno("Clear History", 
                              "Clear all scan history?\n\nThis won't delete the actual files, only the history records."):
            self.db_service.clear_scan_history()
            messagebox.showinfo("✅ Cleared", "Scan history has been cleared.")
            self.log_status("History cleared")

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()
