"""
Loading and Animation Components
Provides various loading indicators and animations for the scanner app
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import math
import time

class LoadingSpinner(ctk.CTkFrame):
    """Animated loading spinner widget"""
    
    def __init__(self, parent, size=50, color="#0284c7", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.size = size
        self.color = color
        self.angle = 0
        self.is_running = False
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(self, width=size, height=size, 
                               bg=self._get_parent_bg(), highlightthickness=0)
        self.canvas.pack()
        
        self.animation_id = None
        
    def _get_parent_bg(self):
        """Get parent background color"""
        try:
            return self.master.cget("fg_color")[0] if isinstance(self.master.cget("fg_color"), tuple) else self.master.cget("fg_color")
        except:
            return "#f0f9ff"
    
    def start(self):
        """Start the spinning animation"""
        self.is_running = True
        self._animate()
        
    def stop(self):
        """Stop the spinning animation"""
        self.is_running = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        self.canvas.delete("all")
    
    def _animate(self):
        """Animate the spinner"""
        if not self.is_running:
            return
            
        self.canvas.delete("all")
        
        # Draw spinning arc
        center = self.size / 2
        radius = self.size / 2 - 5
        
        # Draw multiple arcs for smooth effect
        for i in range(8):
            start_angle = self.angle + (i * 45)
            opacity = int(255 * (i + 1) / 8)
            
            # Create arc
            x1 = center - radius
            y1 = center - radius
            x2 = center + radius
            y2 = center + radius
            
            self.canvas.create_arc(x1, y1, x2, y2,
                                  start=start_angle, extent=30,
                                  outline=self.color, width=4,
                                  style=tk.ARC)
        
        self.angle = (self.angle + 10) % 360
        self.animation_id = self.after(50, self._animate)


class PulseButton(ctk.CTkButton):
    """Button with pulse animation effect"""
    
    def __init__(self, *args, pulse_color=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pulse_color = pulse_color or "#38bdf8"
        self.original_fg = kwargs.get('fg_color', '#0284c7')
        self.is_pulsing = False
        self.pulse_id = None
        self.pulse_state = 0
        
    def start_pulse(self):
        """Start pulsing animation"""
        self.is_pulsing = True
        self._pulse()
        
    def stop_pulse(self):
        """Stop pulsing animation"""
        self.is_pulsing = False
        if self.pulse_id:
            self.after_cancel(self.pulse_id)
            self.pulse_id = None
        self.configure(fg_color=self.original_fg)
    
    def _pulse(self):
        """Animate the pulse effect"""
        if not self.is_pulsing:
            return
        
        # Oscillate between original and pulse color
        self.pulse_state = (self.pulse_state + 0.1) % (2 * math.pi)
        intensity = (math.sin(self.pulse_state) + 1) / 2  # 0 to 1
        
        # Interpolate color (simplified)
        if intensity > 0.5:
            self.configure(fg_color=self.pulse_color)
        else:
            self.configure(fg_color=self.original_fg)
        
        self.pulse_id = self.after(100, self._pulse)


class ProgressOverlay(ctk.CTkFrame):
    """Full-screen progress overlay with loading indicator"""
    
    def __init__(self, parent, message="Loading...", **kwargs):
        super().__init__(parent, fg_color=("#000000", "#000000"), **kwargs)
        self.configure(corner_radius=0)
        
        # Semi-transparent effect
        self.attributes = {'alpha': 0.7}
        
        # Center container
        container = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Loading spinner
        self.spinner = LoadingSpinner(container, size=60)
        self.spinner.pack(pady=(30, 10))
        
        # Message label
        self.message_label = ctk.CTkLabel(container, text=message,
                                         font=("Segoe UI", 14),
                                         text_color="#0f172a")
        self.message_label.pack(pady=(10, 30), padx=40)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(container, width=300, height=8,
                                          corner_radius=4,
                                          progress_color="#0284c7")
        self.progress.pack(pady=(0, 30), padx=40)
        self.progress.set(0)
        
    def show(self):
        """Show the overlay and start animation"""
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()
        self.spinner.start()
        
    def hide(self):
        """Hide the overlay and stop animation"""
        self.spinner.stop()
        self.place_forget()
    
    def update_message(self, message):
        """Update the loading message"""
        self.message_label.configure(text=message)
        
    def update_progress(self, value):
        """Update progress bar (0.0 to 1.0)"""
        self.progress.set(value)


class FadeInFrame(ctk.CTkFrame):
    """Frame that fades in when shown"""
    
    def __init__(self, parent, fade_duration=300, **kwargs):
        super().__init__(parent, **kwargs)
        self.fade_duration = fade_duration
        self.fade_steps = 20
        self.current_step = 0
        self.fade_id = None
        
    def fade_in(self):
        """Fade in the frame"""
        self.current_step = 0
        self._do_fade_in()
        
    def _do_fade_in(self):
        """Perform fade in animation"""
        if self.current_step >= self.fade_steps:
            return
        
        # Calculate opacity (not directly supported in CTk, so we simulate with visibility)
        self.current_step += 1
        
        # Just show it (CTk doesn't support alpha on frames easily)
        if self.current_step == 1:
            self.pack(fill="both", expand=True)
        
        step_duration = self.fade_duration // self.fade_steps
        self.fade_id = self.after(step_duration, self._do_fade_in)


class AnimatedProgressBar(ctk.CTkProgressBar):
    """Progress bar with smooth animation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_value = 0
        self.current_value = 0
        self.animation_id = None
        
    def animate_to(self, target_value, duration=500):
        """Animate to target value smoothly"""
        self.target_value = max(0, min(1, target_value))
        self.current_value = self.get()
        
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        self.steps = 30
        self.step_duration = duration // self.steps
        self.current_step = 0
        
        self._animate_step()
    
    def _animate_step(self):
        """Perform one animation step"""
        if self.current_step >= self.steps:
            self.set(self.target_value)
            return
        
        # Ease-out animation
        progress = self.current_step / self.steps
        eased_progress = 1 - (1 - progress) ** 3  # Cubic ease-out
        
        new_value = self.current_value + (self.target_value - self.current_value) * eased_progress
        self.set(new_value)
        
        self.current_step += 1
        self.animation_id = self.after(self.step_duration, self._animate_step)


class ToastNotification(ctk.CTkFrame):
    """Toast notification that slides in from top"""
    
    def __init__(self, parent, message, duration=3000, type="info"):
        super().__init__(parent, corner_radius=10)
        
        # Color based on type
        colors = {
            "info": "#0284c7",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
        
        self.configure(fg_color=colors.get(type, "#0284c7"))
        
        # Icon based on type
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        icon_label = ctk.CTkLabel(self, text=icons.get(type, "ℹ️"),
                                 font=("Segoe UI", 16))
        icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        message_label = ctk.CTkLabel(self, text=message,
                                     font=("Segoe UI", 12),
                                     text_color="white")
        message_label.pack(side="left", padx=(5, 15), pady=10)
        
        self.duration = duration
        self.slide_steps = 20
        self.current_step = 0
        
    def show(self):
        """Show toast with slide-in animation"""
        # Position at top center, initially above screen
        self.place(relx=0.5, y=-100, anchor="n")
        self._slide_in()
        
    def _slide_in(self):
        """Slide in from top"""
        if self.current_step >= self.slide_steps:
            # Wait for duration then slide out
            self.after(self.duration, self._slide_out)
            return
        
        # Ease-out animation
        progress = self.current_step / self.slide_steps
        eased_progress = 1 - (1 - progress) ** 3
        
        y_pos = -100 + (120 * eased_progress)  # Slide to y=20
        self.place(relx=0.5, y=y_pos, anchor="n")
        
        self.current_step += 1
        self.after(20, self._slide_in)
    
    def _slide_out(self):
        """Slide out to top"""
        self.current_step = 0
        self._do_slide_out()
    
    def _do_slide_out(self):
        """Perform slide out animation"""
        if self.current_step >= self.slide_steps:
            self.destroy()
            return
        
        progress = self.current_step / self.slide_steps
        eased_progress = progress ** 3  # Cubic ease-in
        
        y_pos = 20 - (120 * eased_progress)
        self.place(relx=0.5, y=y_pos, anchor="n")
        
        self.current_step += 1
        self.after(20, self._do_slide_out)
