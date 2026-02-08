# Tab switching helper methods

def create_editor_controls(self):
    """Create Editor tab controls - focused on editing only"""
    self.editor_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
    
    ctk.CTkLabel(self.editor_frame, text="🎨 Editor Mode", 
                font=("Segoe UI", 18, "bold"), text_color=COLORS["primary"]).pack(pady=(0, 10))
    
    ctk.CTkLabel(self.editor_frame, text="Select a page from the right sidebar to edit",
                font=("Segoe UI", 11), text_color=COLORS["text_light"]).pack(pady=(0, 20))
    
    # Quick Tools
    self._section_header(self.editor_frame, "✨ Quick Tools")
    
    quick_tools = [
        ("↺ Rotate Left", lambda: self.rotate(-90)),
        ("↻ Rotate Right", lambda: self.rotate(90)),
        ("↔ Flip H", self.toggle_flip_h),
        ("↕ Flip V", self.toggle_flip_v)
    ]
    
    tool_grid = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
    tool_grid.pack(fill="x", pady=(0, 15))
    tool_grid.grid_columnconfigure((0, 1), weight=1)
    
    for i, (text, cmd) in enumerate(quick_tools):
        btn = ctk.CTkButton(tool_grid, text=text, command=cmd, height=40,
                           fg_color=COLORS["bg_gradient_end"], text_color=COLORS["text"],
                           hover_color=COLORS["border"], font=("Segoe UI", 12), corner_radius=10)
        btn.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
    
    # Adjustments
    self._section_header(self.editor_frame, "🎭 Adjustments")
    self._slider_control(self.editor_frame, "💡 Brightness", self.update_brightness)
    self.bright_slider_editor = self.editor_frame.winfo_children()[-1]
    self.bright_slider_editor.set(1.0)
    
    self._slider_control(self.editor_frame, "🎭 Contrast", self.update_contrast)
    self.cont_slider_editor = self.editor_frame.winfo_children()[-1]
    self.cont_slider_editor.set(1.0)
    
    self.gray_switch_editor = ctk.CTkSwitch(self.editor_frame, text="⚫ Black & White",
                                           command=self.toggle_grayscale, font=("Segoe UI", 12))
    self.gray_switch_editor.pack(anchor="w", pady=(10, 20))
    
    # Advanced
    self._section_header(self.editor_frame, "🔧 Advanced Tools")
    
    adv_actions = [
        ("📐 Auto-Straighten", self.auto_straighten, "#06B6D4"),
        ("✂️ Crop Tool", self.toggle_crop_mode, COLORS["warning"]),
        ("🧹 Remove Background", self.remove_white_bg, COLORS["secondary"]),
        ("📐 Auto Crop", self.perform_auto_crop, COLORS["success"])
    ]
    
    for text, cmd, color in adv_actions:
        self._action_button(self.editor_frame, text, cmd, color)

def create_library_controls(self):
    """Create Library tab controls - manage all scanned pages"""
    self.library_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
    
    ctk.CTkLabel(self.library_frame, text="📚 Library", 
                font=("Segoe UI", 18, "bold"), text_color=COLORS["primary"]).pack(pady=(0, 10))
    
    # Stats
    self.lib_stats_label = ctk.CTkLabel(self.library_frame, 
                                       text="No pages yet",
                                       font=("Segoe UI", 13), 
                                       text_color=COLORS["text"])
    self.lib_stats_label.pack(pady=(0, 20))
    
    # Actions
    self._section_header(self.library_frame, "📋 Manage Pages")
    
    lib_actions = [
        ("➕ Add New Scan", self.perform_scan),
        ("🔄 Refresh Library", self.update_library_stats),
        ("🗑️ Delete Current", self.delete_current_page),
        ("🧹 Clear All", self.clear_all_pages)
    ]
    
    for text, cmd in lib_actions:
        ctk.CTkButton(self.library_frame, text=text, command=cmd, height=40, corner_radius=10,
                     fg_color=COLORS["primary"] if "Add" in text else "transparent",
                     border_width=2 if "Add" not in text else 0,
                     border_color=COLORS["border"],
                     text_color="white" if "Add" in text else COLORS["text"],
                     hover_color=COLORS["primary_light"],
                     font=("Segoe UI", 12, "bold" if "Add" in text else "normal")).pack(fill="x", pady=3)
    
    # Export Section
    self._section_header(self.library_frame, "💾 Export Library")
    
    self._input_field(self.library_frame, "Filename", self.filename_prefix)
    self._input_field(self.library_frame, "Location", self.output_dir)
    
    ctk.CTkButton(self.library_frame, text="📁 Browse...", command=self.browse_folder, 
                 height=36, fg_color="transparent", border_width=2, 
                 border_color=COLORS["border"], text_color=COLORS["text"],
                 hover_color=COLORS["bg_gradient_end"], corner_radius=10,
                 font=("Segoe UI", 11)).pack(fill="x", pady=(0, 15))
    
    self.save_all_btn = ctk.CTkButton(self.library_frame, text="📄 Export All as PDF",
                                     command=self.save_as_pdf, state="disabled",
                                     height=45, corner_radius=12, fg_color=COLORS["primary"],
                                     font=("Segoe UI", 13, "bold"))
    self.save_all_btn.pack(fill="x", pady=3)

def show_tab_controls(self, tab_id):
    """Show/hide appropriate controls based on selected tab"""
    # Hide all frames first
    self.scanner_frame.pack_forget()
    self.editor_frame.pack_forget()
    self.library_frame.pack_forget()
    
    # Show selected frame
    if tab_id == "scanner":
        self.scanner_frame.pack(fill="both", expand=True)
    elif tab_id == "editor":
        self.editor_frame.pack(fill="both", expand=True)
        # Sync sliders with current page
        if self.current_page_index != -1:
            page = self.pages[self.current_page_index]
            self.bright_slider_editor.set(page['brightness'])
            self.cont_slider_editor.set(page['contrast'])
            if page['grayscale']:
                self.gray_switch_editor.select()
            else:
                self.gray_switch_editor.deselect()
    elif tab_id == "library":
        self.library_frame.pack(fill="both", expand=True)
        self.update_library_stats()

def update_library_stats(self):
    """Update library statistics"""
    if hasattr(self, 'lib_stats_label'):
        count = len(self.pages)
        if count == 0:
            self.lib_stats_label.configure(text="No pages in library")
            if hasattr(self, 'save_all_btn'):
                self.save_all_btn.configure(state="disabled")
        else:
            self.lib_stats_label.configure(text=f"📄 {count} page(s) in library")
            if hasattr(self, 'save_all_btn'):
                self.save_all_btn.configure(state="normal")

def clear_all_pages(self):
    """Clear all scanned pages"""
    if not self.pages:
        messagebox.showinfo("Empty", "No pages to clear")
        return
    
    if messagebox.askyesno("Clear All", f"Delete all {len(self.pages)} page(s)?\n\nThis cannot be undone!"):
        self.pages = []
        self.current_page_index = -1
        self.preview_canvas.delete("all")
        self.preview_canvas.create_text(400, 300, text="📄 Library Cleared",
                                      fill=COLORS["text_lighter"], font=("Segoe UI", 18))
        self.update_thumbnails()
        self.update_library_stats()
        self.page_badge.configure(text="0")
        self.save_img_btn.configure(state="disabled")
        self.save_pdf_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        messagebox.showinfo("✅ Cleared", "All pages have been deleted")
