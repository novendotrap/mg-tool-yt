import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from scripts.config_manager import ConfigManager
try:
    from styles.styles import Style, adjust_brightness
except ImportError:
    # Fallback si styles.py no existe
    class Style:
        BG_PRIMARY = "#000000"
        BG_SECONDARY = "#111111"
        BG_TERTIARY = "#1a1a1a"
        BORDER_LIGHT = "#222222"
        BORDER_MEDIUM = "#333333"
        TEXT_PRIMARY = "#e0e0e0"
        TEXT_SECONDARY = "#888888"
        TEXT_SUCCESS = "#27ae60"
        TEXT_ERROR = "#e74c3c"
        FONT_FAMILY = "SF Pro Display"
    
    def adjust_brightness(hex_color, adjustment):
        hex_color = hex_color.lstrip('#')
        r = max(0, min(255, int(hex_color[0:2], 16) + adjustment))
        g = max(0, min(255, int(hex_color[2:4], 16) + adjustment))
        b = max(0, min(255, int(hex_color[4:6], 16) + adjustment))
        return f"#{r:02x}{g:02x}{b:02x}"

class ConfigWindow:
    def __init__(self, parent=None):
        self.config_manager = ConfigManager()
        self.root = ctk.CTkToplevel(parent) if parent else ctk.CTk()
        try:
            from scripts.window_icon import apply_window_icon
            apply_window_icon(self.root)
            # Also ensure parent's icon matches (some platforms prefer the main window)
            if parent is not None:
                try:
                    apply_window_icon(parent)
                except Exception:
                    pass
        except Exception:
            pass
        self.root.title("Configuration - MG Tools")
        self.root.geometry("500x480")
        self.root.resizable(False, False)
        self.root.configure(fg_color=Style.BG_PRIMARY)
        
        self.center_window()
        self.build_ui()
        # Ensure the Toplevel keeps the custom icon: some CTK operations
        # may re-create decorations briefly; reapply icon after short delays.
        try:
            from scripts.window_icon import apply_window_icon
            try:
                # set transient and modal behavior when there is a parent
                if parent is not None:
                    try:
                        self.root.transient(parent)
                    except Exception:
                        pass
                    try:
                        self.root.grab_set()
                    except Exception:
                        pass

                # reapply icon shortly after construction to override CTK redraws
                self.root.after(150, lambda: apply_window_icon(self.root))
                self.root.after(600, lambda: apply_window_icon(self.root))
                # also reapply on the parent (if any)
                if parent is not None:
                    self.root.after(200, lambda: apply_window_icon(parent))
            except Exception:
                pass
        except Exception:
            pass
        if not parent:
            self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def build_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=Style.BG_PRIMARY,
            border_width=0
        )
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            height=70
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Configuration",
            font=(Style.FONT_FAMILY, 22, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Configure application paths",
            font=(Style.FONT_FAMILY, 12),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # Settings frame
        settings_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=8,
            fg_color=Style.BG_SECONDARY,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        settings_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Fiddler Path
        fiddler_label = ctk.CTkLabel(
            settings_frame,
            text="Fiddler Folder (AutoResponder.xml):",
            font=(Style.FONT_FAMILY, 13),
            text_color=Style.TEXT_PRIMARY
        )
        fiddler_label.pack(anchor="w", pady=(16, 8), padx=16)
        
        fiddler_row = ctk.CTkFrame(settings_frame, fg_color=Style.BG_SECONDARY)
        fiddler_row.pack(fill="x", padx=16, pady=(0, 16))
        
        self.fiddler_entry = ctk.CTkEntry(
            fiddler_row,
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            height=36
        )
        self.fiddler_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.fiddler_entry.insert(0, self.config_manager.get_fiddler_path())
        
        fiddler_btn = ctk.CTkButton(
            fiddler_row,
            text="Select",
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BTN_SECONDARY,
            text_color=Style.TEXT_PRIMARY,
            corner_radius=6,
            width=80,
            height=36,
            hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            command=self.select_fiddler_path
        )
        fiddler_btn.pack(side="right")
        
        # Fiddler Executable Path
        fiddler_exec_label = ctk.CTkLabel(
            settings_frame,
            text="Fiddler Executable (.exe):",
            font=(Style.FONT_FAMILY, 13),
            text_color=Style.TEXT_PRIMARY
        )
        fiddler_exec_label.pack(anchor="w", pady=(0, 8), padx=16)
        
        fiddler_exec_row = ctk.CTkFrame(settings_frame, fg_color=Style.BG_SECONDARY)
        fiddler_exec_row.pack(fill="x", padx=16, pady=(0, 16))
        
        self.fiddler_exec_entry = ctk.CTkEntry(
            fiddler_exec_row,
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            height=36
        )
        self.fiddler_exec_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.fiddler_exec_entry.insert(0, self.config_manager.get_fiddler_executable_path())
        
        fiddler_exec_btn = ctk.CTkButton(
            fiddler_exec_row,
            text="Select",
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BTN_SECONDARY,
            text_color=Style.TEXT_PRIMARY,
            corner_radius=6,
            width=80,
            height=36,
            hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            command=self.select_fiddler_executable
        )
        fiddler_exec_btn.pack(side="right")
        
        # Mundo Gaturro Cache Path
        mg_label = ctk.CTkLabel(
            settings_frame,
            text="Mundo Gaturro Cache Folder:",
            font=(Style.FONT_FAMILY, 13),
            text_color=Style.TEXT_PRIMARY
        )
        mg_label.pack(anchor="w", pady=(0, 8), padx=16)
        
        mg_row = ctk.CTkFrame(settings_frame, fg_color=Style.BG_SECONDARY)
        mg_row.pack(fill="x", padx=16, pady=(0, 16))
        
        self.mg_entry = ctk.CTkEntry(
            mg_row,
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            height=36
        )
        self.mg_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.mg_entry.insert(0, self.config_manager.get_mundo_gaturro_cache_path())
        
        mg_btn = ctk.CTkButton(
            mg_row,
            text="Select",
            font=(Style.FONT_FAMILY, 11),
            fg_color=Style.BTN_SECONDARY,
            text_color=Style.TEXT_PRIMARY,
            corner_radius=6,
            width=80,
            height=36,
            hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            command=self.select_mg_path
        )
        mg_btn.pack(side="right")
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        btn_frame.pack(fill="x", pady=(0, 10))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Configuration",
            font=(Style.FONT_FAMILY, 13, "normal"),
            fg_color=Style.BTN_TERTIARY,
            text_color=Style.TEXT_PRIMARY,
            corner_radius=8,
            height=40,
            hover_color=adjust_brightness(Style.BTN_TERTIARY, 40),
            command=self.save_config
        )
        save_btn.pack(fill="x", pady=(0, 8))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            font=(Style.FONT_FAMILY, 11),
            fg_color="transparent",
            text_color=Style.TEXT_SECONDARY,
            corner_radius=6,
            height=36,
            hover_color=Style.BG_TERTIARY,
            border_width=1,
            border_color=Style.BORDER_MEDIUM,
            command=self.root.destroy
        )
        cancel_btn.pack(fill="x")
    
    def select_fiddler_path(self):
        path = filedialog.askdirectory(title="Select Fiddler folder")
        if path:
            self.fiddler_entry.delete(0, ctk.END)
            self.fiddler_entry.insert(0, path)
            
    def select_fiddler_executable(self):
        path = filedialog.askopenfilename(
            title="Select Fiddler Executable",
            filetypes=[("Executables", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.fiddler_exec_entry.delete(0, ctk.END)
            self.fiddler_exec_entry.insert(0, path)
    
    def select_mg_path(self):
        path = filedialog.askdirectory(title="Select Mundo Gaturro cache folder")
        if path:
            self.mg_entry.delete(0, ctk.END)
            self.mg_entry.insert(0, path)
    
    def save_config(self):
        fiddler_path = self.fiddler_entry.get().strip()
        fiddler_exec_path = self.fiddler_exec_entry.get().strip()
        mg_path = self.mg_entry.get().strip()
        
        if not fiddler_path:
            messagebox.showerror("Error", "Fiddler path cannot be empty.")
            return
            
        if not fiddler_exec_path:
            messagebox.showerror("Error", "Fiddler executable path cannot be empty.")
            return
        
        if not mg_path:
            messagebox.showerror("Error", "Mundo Gaturro cache path cannot be empty.")
            return
        
        self.config_manager.set_fiddler_path(fiddler_path)
        self.config_manager.set_fiddler_executable_path(fiddler_exec_path)
        self.config_manager.set_mundo_gaturro_cache_path(mg_path)
        
        messagebox.showinfo(
            title="Success", 
            message="Configuration saved successfully."
        )
        self.root.destroy()