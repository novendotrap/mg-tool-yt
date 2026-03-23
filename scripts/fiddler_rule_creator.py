import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil
import psutil
from scripts.swf_processor import SWFProcessor
from scripts.window_icon import apply_window_icon
import customtkinter as ctk
import base64
from scripts.config_manager import ConfigManager

# Import styles
try:
    from styles.styles import Style, adjust_brightness, create_button, create_entry
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
        BTN_PRIMARY = "#2a2a2a"
        BTN_SECONDARY = "#333333"
        BTN_TERTIARY = "#3a3a3a"
        FONT_FAMILY = "SF Pro Display"
        FONT_SIZE_XL = 28
        FONT_SIZE_L = 22
        FONT_SIZE_M = 14
        FONT_SIZE_S = 12
        FONT_SIZE_XS = 11
        RADIUS_L = 12
        RADIUS_M = 8
        RADIUS_S = 6
    
    def adjust_brightness(hex_color, adjustment):
        hex_color = hex_color.lstrip('#')
        r = max(0, min(255, int(hex_color[0:2], 16) + adjustment))
        g = max(0, min(255, int(hex_color[2:4], 16) + adjustment))
        b = max(0, min(255, int(hex_color[4:6], 16) + adjustment))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_button(parent, text, command, color=Style.BTN_SECONDARY, height=36, font_size=11):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=(Style.FONT_FAMILY, font_size),
            corner_radius=Style.RADIUS_S,
            height=height,
            border_width=0,
            fg_color=color,
            hover_color=adjust_brightness(color, 40),
            text_color=Style.TEXT_PRIMARY
        )
    
    def create_entry(parent, placeholder="", width=300, height=36):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            corner_radius=Style.RADIUS_S,
            width=width,
            height=height,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY
        )

class FiddlerRuleCreator:
    def __init__(self):
        self.rules = []
        self.config_manager = ConfigManager()
        self.fiddler_rules_path = self.get_fiddler_rules_path()
        self.swf_processor = SWFProcessor()
        self.current_qty = 1
    
    def get_fiddler_rules_path(self):
        return os.path.join(self.config_manager.get_fiddler_path(), "AutoResponder.xml")
    
    def create_main_panel(self):
        self.root = ctk.CTk()
        self.root.title("MG Tools")
        self.root.geometry("400x580")
        self.root.resizable(False, False)
        self.root.configure(fg_color=Style.BG_PRIMARY)
        try:
            apply_window_icon(self.root)
        except Exception:
            pass
        self.center_window()
        
        # Frame principal
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
            height=80
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header_frame,
            text="MG Tools",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XL, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Fiddler Rules Manager",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="both", expand=True, pady=10)
        
        # Buttons
        buttons_data = [
            ("Apply to Mundo Gaturro", self.aplicar_en_mundo_gaturro, Style.BTN_PRIMARY),
            ("Extract Objects", self.sacar_objetos, Style.BTN_SECONDARY),
            ("Back to Launcher", self.volver_al_launcher, Style.BTN_TERTIARY),
        ]
        
        for text, command, color in buttons_data:
            btn = create_button(
                buttons_frame,
                text=text,
                command=command,
                color=color,
                height=48,
                font_size=13
            )
            btn.pack(fill="x", pady=4)
        
        # Footer
        footer_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            height=30
        )
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        author = ctk.CTkLabel(
            footer_frame,
            text="naw • fiddler tools",
            font=(Style.FONT_FAMILY, 10),
            text_color="#444444"
        )
        author.pack(side="right")
        
        self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def center_sub_window(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def aplicar_en_mundo_gaturro(self):
        self.root.destroy()
        self.create_aplicar_reglas_panel()
    
    def sacar_objetos(self):
        self.root.destroy()
        self.create_sacar_objetos_panel()
    
    def volver_al_launcher(self):
        self.root.destroy()
        from run import ModernLauncher
        ModernLauncher()
    
    def trucar(self):
        self.root.destroy()
        from scripts.trucar_launcher import TrucarLauncher
        app = TrucarLauncher()
        app.start()
    
    def trucar_tiendas(self):
        self.root.destroy()
        from scripts.trucar_tiendas import TrucarTiendasLauncher
        app = TrucarTiendasLauncher()
        app.start()
    
    def get_latest_output_file(self):
        candidates = []
        base = Path("output_sacar_objetos")
        folders = ["exacts", "objetos", "trucados"]
        for folder in folders:
            dir_path = base / folder
            if dir_path.exists() and dir_path.is_dir():
                for p in dir_path.iterdir():
                    if p.is_file():
                        try:
                            mtime = p.stat().st_mtime
                            candidates.append((mtime, p))
                        except Exception:
                            continue
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0], reverse=True)
        try:
            return str(candidates[0][1].resolve())
        except Exception:
            return str(candidates[0][1])
    
    def normalize_lola_file(self, path):
        try:
            p = Path(path)
            if 'objetos' in p.parts:
                return str(p)
            if 'exacts' in p.parts and p.name.endswith('_exact.txt'):
                base = p.name[:-len('_exact.txt')]
                objetos_path = Path('output_sacar_objetos') / 'objetos' / f"{base}_objetos.txt"
                if objetos_path.exists():
                    return str(objetos_path.resolve())
            return str(p)
        except Exception:
            return path
    
    def get_latest_swf_in_cache(self):
        base = Path("swf_cache")
        if not base.exists():
            return None
        candidates = []
        for p in base.rglob('*.swf'):
            try:
                candidates.append((p.stat().st_mtime, p))
            except Exception:
                continue
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0], reverse=True)
        return str(candidates[0][1].resolve())
    
    def create_aplicar_reglas_panel(self):
        self.ar_root = ctk.CTk()
        self.ar_root.title("Apply Rules - MG Tools")
        self.ar_root.geometry("600x700")
        self.ar_root.resizable(False, False)
        self.ar_root.configure(fg_color=Style.BG_PRIMARY)
        try:
            apply_window_icon(self.ar_root)
        except Exception:
            pass
        self.center_sub_window(self.ar_root, 600, 700)
        
        # Main container with scroll
        main_container = ctk.CTkScrollableFrame(
            self.ar_root,
            corner_radius=0,
            fg_color=Style.BG_PRIMARY,
            border_width=0
        )
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent",
            height=70
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Apply Rules",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_L, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Apply custom rules to Mundo Gaturro",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # Config section
        config_frame = ctk.CTkFrame(
            main_container,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_SECONDARY,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        config_frame.pack(fill="x", pady=10)
        
        # Lola section
        lola_label = ctk.CTkLabel(
            config_frame,
            text="Lola Rule (required):",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        lola_label.pack(anchor="w", pady=(16, 4), padx=16)
        
        lola_info = ctk.CTkLabel(
            config_frame,
            text="URL: cdn-ar.mundogaturro.com/juego/npc/lola.npc",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        lola_info.pack(anchor="w", padx=16, pady=(0, 8))
        
        lola_row = ctk.CTkFrame(config_frame, fg_color=Style.BG_SECONDARY, corner_radius=Style.RADIUS_S)
        lola_row.pack(fill="x", padx=16, pady=(0, 12))
        
        latest = self.get_latest_output_file()
        if latest:
            default_lola_value = self.normalize_lola_file(latest)
        else:
            default_lola_value = "No file selected"
        self.lola_file_path = ctk.StringVar(value=default_lola_value)
        
        lola_file_entry = ctk.CTkEntry(
            lola_row,
            textvariable=self.lola_file_path,
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            corner_radius=Style.RADIUS_S,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            state="disabled",
            height=36
        )
        lola_file_entry.pack(side="left", padx=(0, 8), pady=8, fill="x", expand=True)
        
        lola_file_btn = create_button(
            lola_row,
            text="Select File",
            command=self.seleccionar_archivo_lola,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        lola_file_btn.pack(side="left", pady=8)
        
        # SWF rules section
        swf_rules_label = ctk.CTkLabel(
            config_frame,
            text="Additional SWF Rules:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        swf_rules_label.pack(anchor="w", padx=16, pady=(0, 8))
        
        self.swf_rules = []
        self.swf_rules_frame = ctk.CTkScrollableFrame(
            config_frame,
            fg_color=Style.BG_SECONDARY,
            corner_radius=Style.RADIUS_S,
            height=140,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        self.swf_rules_frame.pack(fill="x", padx=16, pady=(0, 12))
        
        add_swf_btn = create_button(
            config_frame,
            text="+ Add SWF Rule",
            command=self.agregar_regla_swf,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        add_swf_btn.pack(anchor="w", padx=16, pady=(0, 12))
        
        # Actions section
        separator = ctk.CTkFrame(
            main_container,
            height=1,
            fg_color=Style.BORDER_LIGHT
        )
        separator.pack(fill="x", pady=(10, 15))
        
        action_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )
        action_frame.pack(fill="x", pady=(0, 20))
        
        self.execute_btn = create_button(
            action_frame,
            text="Execute Configuration",
            command=self.ejecutar_configuracion_thread,
            color=Style.BTN_TERTIARY,
            height=42,
            font_size=13
        )
        self.execute_btn.pack(fill="x", pady=(0, 8))
        
        back_btn = ctk.CTkButton(
            action_frame,
            text="← Back to Menu",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            fg_color="transparent",
            text_color=Style.TEXT_SECONDARY,
            corner_radius=Style.RADIUS_S,
            height=36,
            hover_color=Style.BG_TERTIARY,
            border_width=1,
            border_color=Style.BORDER_MEDIUM,
            command=self.volver_al_menu_desde_reglas
        )
        back_btn.pack(fill="x")
        
        # Results section
        results_label = ctk.CTkLabel(
            main_container,
            text="Execution Log:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS, "normal"),
            text_color=Style.TEXT_SECONDARY
        )
        results_label.pack(anchor="w", pady=(0, 8))
        
        self.ar_results_text = ctk.CTkTextbox(
            main_container,
            font=("Consolas", Style.FONT_SIZE_XS),
            fg_color=Style.BG_SECONDARY,
            text_color=Style.TEXT_PRIMARY,
            height=120,
            corner_radius=Style.RADIUS_S,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        self.ar_results_text.pack(fill="x", pady=(0, 10))
        
        self.ar_root.mainloop()
    
    def agregar_regla_swf(self):
        rule_row = ctk.CTkFrame(self.swf_rules_frame, fg_color=Style.BG_TERTIARY, corner_radius=Style.RADIUS_S)
        rule_row.pack(fill="x", pady=4, padx=4)
        
        swf_name_var = ctk.StringVar()
        latest_swf = self.get_latest_swf_in_cache()
        if latest_swf:
            latest_stem = Path(latest_swf).stem
            if latest_stem.endswith("_trucado"):
                latest_stem = latest_stem[:-len("_trucado")]
            swf_name_var.set(latest_stem)
        
        swf_entry = create_entry(
            rule_row,
            placeholder="SWF name",
            width=150,
            height=30
        )
        swf_entry.configure(textvariable=swf_name_var)
        swf_entry.pack(side="left", padx=8, pady=6)
        
        file_var = ctk.StringVar(value="No file")
        file_label = ctk.CTkLabel(
            rule_row,
            textvariable=file_var,
            font=(Style.FONT_FAMILY, 10),
            text_color=Style.TEXT_SECONDARY,
            width=120
        )
        file_label.pack(side="left", padx=8)
        
        def seleccionar_archivo():
            file_path = filedialog.askopenfilename(
                title=f"Select file for {swf_name_var.get() or 'SWF'}",
                filetypes=[("All files", "*.*")]
            )
            if file_path:
                file_var.set(os.path.basename(file_path))
                file_label.configure(text_color=Style.TEXT_SUCCESS)
                rule_row.full_path = file_path
        
        file_btn = create_button(
            rule_row,
            text="File",
            command=seleccionar_archivo,
            height=30,
            font_size=10
        )
        file_btn.pack(side="left", padx=8)
        
        def eliminar_regla():
            for i, rule in enumerate(self.swf_rules):
                if rule['row'] == rule_row:
                    self.swf_rules.pop(i)
                    break
            rule_row.destroy()
        
        delete_btn = ctk.CTkButton(
            rule_row,
            text="×",
            font=(Style.FONT_FAMILY, 12, "bold"),
            fg_color=adjust_brightness(Style.BTN_TERTIARY, 10),
            text_color=Style.TEXT_SECONDARY,
            corner_radius=Style.RADIUS_S,
            width=30,
            height=30,
            hover_color=adjust_brightness(Style.BTN_TERTIARY, 30),
            command=eliminar_regla
        )
        delete_btn.pack(side="left", padx=8)
        
        rule_row.full_path = None
        if latest_swf:
            rule_row.full_path = latest_swf
            file_var.set(os.path.basename(latest_swf))
            file_label.configure(text_color=Style.TEXT_SUCCESS)
        
        self.swf_rules.append({
            'row': rule_row,
            'name_var': swf_name_var,
            'file_var': file_var
        })
    
    def create_sacar_objetos_panel(self):
        self.so_root = ctk.CTk()
        self.so_root.title("Extract Objects - MG Tools")
        self.so_root.geometry("500x600")
        self.so_root.resizable(False, False)
        self.so_root.configure(fg_color=Style.BG_PRIMARY)
        try:
            apply_window_icon(self.so_root)
        except Exception:
            pass
        self.center_sub_window(self.so_root, 500, 600)
        
        # Main frame
        main_frame = ctk.CTkFrame(
            self.so_root,
            corner_radius=0,
            fg_color=Style.BG_PRIMARY,
            border_width=0
        )
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
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
            text="Extract Objects",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_L, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Extract objects from SWF files",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # Input section
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        input_frame.pack(fill="x", pady=(0, 20))
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="SWF Name:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        input_label.pack(anchor="w", pady=(0, 8))
        
        self.swf_entry = create_entry(
            input_frame,
            placeholder="Enter SWF name",
            height=36
        )
        self.swf_entry.pack(fill="x", pady=(0, 12))
        
        # Buttons
        btns_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        btns_frame.pack(fill="x", pady=(0, 20))
        
        process_btn = create_button(
            btns_frame,
            text="Process SWF",
            command=self.procesar_swf_thread,
            color=Style.BTN_SECONDARY,
            height=40,
            font_size=12
        )
        process_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        back_btn = ctk.CTkButton(
            btns_frame,
            text="← Back",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            fg_color="transparent",
            text_color=Style.TEXT_SECONDARY,
            corner_radius=Style.RADIUS_M,
            height=40,
            hover_color=Style.BG_TERTIARY,
            border_width=1,
            border_color=Style.BORDER_MEDIUM,
            command=self.volver_al_menu
        )
        back_btn.pack(side="left", fill="x", expand=True)
        
        # Results
        results_label = ctk.CTkLabel(
            main_frame,
            text="Results:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS, "normal"),
            text_color=Style.TEXT_SECONDARY
        )
        results_label.pack(anchor="w", pady=(0, 8))
        
        self.results_text = ctk.CTkTextbox(
            main_frame,
            font=("Consolas", Style.FONT_SIZE_XS),
            fg_color=Style.BG_SECONDARY,
            text_color=Style.TEXT_PRIMARY,
            height=180,
            corner_radius=Style.RADIUS_M,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        self.results_text.pack(fill="x", pady=(0, 12))
        
        # Action buttons
        action_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        action_frame.pack(fill="x", pady=(0, 10))
        
        self.encode_btn = create_button(
            action_frame,
            text="Generate Encode",
            command=self.generar_encode,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        self.encode_btn.configure(state="disabled")
        self.encode_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        self.exact_btn = create_button(
            action_frame,
            text="Copy EXACT",
            command=self.copiar_exact,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        self.exact_btn.configure(state="disabled")
        self.exact_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        self.save_btn = create_button(
            action_frame,
            text="Save All",
            command=self.guardar_todo_sacar_objetos,
            color=Style.BTN_TERTIARY,
            height=36,
            font_size=11
        )
        self.save_btn.configure(state="disabled")
        self.save_btn.pack(side="left", fill="x", expand=True)
        
        self.current_swf_name = ""
        self.current_classes = []
        self.current_objects = []
        
        self.so_root.mainloop()
    
    def procesar_swf_thread(self):
        thread = threading.Thread(target=self.procesar_swf)
        thread.daemon = True
        thread.start()
    
    def procesar_swf(self):
        swf_name = self.swf_entry.get().strip()
        if not swf_name:
            self.mostrar_resultado("Error: Enter SWF name")
            return
        
        self.mostrar_resultado("Downloading SWF from CDN...")
        swf_file, error_msg = self.swf_processor.download_swf(swf_name)
        if not swf_file:
            self.mostrar_resultado(error_msg or "Error: Could not download SWF")
            return
        
        self.mostrar_resultado(f"SWF downloaded: {Path(swf_file).name}")
        self.mostrar_resultado("Extracting classes from SWF...")
        classes, message = self.swf_processor.extract_classes(swf_file)
        
        if not classes:
            self.mostrar_resultado(f"Extraction error: {message}")
            return
        
        self.mostrar_resultado(f"Classes extracted: {len(classes)}")
        self.mostrar_resultado("Filtering objects...")
        combined_objects = self.swf_processor.combine_filters(classes)
        
        if not combined_objects:
            self.mostrar_resultado("No objects found")
            return
        
        self.current_swf_name = swf_name
        self.current_classes = classes
        self.current_objects = combined_objects
        
        self.mostrar_resultado(f"Objects found: {len(combined_objects)}\n")
        for i, obj in enumerate(combined_objects[:15], 1):
            self.mostrar_resultado(f"{i:2d}. {obj}")
        
        if len(combined_objects) > 15:
            self.mostrar_resultado(f"... and {len(combined_objects) - 15} more objects")
        
        self.so_root.after(0, self.habilitar_botones)
        self.mostrar_resultado("\nAvailable options:")
        self.mostrar_resultado("- GENERATE ENCODE")
        self.mostrar_resultado("- COPY EXACT COMMAND")
        self.mostrar_resultado("- SAVE ALL FILES")
    
    def habilitar_botones(self):
        self.encode_btn.configure(state='normal')
        self.exact_btn.configure(state='normal')
        self.save_btn.configure(state='normal')
    
    def mostrar_resultado(self, texto):
        self.so_root.after(0, lambda: self.results_text.insert(tk.END, texto + "\n"))
        self.so_root.after(0, lambda: self.results_text.see(tk.END))
    
    def generar_encode(self):
        if not self.current_objects:
            messagebox.showerror("Error", "No objects to generate encode")
            return
        try:
            from scripts.ctk_dialogs import ask_integer
            qty = ask_integer(self.so_root, "Quantity", "Enter quantity per object:", initialvalue=1, minvalue=1)
        except Exception:
            qty = 1

        if qty is None:
            self.mostrar_resultado("Generation cancelled")
            return

        self.mostrar_resultado("Generating encode...")
        self.current_qty = qty
        encode_content = self.swf_processor.generate_encode(self.current_objects, self.current_swf_name, qty=qty)
        
        if encode_content:
            encode_base64 = base64.b64encode(encode_content.encode('utf-8')).decode('utf-8')
            self.mostrar_resultado("Encode generated (base64):")
            preview_lines = encode_content.split('\n')[:10]
            for line in preview_lines:
                self.mostrar_resultado(line)
            if len(encode_content.split('\n')) > 10:
                self.mostrar_resultado("...")
            self.current_encode = encode_base64
            self.current_encode_content = encode_content
            self.mostrar_resultado("Use SAVE ALL to export the encode")
        else:
            self.mostrar_resultado("Error generating encode")
    
    def copiar_exact(self):
        if not self.current_swf_name:
            messagebox.showerror("Error", "No processed SWF")
            return
        
        exact_command = self.swf_processor.get_exact_command(self.current_swf_name)
        self.so_root.clipboard_clear()
        self.so_root.clipboard_append(exact_command)
        self.mostrar_resultado(f"EXACT command copied: {exact_command}")
    
    def guardar_todo_sacar_objetos(self):
        if not self.current_objects:
            messagebox.showerror("Error", "No data to save")
            return
        
        output_dir = Path("output_sacar_objetos")
        objetos_dir = output_dir / "objetos"
        exacts_dir = output_dir / "exacts"
        
        output_dir.mkdir(exist_ok=True)
        objetos_dir.mkdir(exist_ok=True)
        exacts_dir.mkdir(exist_ok=True)
        
        safe_name = self.current_swf_name.replace("/", "_").replace("\\", "_")
        
        try:
            qty = getattr(self, 'current_qty', 1)
            encode_content = self.swf_processor.generate_encode(self.current_objects, self.current_swf_name, qty=qty)
            encode_base64 = base64.b64encode(encode_content.encode('utf-8')).decode('utf-8') if encode_content else ''
            
            exact_file = exacts_dir / f"{safe_name}_exact.txt"
            exact_command = self.swf_processor.get_exact_command(self.current_swf_name)
            with open(exact_file, 'w', encoding='utf-8') as f:
                f.write(exact_command)

            objects_file = objetos_dir / f"{safe_name}_objetos.txt"
            with open(objects_file, 'w', encoding='utf-8') as f:
                f.write(encode_base64)

            self.mostrar_resultado(f"Files saved to: {output_dir}/")
            self.mostrar_resultado(f"- {exact_file.name} (EXACT command)")
            self.mostrar_resultado(f"- {objects_file.name} (base64 encode)")

            messagebox.showinfo("Success", f"Files saved to:\n{output_dir}\n\n- exacts/ (EXACT command)\n- objetos/ (base64 encode)")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save files:\n{str(e)}")
    
    def volver_al_menu(self):
        self.so_root.destroy()
        from run import ModernLauncher
        ModernLauncher()
    
    def volver_al_menu_desde_reglas(self):
        self.ar_root.destroy()
        from run import ModernLauncher
        ModernLauncher()
    
    def seleccionar_archivo_lola(self):
        file_path = tk.filedialog.askopenfilename(
            title="Select file for Lola rule",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            normalized = self.normalize_lola_file(file_path)
            self.lola_file_path.set(normalized)
            if hasattr(self, 'ar_results_text'):
                self.ar_results_text.insert("end", f"File selected for Lola: {os.path.basename(normalized)}\n")
                self.ar_results_text.see("end")
    
    def ejecutar_configuracion_thread(self):
        thread = threading.Thread(target=self.ejecutar_configuracion_completa)
        thread.daemon = True
        thread.start()
    
    def ejecutar_configuracion_completa(self):
        self.execute_btn.configure(state='disabled', text="⏳ Executing...")
        self.mostrar_resultado_reglas("🎮 STARTING COMPLETE CONFIGURATION...")
        self.mostrar_resultado_reglas("=" * 50)
        
        lola_file = self.lola_file_path.get()
        lola_file = self.normalize_lola_file(lola_file) if lola_file else lola_file
        if not lola_file or lola_file == "No file selected":
            self.mostrar_resultado_reglas("❌ ERROR: No file selected for Lola rule")
            self.ar_root.after(0, lambda: self.execute_btn.configure(state='normal', text="Execute Configuration"))
            return
        else:
            self.mostrar_resultado_reglas(f"Using file for Lola: {os.path.basename(lola_file)}")
        
        self.mostrar_resultado_reglas("\n🔄 STEP 1: Closing Mundo Gaturro...")
        if not self.close_mundo_gaturro():
            self.mostrar_resultado_reglas("❌ Could not close Mundo Gaturro. Aborting...")
            self.ar_root.after(0, lambda: self.execute_btn.configure(state='normal', text="Execute Configuration"))
            return
        
        self.mostrar_resultado_reglas("\n🧹 STEP 2: Cleaning cache...")
        if not self.clear_mundo_gaturro_cache():
            self.mostrar_resultado_reglas("⚠️ Could not completely clean cache, but continuing...")
        
        self.mostrar_resultado_reglas("\n🎯 STEP 3: Configuring Fiddler rules...")
        self.rules = []
        
        lola_url = "https://cdn-ar.mundogaturro.com/juego/npc/lola.npc?cache=no%20cache"
        self.rules.append({
            'match': f"EXACT:{lola_url}",
            'action': lola_file,
            'enabled': 'true'
        })
        self.mostrar_resultado_reglas(f"✅ Lola rule added: {os.path.basename(lola_file)}")
        
        if hasattr(self, 'swf_rules'):
            valid_swf_rules = 0
            for i, rule_data in enumerate(self.swf_rules, 1):
                swf_name = rule_data['name_var'].get().strip()
                swf_file = getattr(rule_data['row'], 'full_path', None)
                if swf_name and swf_file:
                    exact_match = self.swf_processor.get_exact_command_with_size(swf_name)
                    self.rules.append({
                        'match': exact_match,
                        'action': swf_file,
                        'enabled': 'true'
                    })
                    self.mostrar_resultado_reglas(f"✅ SWF rule {i} added: {swf_name} -> {os.path.basename(swf_file)}")
                    valid_swf_rules += 1
            self.mostrar_resultado_reglas(f"📊 Total rules: 1 Lola + {valid_swf_rules} SWF")
        
        if self.save_rules_to_fiddler_visual():
            self.mostrar_resultado_reglas("✅ Rules saved to Fiddler successfully")
            
            self.mostrar_resultado_reglas("\n🔧 STEP 4: Restarting Fiddler...")
            if self.restart_fiddler_visual():
                self.mostrar_resultado_reglas("✅ Fiddler restarted successfully")
                
                self.mostrar_resultado_reglas("\n🎮 STEP 5: Opening Mundo Gaturro...")
                if self.open_mundo_gaturro_visual():
                    self.mostrar_resultado_reglas("✅ Mundo Gaturro opened successfully")
                    self.mostrar_resultado_reglas("\n🎉 CONFIGURATION COMPLETED SUCCESSFULLY!")
                    self.mostrar_resultado_reglas("✨ Ready to play with new rules applied")
                else:
                    self.mostrar_resultado_reglas("⚠️ Fiddler configured but could not open Mundo Gaturro")
            else:
                self.mostrar_resultado_reglas("❌ Error restarting Fiddler")
        else:
            self.mostrar_resultado_reglas("❌ Error saving rules to Fiddler")
        
        self.ar_root.after(0, lambda: self.execute_btn.configure(state='normal', text="Execute Configuration"))
    
    def close_mundo_gaturro(self):
        import subprocess, time
        # Try to locate processes related to Mundo Gaturro (MundoGaturro.exe or nw.exe instances
        # that belong to the Mundo Gaturro installation) and terminate them by PID to avoid
        # accidentally killing unrelated nw.exe processes.
        procs = self.find_mundo_gaturro_processes()
        if procs:
            self.mostrar_resultado_reglas("Closing Mundo Gaturro...")
            try:
                for p in procs:
                    try:
                        subprocess.run(["taskkill", "/f", "/pid", str(p.pid)], capture_output=True)
                    except Exception:
                        pass
                time.sleep(3)
                remaining = self.find_mundo_gaturro_processes()
                if remaining:
                    self.mostrar_resultado_reglas("Forcing close...")
                    for p in remaining:
                        try:
                            subprocess.run(["taskkill", "/f", "/pid", str(p.pid)], capture_output=True)
                        except Exception:
                            pass
                    time.sleep(2)
                self.mostrar_resultado_reglas("Mundo Gaturro closed")
                return True
            except Exception as e:
                self.mostrar_resultado_reglas(f"Error closing Mundo Gaturro: {e}")
                return False
        else:
            self.mostrar_resultado_reglas("Mundo Gaturro is not open")
            return True
    
    def clear_mundo_gaturro_cache(self):
        import shutil, os
        roaming_path = self.config_manager.get_mundo_gaturro_cache_path()
        if not os.path.exists(roaming_path):
            self.mostrar_resultado_reglas("Mundo Gaturro folder not found")
            return False
        
        if self.is_process_running('MundoGaturro'):
            self.mostrar_resultado_reglas("Mundo Gaturro is open. Cannot clean cache.")
            return False
        
        try:
            files_deleted = 0
            folders_deleted = 0
            for item in os.listdir(roaming_path):
                item_path = os.path.join(roaming_path, item)
                if os.path.isfile(item_path):
                    if item.lower() != 'cookies':
                        try:
                            os.remove(item_path)
                            self.mostrar_resultado_reglas(f"File deleted: {item}")
                            files_deleted += 1
                        except Exception as e:
                            self.mostrar_resultado_reglas(f"Could not delete {item}: {e}")
                elif os.path.isdir(item_path):
                    if item.lower() != 'cookies':
                        try:
                            shutil.rmtree(item_path)
                            self.mostrar_resultado_reglas(f"Folder deleted: {item}")
                            folders_deleted += 1
                        except Exception as e:
                            self.mostrar_resultado_reglas(f"Could not delete folder {item}: {e}")
            
            self.mostrar_resultado_reglas(f"Cache cleaned - Files: {files_deleted}, Folders: {folders_deleted}")
            return True
        except Exception as e:
            self.mostrar_resultado_reglas(f"Error cleaning cache: {e}")
            return False
    
    def is_process_running(self, process_name):
        # Backwards-compatible wrapper: return True if any Mundo Gaturro related process exists
        return len(self.find_mundo_gaturro_processes()) > 0

    def find_mundo_gaturro_processes(self):
        """Return list of psutil.Process objects that likely belong to Mundo Gaturro.
        This includes processes whose name contains 'MundoGaturro' and also `nw.exe`
        instances whose executable path or command line mentions 'Mundo'/'Gaturro'/'gaturro'.
        """
        import psutil
        matches = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    name = (proc.info.get('name') or '').lower()
                    exe = (proc.info.get('exe') or '') or ''
                    cmd = ' '.join(proc.info.get('cmdline') or []).lower()
                    # Direct MundoGaturro executable
                    if 'mundogaturro' in name or 'mundogaturro' in exe.lower() or 'mundogaturro' in cmd:
                        matches.append(proc)
                        continue
                    # NW.js (nw.exe) or node wrapper: check path/args for hints
                    if name in ('nw.exe', 'node.exe'):
                        if 'mundo gaturro' in exe.lower() or 'mundo gaturro' in cmd or 'gaturro' in exe.lower() or 'gaturro' in cmd:
                            matches.append(proc)
                            continue
                except Exception:
                    continue
        except Exception:
            return []
        return matches
    
    def mostrar_resultado_reglas(self, texto):
        self.ar_root.after(0, lambda: self.ar_results_text.insert('end', texto + "\n"))
        self.ar_root.after(0, lambda: self.ar_results_text.see('end'))
    
    def save_rules_to_fiddler_visual(self):
        import shutil, os
        from datetime import datetime
        try:
            existing_rules = self.load_existing_rules()
            self.mostrar_resultado_reglas(f"Existing rules found: {len(existing_rules)}")
            
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "-03:00"
            xml_content = f'<?xml version="1.0" encoding="utf-8"?>\n<AutoResponder LastSave="{current_time}" FiddlerVersion="5.0.20253.3311">\n'
            xml_content += '  <State Enabled="true" AcceptAllConnects="false" Fallthrough="true" UseLatency="true">\n'
            
            for rule in self.rules:
                xml_content += f'    <ResponseRule Match="{rule["match"]}" Action="{rule["action"]}" Enabled="{rule["enabled"]}"/>\n'
            
            for rule in existing_rules:
                xml_content += f'    <ResponseRule Match="{rule["match"]}" Action="{rule["action"]}" Enabled="{rule["enabled"]}"/>\n'
            
            xml_content += '  </State>\n'
            xml_content += '</AutoResponder>'
            
            if os.path.exists(self.fiddler_rules_path):
                backup_path = self.fiddler_rules_path + ".backup"
                shutil.copy2(self.fiddler_rules_path, backup_path)
                self.mostrar_resultado_reglas(f"Backup created: {backup_path}")
            
            with open(self.fiddler_rules_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            self.mostrar_resultado_reglas(f"Rules saved to: {self.fiddler_rules_path}")
            self.mostrar_resultado_reglas(f"Total rules: {len(existing_rules) + len(self.rules)}")
            return True
        except Exception as e:
            self.mostrar_resultado_reglas(f"Error saving rules: {e}")
            return False
    
    def load_existing_rules(self):
        import os
        existing_rules = []
        try:
            if os.path.exists(self.fiddler_rules_path):
                tree = ET.parse(self.fiddler_rules_path)
                root = tree.getroot()
                state_elem = root.find('State')
                if state_elem is not None:
                    for rule_elem in state_elem.findall('ResponseRule'):
                        match_attr = rule_elem.get('Match', '')
                        action_attr = rule_elem.get('Action', '')
                        if match_attr:
                            rule = {
                                'match': match_attr,
                                'action': action_attr,
                                'enabled': 'false'
                            }
                            existing_rules.append(rule)
        except Exception as e:
            print(f"Error loading existing rules: {e}")
        return existing_rules
    
    def restart_fiddler_visual(self):
        import subprocess, platform, time, os
        try:
            if platform.system() == "Windows":
                fiddler_exec = self.config_manager.get_fiddler_executable_path()
                fiddler_basename = os.path.basename(fiddler_exec) if fiddler_exec and fiddler_exec != "fiddler" else "fiddler.exe"
                
                self.mostrar_resultado_reglas("Closing Fiddler...")
                result = subprocess.run(["taskkill", "/f", "/im", fiddler_basename], capture_output=True, text=True)
                if result.returncode == 0:
                    self.mostrar_resultado_reglas("Fiddler closed")
                else:
                    self.mostrar_resultado_reglas("Fiddler was not open")
                
                time.sleep(2)
                self.mostrar_resultado_reglas("Opening Fiddler...")
                # Use shell=True if it's just 'fiddler' or run executable directly
                if fiddler_exec == "fiddler":
                    subprocess.Popen([fiddler_exec], shell=True)
                else:
                    subprocess.Popen([fiddler_exec])
                time.sleep(3)
                self.mostrar_resultado_reglas("Fiddler ready and running")
                return True
        except FileNotFoundError as e:
            self.mostrar_resultado_reglas(f"Error restarting Fiddler: {e}")
            self.mostrar_resultado_reglas("💡 TIP: Fiddler was not found in your system PATH.")
            self.mostrar_resultado_reglas("Please go to 'Settings' and manually select your Fiddler Executable (.exe).")
            return False
        except Exception as e:
            self.mostrar_resultado_reglas(f"Error restarting Fiddler: {e}")
            return False
    
    def open_mundo_gaturro_visual(self):
        import os, subprocess
        # Try the new desktop installer location first (native exe)
        local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'gaturro-desktop', 'MundoGaturro.exe')
        if os.path.exists(local_path):
            try:
                subprocess.Popen([local_path])
                self.mostrar_resultado_reglas("Mundo Gaturro opened successfully")
                return True
            except Exception as e:
                self.mostrar_resultado_reglas(f"Error opening Mundo Gaturro: {e}")
                return False

        # Fallbacks: look for classic MundoGaturro.exe or NW.js (nw.exe) installation paths
        self.mostrar_resultado_reglas("MundoGaturro.exe not found in main path")
        alternative_paths = [
            r"C:\Program Files (x86)\MundoGaturro\MundoGaturro.exe",
            r"C:\Program Files\MundoGaturro\MundoGaturro.exe",
            r"C:\Program Files (x86)\Mundo Gaturro\nw.exe",
            r"C:\Program Files\Mundo Gaturro\nw.exe",
        ]

        # Also try nw.exe located inside the desktop install folder
        possible_nw_in_local = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'gaturro-desktop', 'nw.exe')
        alternative_paths.insert(0, possible_nw_in_local)

        for path in alternative_paths:
            if path and os.path.exists(path):
                try:
                    subprocess.Popen([path])
                    self.mostrar_resultado_reglas(f"Mundo Gaturro opened from: {path}")
                    return True
                except Exception as e:
                    self.mostrar_resultado_reglas(f"Error with alternative path {path}: {e}")

        self.mostrar_resultado_reglas("Could not find MundoGaturro executable (MundoGaturro.exe or nw.exe)")
        return False


if __name__ == "__main__":
    app = FiddlerRuleCreator()
    app.create_main_panel()