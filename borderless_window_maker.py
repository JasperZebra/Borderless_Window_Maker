import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con

class BorderlessWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Borderless Window Maker")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.secondary_bg = "#2d2d2d"
        self.hover_color = "#3e3e3e"
        self.success_color = "#4ec9b0"
        self.warning_color = "#ce9178"
        
        self.root.configure(bg=self.bg_color)
        
        # Main container with padding
        main_container = tk.Frame(root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title with modern font
        title_label = tk.Label(main_container, text="Borderless Window Maker", 
                              font=("Segoe UI", 24, "bold"),
                              bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle = tk.Label(main_container, text="Remove window borders with one click",
                           font=("Segoe UI", 10),
                           bg=self.bg_color, fg="#a0a0a0")
        subtitle.pack(pady=(0, 30))
        
        # Refresh button with modern styling
        refresh_btn = tk.Button(main_container, text="⟳ Refresh Window List", 
                               command=self.refresh_windows, 
                               font=("Segoe UI", 10),
                               bg=self.secondary_bg,
                               fg=self.fg_color,
                               activebackground=self.hover_color,
                               activeforeground=self.fg_color,
                               relief=tk.FLAT,
                               cursor="hand2",
                               padx=20, pady=8,
                               border=0)
        refresh_btn.pack(pady=(0, 15))
        self._bind_hover(refresh_btn, self.secondary_bg, self.hover_color)
        
        # Window list container with modern styling
        list_container = tk.Frame(main_container, bg=self.secondary_bg, highlightthickness=1,
                                 highlightbackground="#3e3e3e")
        list_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Scrollbar with custom styling
        scrollbar = tk.Scrollbar(list_container, troughcolor=self.secondary_bg,
                                bg=self.bg_color, activebackground=self.accent_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 2), pady=2)
        
        # Listbox with modern styling
        self.window_listbox = tk.Listbox(list_container, 
                                         yscrollcommand=scrollbar.set,
                                         font=("Segoe UI", 10),
                                         bg=self.secondary_bg,
                                         fg=self.fg_color,
                                         selectbackground=self.accent_color,
                                         selectforeground=self.fg_color,
                                         activestyle='none',
                                         relief=tk.FLAT,
                                         highlightthickness=0,
                                         border=0)
        self.window_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.config(command=self.window_listbox.yview)
        
        # Store window handles
        self.window_handles = {}
        
        # Buttons container
        button_container = tk.Frame(main_container, bg=self.bg_color)
        button_container.pack(fill=tk.X)
        
        # Make borderless button (primary action)
        make_borderless_btn = tk.Button(button_container, text="✓ Make Borderless", 
                                       command=self.make_selected_borderless,
                                       font=("Segoe UI", 11, "bold"),
                                       bg=self.success_color,
                                       fg="#000000",
                                       activebackground="#5eddc3",
                                       activeforeground="#000000",
                                       relief=tk.FLAT,
                                       cursor="hand2",
                                       padx=30, pady=12,
                                       border=0)
        make_borderless_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self._bind_hover(make_borderless_btn, self.success_color, "#5eddc3")
        
        # Restore button (secondary action)
        restore_btn = tk.Button(button_container, text="↺ Restore Borders", 
                               command=self.restore_selected_borders,
                               font=("Segoe UI", 11),
                               bg=self.secondary_bg,
                               fg=self.fg_color,
                               activebackground=self.hover_color,
                               activeforeground=self.fg_color,
                               relief=tk.FLAT,
                               cursor="hand2",
                               padx=30, pady=12,
                               border=0)
        restore_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self._bind_hover(restore_btn, self.secondary_bg, self.hover_color)
        
        # Status bar at bottom
        self.status_label = tk.Label(main_container, text="Ready",
                                     font=("Segoe UI", 9),
                                     bg=self.bg_color, fg="#808080")
        self.status_label.pack(pady=(15, 0))
        
        # Initial refresh
        self.refresh_windows()
        
    def _bind_hover(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def update_status(self, message, color="#808080"):
        """Update status bar message"""
        self.status_label.config(text=message, fg=color)
        
    def get_all_windows(self):
        """Get all visible windows with titles"""
        windows = {}
        
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Only include windows with titles
                    windows[title] = hwnd
            return True
        
        win32gui.EnumWindows(callback, None)
        return windows
    
    def refresh_windows(self):
        """Refresh the list of windows"""
        self.window_listbox.delete(0, tk.END)
        self.window_handles = self.get_all_windows()
        
        for title in sorted(self.window_handles.keys()):
            self.window_listbox.insert(tk.END, title)
        
        self.update_status(f"Found {len(self.window_handles)} windows", "#4ec9b0")
    
    def make_selected_borderless(self):
        """Make the selected window borderless"""
        selection = self.window_listbox.curselection()
        if not selection:
            self.update_status("Please select a window first", "#ce9178")
            self._show_modern_message("No Selection", "Please select a window from the list first!", "warning")
            return
        
        window_title = self.window_listbox.get(selection[0])
        hwnd = self.window_handles.get(window_title)
        
        if not hwnd:
            self.update_status("Error: Window not found", "#f48771")
            self._show_modern_message("Error", "Window handle not found!", "error")
            return
        
        try:
            # Get current style
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            
            # Remove title bar and borders
            style = style & ~win32con.WS_CAPTION & ~win32con.WS_THICKFRAME
            
            # Apply new style
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            
            # Refresh window
            win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                                win32con.SWP_FRAMECHANGED | 
                                win32con.SWP_NOMOVE | 
                                win32con.SWP_NOSIZE | 
                                win32con.SWP_NOZORDER)
            
            self.update_status(f"Successfully made borderless: {window_title}", "#4ec9b0")
            self._show_modern_message("Success", f"'{window_title}' is now borderless!", "success")
        except Exception as e:
            self.update_status("Error occurred", "#f48771")
            self._show_modern_message("Error", f"Failed to make window borderless:\n{str(e)}", "error")
    
    def restore_selected_borders(self):
        """Restore borders to the selected window"""
        selection = self.window_listbox.curselection()
        if not selection:
            self.update_status("Please select a window first", "#ce9178")
            self._show_modern_message("No Selection", "Please select a window from the list first!", "warning")
            return
        
        window_title = self.window_listbox.get(selection[0])
        hwnd = self.window_handles.get(window_title)
        
        if not hwnd:
            self.update_status("Error: Window not found", "#f48771")
            self._show_modern_message("Error", "Window handle not found!", "error")
            return
        
        try:
            # Get current style
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            
            # Add back title bar and borders
            style = style | win32con.WS_CAPTION | win32con.WS_THICKFRAME
            
            # Apply new style
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            
            # Refresh window
            win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                                win32con.SWP_FRAMECHANGED | 
                                win32con.SWP_NOMOVE | 
                                win32con.SWP_NOSIZE | 
                                win32con.SWP_NOZORDER)
            
            self.update_status(f"Successfully restored borders: {window_title}", "#4ec9b0")
            self._show_modern_message("Success", f"Borders restored for '{window_title}'!", "success")
        except Exception as e:
            self.update_status("Error occurred", "#f48771")
            self._show_modern_message("Error", f"Failed to restore borders:\n{str(e)}", "error")
    
    def _show_modern_message(self, title, message, msg_type="info"):
        """Show modern styled message box"""
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BorderlessWindowApp(root)
    root.mainloop()