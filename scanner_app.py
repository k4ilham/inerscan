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
        
        # Left Panel - Controls Card (Scanner Tab)
        self.left_card = self._create_card(main, 320)
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        scroll = ctk.CTkScrollableFrame(self.left_card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Scan Button with Badge
        scan_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        scan_frame.pack(fill="x", pady=(0, 10))
        
        self.scan_btn = ctk.CTkButton(scan_frame, text="🚀 Start Scan", height=50, corner_radius=12,
                                     fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
                                     font=("Segoe UI", 15, "bold"), command=self.perform_scan)
        self.scan_btn.pack(fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(scroll, height=8, corner_radius=4, 
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
            ("✂️ Crop Tool", self.toggle_crop_mode, COLORS["warning"]),
            ("🧹 Remove Background", self.remove_white_bg, COLORS["secondary"]),
            ("📐 Auto Crop", self.perform_auto_crop, COLORS["success"])
        ]
        
        for text, cmd, color in actions:
            self._action_button(scroll, text, cmd, color)
        
        self.gray_switch = ctk.CTkSwitch(scroll, text="⚫ Black & White", 
                                        command=self.toggle_grayscale, font=("Segoe UI", 12))
        self.gray_switch.pack(anchor="w", pady=(10, 20))
        
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
        
        # Show different content based on tab
        if tab_id == "editor":
            messagebox.showinfo("🎨 Editor Mode", 
                              "Editor mode is active!\n\n"
                              "You can now use all editing tools in the left sidebar:\n"
                              "• Rotate, flip, crop\n"
                              "• Adjust brightness & contrast\n"
                              "• Remove background\n"
                              "• Resize to paper sizes\n"
                              "• Create photo grids\n\n"
                              "Select a page from the right sidebar to edit.")
        elif tab_id == "library":
            if not self.pages:
                messagebox.showinfo("📚 Library", 
                                  "No scanned documents yet!\n\n"
                                  "Switch back to Scanner tab and scan some documents first.")
            else:
                messagebox.showinfo("📚 Library", 
                                  f"You have {len(self.pages)} page(s) in your library.\n\n"
                                  "View all pages in the right sidebar.\n"
                                  "Click any page to view and edit it.")

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

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()
