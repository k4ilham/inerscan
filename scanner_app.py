import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance, ImageOps
import win32com.client
import sys
import numpy as np
from tkinter import colorchooser

# Aesthetic Setup - Dark Mode with Cyan Accents
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Using built-in theme for reliability

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("InerScan - Advanced Document Scanner")
        self.geometry("900x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Row 1 removed (was edit controls)

        # --- Variables ---
        self.pages = []
        self.current_page_index = -1
        self.scan_result_path = "temp_scan.png"
        
        # Edit States
        self.cropping_active = False
        self.crop_start = None
        self.crop_end = None
        self.crop_rect_id = None
        self.tk_image_ref = None # Keep reference to avoid garbage collection
        self.display_image_ref = None # The resized image shown on canvas
        self.display_scale = 1.0 # Ratio of display / actual
        
        # Export Variables
        self.output_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Documents", "Scans"))
        self.filename_prefix = tk.StringVar(value="Scan")



        # --- Sidebar (Controls) ---
        # --- Sidebar (Controls) ---
        # --- Sidebar (Left) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1) # Scrollable Content

        # 1. Header
        self.header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(self.header_frame, text="InerScan", font=ctk.CTkFont(size=24, weight="bold", family="Roboto")).pack(anchor="w")
        ctk.CTkLabel(self.header_frame, text="v1.2 Pro", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray").pack(anchor="w")
        
        # Theme Toggle (Header)
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.header_frame, values=["Dark", "Light"], command=self.change_appearance_mode_event, width=100)
        self.appearance_mode_menu.pack(anchor="w", pady=(10, 0))

        # 2. Scrollable Content
        self.scroll_content = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="CONTROLS")
        self.scroll_content.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_content.grid_columnconfigure(0, weight=1)

        # --- Section: Scan ---
        ctk.CTkLabel(self.scroll_content, text="SCANNER", font=ctk.CTkFont(size=12, weight="bold"), text_color=("gray50", "gray70")).pack(anchor="w", pady=(0, 5))
        
        self.device_label = ctk.CTkLabel(self.scroll_content, text="Epson L3110", font=ctk.CTkFont(size=12), text_color="#00A8E8")
        self.device_label.pack(anchor="w", pady=(0, 10))

        self.scan_button = ctk.CTkButton(self.scroll_content, text="START SCAN", command=self.perform_scan, height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#00A8E8", hover_color="#0077B6")
        self.scan_button.pack(fill="x", pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.scroll_content, height=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(5, 15))

        # --- Section: Edit ---
        ctk.CTkLabel(self.scroll_content, text="IMAGE EDITING", font=ctk.CTkFont(size=12, weight="bold"), text_color=("gray50", "gray70")).pack(anchor="w", pady=(10, 5))
        
        # Adjustments Grid
        self.edit_grid = ctk.CTkFrame(self.scroll_content, fg_color="transparent")
        self.edit_grid.pack(fill="x", pady=5)
        
        # Row 1: Rotate/Flip Buttons
        btn_frame = ctk.CTkFrame(self.edit_grid, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="↺", width=30, command=lambda: self.rotate(-90)).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="↻", width=30, command=lambda: self.rotate(90)).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Flip H", width=50, command=self.toggle_flip_h).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Flip V", width=50, command=self.toggle_flip_v).pack(side="left", padx=2)

        # Row 2: Brightness
        ctk.CTkLabel(self.edit_grid, text="Brightness", font=ctk.CTkFont(size=11)).pack(anchor="w")
        self.bright_slider = ctk.CTkSlider(self.edit_grid, from_=0.5, to=2.0, command=self.update_brightness)
        self.bright_slider.set(1.0)
        self.bright_slider.pack(fill="x", pady=(0, 10))

        # Row 3: Contrast
        ctk.CTkLabel(self.edit_grid, text="Contrast", font=ctk.CTkFont(size=11)).pack(anchor="w")
        self.cont_slider = ctk.CTkSlider(self.edit_grid, from_=0.5, to=2.0, command=self.update_contrast)
        self.cont_slider.set(1.0)
        self.cont_slider.pack(fill="x", pady=(0, 10))
        
        # Row 4: Advanced Edits (Crop, BG)
        adv_frame = ctk.CTkFrame(self.edit_grid, fg_color="transparent")
        adv_frame.pack(fill="x", pady=5)
        
        self.crop_btn = ctk.CTkButton(adv_frame, text="Crop Tool", width=80, command=self.toggle_crop_mode, fg_color="#E76F51", hover_color="#D35400")
        self.crop_btn.pack(side="left", padx=2, fill="x", expand=True)

        ctk.CTkButton(adv_frame, text="BG Color", width=80, command=self.change_bg_color, fg_color="#2A9D8F", hover_color="#21867A").pack(side="left", padx=2, fill="x", expand=True)
        
        self.remove_bg_btn = ctk.CTkButton(self.scroll_content, text="Remove White Background", command=self.remove_white_bg, fg_color="#264653", hover_color="#1D353F")
        self.remove_bg_btn.pack(fill="x", pady=5)
        
        # Row 5: Mode & Reset
        self.gray_switch = ctk.CTkSwitch(self.edit_grid, text="B&W Mode", command=self.toggle_grayscale)
        self.gray_switch.pack(anchor="w", pady=5)
        
        self.reset_btn = ctk.CTkButton(self.edit_grid, text="Reset Edits", height=25, fg_color="transparent", border_width=1, border_color=("gray", "gray"), text_color=("black", "gray90"), command=self.reset_edits)
        self.reset_btn.pack(fill="x", pady=10)

        # --- Section: Export ---
        ctk.CTkLabel(self.scroll_content, text="EXPORT SETTINGS", font=ctk.CTkFont(size=12, weight="bold"), text_color=("gray50", "gray70")).pack(anchor="w", pady=(15, 5))
        
        ctk.CTkLabel(self.scroll_content, text="Filename Prefix:", font=ctk.CTkFont(size=11)).pack(anchor="w")
        self.filename_entry = ctk.CTkEntry(self.scroll_content, textvariable=self.filename_prefix)
        self.filename_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(self.scroll_content, text="Save Location:", font=ctk.CTkFont(size=11)).pack(anchor="w")
        self.folder_entry = ctk.CTkEntry(self.scroll_content, textvariable=self.output_dir)
        self.folder_entry.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(self.scroll_content, text="Browse Folder...", height=25, fg_color=("gray75", "#2B2B2B"), text_color=("black", "white"), command=self.browse_folder).pack(fill="x", pady=(0, 15))

        self.save_img_btn = ctk.CTkButton(self.scroll_content, text="Save Selected (JPG)", command=self.save_as_image, state="disabled", fg_color="#2B2B2B", hover_color="#3A3A3A")
        self.save_img_btn.pack(fill="x", pady=5)
        
        self.save_pdf_btn = ctk.CTkButton(self.scroll_content, text="Save All to PDF", command=self.save_as_pdf, state="disabled", fg_color="#2B2B2B", hover_color="#3A3A3A")
        self.save_pdf_btn.pack(fill="x", pady=5)

        # --- Main Area (Preview) ---
        self.preview_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("gray90", "#232323"))
        self.preview_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        # --- Right Sidebar (Pages) ---
        self.right_sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.right_sidebar.grid(row=0, column=2, rowspan=2, sticky="nsew")
        self.right_sidebar.grid_rowconfigure(1, weight=1)

        self.thumb_label = ctk.CTkLabel(self.right_sidebar, text="PAGES", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray")
        self.thumb_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.thumb_scroll = ctk.CTkScrollableFrame(self.right_sidebar, label_text="")
        self.thumb_scroll.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.delete_btn = ctk.CTkButton(self.right_sidebar, text="Delete Selected Page", fg_color="#E63946", hover_color="#B92B27", command=self.delete_current_page, state="disabled")
        self.delete_btn.grid(row=2, column=0, padx=10, pady=20, sticky="ew")

        # Canvas for Image Preview (Replaces Label)
        self.preview_canvas = tk.Canvas(self.preview_frame, bg="#232323", highlightthickness=0)
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind Mouse Events for Cropping
        self.preview_canvas.bind("<Button-1>", self.on_mouse_down)
        self.preview_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # Placeholder Text (drawn on canvas initially)
        self.preview_canvas.create_text(250, 300, text="No document scanned.\nClick 'START SCAN' to begin.", fill="gray", font=("Arial", 16), tags="placeholder")

        # Old Edit Frame Removed


        # Status Bar
        self.status_label = ctk.CTkLabel(self, text="Ready", anchor="w", padx=10, font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="ew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def log_status(self, message):
        self.status_label.configure(text=message)
        self.update_idletasks()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def perform_scan(self):
        """Initiates the scanning process using WIA."""
        self.log_status("Connecting to scanner...")
        self.progress_bar.start()
        try:
            # WIA Common Dialog for standardized scanning interface
            wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
            
            # This opens the native Windows scan dialog
            # It handles device selection if multiple, or uses default
            image_file = wia_dialog.ShowAcquireImage()

            if image_file:
                self.log_status("Scan complete. Adding page...")
                
                # Save temporarily
                if os.path.exists(self.scan_result_path):
                    os.remove(self.scan_result_path)
                    
                image_file.SaveFile(os.path.abspath(self.scan_result_path))
                
                # Load with PIL
                new_img = Image.open(self.scan_result_path)
                
                # Create Page Object
                page_data = {
                    'original': new_img.copy(),
                    'processed': new_img.copy(),
                    'rotation': 0,
                    'flip_h': False,
                    'flip_v': False,
                    'brightness': 1.0,
                    'contrast': 1.0,
                    'grayscale': False
                }
                
                self.pages.append(page_data)
                self.select_page(len(self.pages) - 1)
                self.update_thumbnails()
                
                # Enable Save Buttons
                self.save_img_btn.configure(state="normal")
                self.save_pdf_btn.configure(state="normal")
                self.delete_btn.configure(state="normal")
                self.log_status(f"Page {len(self.pages)} added.")
            else:
                self.log_status("Scan cancelled by user.")
                
            self.progress_bar.stop()
            self.progress_bar.set(0)
                
        except Exception as e:
            self.progress_bar.stop()
            self.progress_bar.set(0)
            # Check for specific WIA errors (like no device found)
            err_msg = str(e)
            if "0x80210015" in err_msg:
                 messagebox.showerror("Error", "No scanner device found or device is busy.\nPlease check connection to Epson L3110.")
            else:
                 messagebox.showerror("Error", f"Failed to scan: {e}")
            self.log_status("Error occurred.")

    def show_preview(self, pil_image):
        """Resizes and displays the image in the GUI."""
        # Calculate aspect ratio to fit in preview frame
        # Get current frame size (approximate if not drawn yet)
        frame_width = self.preview_frame.winfo_width()
        frame_height = self.preview_frame.winfo_height()
        
        if frame_width < 50: frame_width = 500
        if frame_height < 50: frame_height = 600
        
        # Resize logic
        img_ratio = pil_image.width / pil_image.height
        frame_ratio = frame_width / frame_height
        
        if img_ratio > frame_ratio:
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            new_height = frame_height
            new_width = int(frame_height * img_ratio)
            
        # Create thumbnail (copy)
        preview_img = pil_image.copy()
        preview_img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to CTkImage
        # ctk_img = ctk.CTkImage(light_image=preview_img, dark_image=preview_img, size=(new_width, new_height))
        
        # Update Label
        # self.preview_label.configure(image=ctk_img, text="")
        # self.preview_label.image = ctk_img  # Keep reference

    def update_thumbnails(self):
        # Clear existing
        for widget in self.thumb_scroll.winfo_children():
            widget.destroy()
            
        for i, page in enumerate(self.pages):
            # Create thumbnail
            thumb_img = page['processed'].copy()
            thumb_img.thumbnail((80, 100))
            ctk_thumb = ctk.CTkImage(light_image=thumb_img, dark_image=thumb_img, size=(80, int(80 * thumb_img.height / thumb_img.width)))
            
            btn_color = "#00A8E8" if i == self.current_page_index else "transparent"
            btn = ctk.CTkButton(self.thumb_scroll, text=f"Page {i+1}", image=ctk_thumb, compound="top", 
                                fg_color=btn_color, command=lambda idx=i: self.select_page(idx))
            btn.pack(pady=5, padx=5, fill="x")

    def delete_current_page(self):
        if 0 <= self.current_page_index < len(self.pages):
            del self.pages[self.current_page_index]
            
            if not self.pages:
                # No pages left
                self.current_page_index = -1
                self.preview_canvas.delete("all")
                self.preview_canvas.create_text(250, 300, text="No document scanned.\nClick 'START SCAN' to begin.", fill="gray", font=("Arial", 16), tags="placeholder")
                self.save_img_btn.configure(state="disabled")
                self.save_pdf_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
                self.update_thumbnails()
            else:
                # Select previous or next
                new_index = max(0, self.current_page_index - 1)
                self.select_page(new_index)

    def select_page(self, index):
        if 0 <= index < len(self.pages):
            self.current_page_index = index
            page = self.pages[index]
            
            # Update Edit Controls
            self.bright_slider.set(page['brightness'])
            self.cont_slider.set(page['contrast'])
            if page['grayscale']:
                self.gray_switch.select()
            else:
                self.gray_switch.deselect()
                
            self.show_preview(page['processed'])
            self.update_thumbnails()
            
            # Reset Crop State
            self.cancel_crop_mode()

    def show_preview(self, pil_image):
        """Resizes and displays the image on the Canvas."""
        # Clear Canvas
        self.preview_canvas.delete("all")
        
        # Get Frame Size
        frame_width = self.preview_frame.winfo_width()
        frame_height = self.preview_frame.winfo_height()
        
        if frame_width < 50: frame_width = 500
        if frame_height < 50: frame_height = 600
        
        # Resize logic
        img_ratio = pil_image.width / pil_image.height
        frame_ratio = frame_width / frame_height
        
        if img_ratio > frame_ratio:
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            new_height = frame_height
            new_width = int(frame_height * img_ratio)
            
        self.display_scale = new_width / pil_image.width
            
        # Create thumbnail (copy)
        self.display_image_ref = pil_image.copy()
        self.display_image_ref.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to ImageTk
        self.tk_image_ref = ImageTk.PhotoImage(self.display_image_ref)
        
        # Center Image
        x_center = frame_width // 2
        y_center = frame_height // 2
        
        self.preview_canvas.create_image(x_center, y_center, image=self.tk_image_ref, anchor="center")
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))

    # --- Crop Logic ---
    def toggle_crop_mode(self):
        if self.current_page_index == -1: return
        
        if not self.cropping_active:
            self.cropping_active = True
            self.crop_btn.configure(text="Cancel Crop", fg_color="#E76F51") # Red
            self.preview_canvas.config(cursor="crosshair")
            self.log_status("Crop Mode Active. Drag to select area.")
        else:
            self.cancel_crop_mode()
            
    def cancel_crop_mode(self):
        self.cropping_active = False
        self.crop_btn.configure(text="Crop Tool", fg_color="#E76F51") # Reset color
        self.preview_canvas.config(cursor="")
        self.preview_canvas.delete("crop_rect")
        self.log_status("Ready")

    def on_mouse_down(self, event):
        if not self.cropping_active: return
        self.crop_start = (event.x, event.y)
        if self.crop_rect_id:
            self.preview_canvas.delete(self.crop_rect_id)
            
    def on_mouse_drag(self, event):
        if not self.cropping_active or not self.crop_start: return
        
        if self.crop_rect_id:
            self.preview_canvas.delete(self.crop_rect_id)
            
        self.crop_rect_id = self.preview_canvas.create_rectangle(
            self.crop_start[0], self.crop_start[1], event.x, event.y,
            outline="red", width=2, dash=(4, 4), tags="crop_rect"
        )

    def on_mouse_release(self, event):
        if not self.cropping_active or not self.crop_start: return
        
        self.crop_end = (event.x, event.y)
        
        # Confirm Dialog
        if messagebox.askyesno("Confirm Crop", "Apply this crop?"):
            self.apply_crop()
        else:
            self.preview_canvas.delete("crop_rect")

    def apply_crop(self):
        if not self.crop_start or not self.crop_end: return
        
        # Calculate coordinate in original image space
        # Canvas Coords (Centered) -> Image Coords
        # We need to know where the image top-left is drawn
        frame_width = self.preview_frame.winfo_width()
        frame_height = self.preview_frame.winfo_height()
        
        # Image dimensions on canvas
        disp_w, disp_h = self.display_image_ref.size
        
        # Image top-left on canvas
        img_x = (frame_width - disp_w) // 2
        img_y = (frame_height - disp_h) // 2
        
        # Selection relative to image
        x1 = (self.crop_start[0] - img_x) / self.display_scale
        y1 = (self.crop_start[1] - img_y) / self.display_scale
        x2 = (self.crop_end[0] - img_x) / self.display_scale
        y2 = (self.crop_end[1] - img_y) / self.display_scale
        
        # Normalize coords
        left = max(0, min(x1, x2))
        top = max(0, min(y1, y2))
        right = min(self.pages[self.current_page_index]['original'].width, max(x1, x2))
        bottom = min(self.pages[self.current_page_index]['original'].height, max(y1, y2))
        
        if right - left < 10 or bottom - top < 10:
             self.log_status("Crop area too small.")
             return

        # Crop original and processed
        box = (left, top, right, bottom)
        
        # We crop the *current processed* image to reflect edits properly
        # But for non-destructive workflow, we usually crop original. 
        # Here we crop original and re-process.
        # But wait, cropping is a geometric transform. Rotations are also geometric.
        # If we crop original, rotation needs to happen after.
        # It's safer to crop the *current processed state* and set that as new original?
        # Let's crop the PROCESSED image and set keys to default.
        
        cropped_img = self.pages[self.current_page_index]['processed'].crop(box)
        
        # Update Page Data
        self.pages[self.current_page_index]['original'] = cropped_img
        self.pages[self.current_page_index]['processed'] = cropped_img
        
        # Reset Edits since they are baked in now (or try to preserve? Baking is safer for Crop)
        self.pages[self.current_page_index]['rotation'] = 0
        self.pages[self.current_page_index]['flip_h'] = False
        self.pages[self.current_page_index]['flip_v'] = False
        
        self.cancel_crop_mode()
        self.process_image() # Refresh view
        self.log_status("Image cropped.")
        
    # --- Background Logic ---
    def remove_white_bg(self):
        if self.current_page_index == -1: return
        
        img = self.pages[self.current_page_index]['processed'].convert("RGBA")
        data = np.array(img)
        
        # Threshold for white (e.g., > 200, 200, 200)
        red, green, blue, alpha = data.T
        white_areas = (red > 200) & (green > 200) & (blue > 200)
        data[..., 3][white_areas.T] = 0 # Set alpha to 0
        
        new_img = Image.fromarray(data)
        
        # Update as new original (destructive edit for simplicity)
        self.pages[self.current_page_index]['original'] = new_img
        self.process_image()
        self.log_status("White background removed.")
        
    def change_bg_color(self):
        if self.current_page_index == -1: return
        
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]: # Hex string
            bg_color = color[0] # RGB tuple
            
            img = self.pages[self.current_page_index]['processed'].convert("RGBA")
            
            # Create colored background
            background = Image.new("RGBA", img.size, (int(bg_color[0]), int(bg_color[1]), int(bg_color[2]), 255))
            
            # Composite (Image over Background)
            # If image has no alpha, this does nothing useful unless we removed bg first
            # But "Change BG" implies we probably just removed it.
            # If image is solid, this just puts it on top.
            # So this is mostly useful AFTER remove_white_bg.
            
            composite = Image.alpha_composite(background, img)
            
            self.pages[self.current_page_index]['original'] = composite.convert("RGB")
            self.process_image()
            self.log_status(f"Background changed to {color[1]}")

    # --- Image Processing Methods ---
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
        
    def reset_edits(self, reload_ui=True):
        if self.current_page_index == -1: return
        
        self.pages[self.current_page_index]['rotation'] = 0
        self.pages[self.current_page_index]['flip_h'] = False
        self.pages[self.current_page_index]['flip_v'] = False
        self.pages[self.current_page_index]['brightness'] = 1.0
        self.pages[self.current_page_index]['contrast'] = 1.0
        self.pages[self.current_page_index]['grayscale'] = False
        
        if reload_ui:
            self.bright_slider.set(1.0)
            self.cont_slider.set(1.0)
            self.gray_switch.deselect()
            self.process_image()
            
    def process_image(self):
        if self.current_page_index == -1: return
        
        page = self.pages[self.current_page_index]
        img = page['original'].copy()

        # Rotate
        if page['rotation'] != 0:
            img = img.rotate(page['rotation'], expand=True)

        # Flip
        if page['flip_h']:
            img = ImageOps.mirror(img)
        if page['flip_v']:
            img = ImageOps.flip(img)

        # Grayscale
        if page['grayscale']:
            img = img.convert("L").convert("RGB")
        else:
            if img.mode != "RGB":
                img = img.convert("RGB")

        # Color Enhancements
        if page['brightness'] != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(page['brightness'])
            
        if page['contrast'] != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(page['contrast'])

        self.pages[self.current_page_index]['processed'] = img
        self.show_preview(img)
        self.update_thumbnails()


    def save_as_image(self):
        if self.current_page_index == -1: return
            
        # Determine path
        folder = self.output_dir.get()
        prefix = self.filename_prefix.get().strip() or "Scan"
        
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                messagebox.showerror("Error", "Invalid Output Folder")
                return

        # Auto-generate name to avoid overwrite
        filename = f"{prefix}_{len(self.pages)}_{self.current_page_index+1}.jpg"
        file_path = os.path.join(folder, filename)
        
        # If user didn't select a folder, default to ask
        if not folder or folder == ".":
             file_path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=filename)

        if file_path:
            try:
                self.pages[self.current_page_index]['processed'].save(file_path)
                self.log_status(f"Saved to {file_path}")
                messagebox.showinfo("Success", f"Saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def save_as_pdf(self):
        if not self.pages: return
            
        folder = self.output_dir.get()
        prefix = self.filename_prefix.get().strip() or "Scan"
        
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                messagebox.showerror("Error", "Invalid Output Folder")
                return
                
        filename = f"{prefix}_Full.pdf"
        file_path = os.path.join(folder, filename)
        
        if not folder or folder == ".":
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=filename)
        
        if file_path:
            try:
                pdf_images = []
                for p in self.pages:
                    pdf_images.append(p['processed'].convert("RGB"))
                
                if pdf_images:
                    pdf_images[0].save(file_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])
                    
                self.log_status(f"Saved full PDF to {file_path}")
                messagebox.showinfo("Success", f"Saved PDF to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save PDF: {e}")

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()
