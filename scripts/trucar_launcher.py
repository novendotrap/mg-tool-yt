import customtkinter as ctk
import os
from scripts.swf_processor import SWFProcessor
from scripts.window_icon import apply_window_icon
from scripts.ctk_dialogs import create_modal

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
        TEXT_WARNING = "#f39c12"
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

PARTES_CUERPO = [
    ("hats", "sombrero"),
    ("hairs", "cabello"),
    ("mouths", "boca"),
    ("neck", "cuello"),
    ("accessories", "accesorios"),
    ("cloth", "ropa/remera"),
    ("clothBack", "parte de atras"),
    ("leg", "pierna"),
    ("foot", "pie"),
    ("arm", "brazo"),
    ("grip", "agarre"),
    ("gripFore", "agarre (la otra mano)")
]

class TrucarLauncher:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modify SWF - MG Tools")
        self.root.geometry("500x620")
        self.root.resizable(False, False)
        self.root.configure(fg_color=Style.BG_PRIMARY)
        
        try:
            apply_window_icon(self.root)
        except Exception:
            pass

        self.center_window()
        self.swf_processor = SWFProcessor()
        self.classes = []
        self.trucables = []
        self.selected_objeto = None
        self.selected_parte = None
        self.selected_objeto_poner = None
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def start(self):
        self.build_ui()
        self.root.mainloop()
    
    def build_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(
            self.root,
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
            text="Modify SWF",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_L, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Modify SWF files for custom clothing",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # Input section
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        input_frame.pack(fill="x", pady=(0, 10))
        
        swf_label = ctk.CTkLabel(
            input_frame,
            text="SWF Name:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        swf_label.pack(anchor="w", pady=(0, 8))
        
        self.swf_entry = create_entry(
            input_frame,
            placeholder="SWF name (without .swf)",
            height=36
        )
        self.swf_entry.pack(fill="x", pady=(0, 12))
        
        buscar_btn = create_button(
            input_frame,
            text="Search SWF",
            command=self.buscar_swf,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=12
        )
        buscar_btn.pack(fill="x", pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY,
            height=30
        )
        self.status_label.pack(fill="x", pady=(0, 10))
        
        # Container for dynamic content
        self.dynamic_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        self.dynamic_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        nav_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        volver_btn = ctk.CTkButton(
            nav_frame,
            text="← Back to Menu",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            fg_color="transparent",
            text_color=Style.TEXT_SECONDARY,
            corner_radius=Style.RADIUS_S,
            height=36,
            hover_color=Style.BG_TERTIARY,
            border_width=1,
            border_color=Style.BORDER_MEDIUM,
            command=self.volver_al_menu
        )
        volver_btn.pack(fill="x")
    
    def volver_al_menu(self):
        self.root.destroy()
        from run import ModernLauncher
        ModernLauncher()
    
    def buscar_swf(self):
        swf_name = self.swf_entry.get().strip()
        if not swf_name:
            self.status_label.configure(text="Please enter a SWF name.", text_color=Style.TEXT_ERROR)
            return
        
        swf_path = os.path.join("swf_cache", f"{swf_name}.swf")
        if not os.path.exists(swf_path):
            self.status_label.configure(text="Downloading SWF...", text_color=Style.TEXT_SECONDARY)
            swf_path = self.swf_processor.download_swf(swf_name)
            if not swf_path:
                self.status_label.configure(text="Could not download SWF.", text_color=Style.TEXT_ERROR)
                return
        
        self.status_label.configure(text="Extracting objects...", text_color=Style.TEXT_SECONDARY)
        classes, msg = self.swf_processor.extract_classes(swf_path)
        if not classes:
            self.status_label.configure(text=f"Error extracting classes: {msg}", text_color=Style.TEXT_ERROR)
            return
        
        self.classes = classes
        self.trucables = self.swf_processor.combine_filters(classes)
        
        if not self.trucables:
            self.status_label.configure(text="No modifiable objects found.", text_color=Style.TEXT_ERROR)
            return
        
        self.status_label.configure(text=f"Modifiable objects found: {len(self.trucables)}", text_color=Style.TEXT_SUCCESS)
        self.mostrar_objetos_trucables()
    
    def mostrar_objetos_trucables(self):
        # Clear dynamic frame
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        # Search section
        search_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="Select Object:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        search_label.pack(anchor="w", pady=(0, 8))
        
        self.search_entry = create_entry(
            self.dynamic_frame,
            placeholder="Search object...",
            height=36
        )
        self.search_entry.pack(fill="x", pady=(0, 8))
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_trucables())
        
        self.objetos_listbox = ctk.CTkComboBox(
            self.dynamic_frame,
            values=self.trucables,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            button_color=Style.BTN_SECONDARY,
            button_hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS)
        )
        self.objetos_listbox.pack(fill="x", pady=(0, 12))
        
        # Buttons row
        buttons_frame = ctk.CTkFrame(
            self.dynamic_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        seleccionar_btn = create_button(
            buttons_frame,
            text="Select Object",
            command=self.seleccionar_objeto,
            height=32,
            font_size=11
        )
        seleccionar_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        clear_btn = create_button(
            buttons_frame,
            text="Clear Search",
            command=self.clear_search,
            color=Style.BTN_TERTIARY,
            height=32,
            font_size=11
        )
        clear_btn.pack(side="left", fill="x", expand=True)
    
    def filter_trucables(self):
        try:
            query = self.search_entry.get().strip().lower()
        except:
            query = ''
        if not query:
            filtered = self.trucables
        else:
            filtered = [t for t in self.trucables if query in t.lower()]
        if not filtered:
            filtered = ["(no results)"]
        try:
            self.objetos_listbox.configure(values=filtered)
            if filtered and filtered[0] != "(no results)":
                self.objetos_listbox.set(filtered[0])
        except Exception:
            pass
    
    def clear_search(self):
        try:
            self.search_entry.delete(0, 'end')
            self.filter_trucables()
            self.status_label.configure(text="Search cleared", text_color=Style.TEXT_SECONDARY)
        except:
            pass
    
    def seleccionar_objeto(self):
        objeto = self.objetos_listbox.get()
        if not objeto or objeto == "(no results)":
            self.status_label.configure(text="Select an object.", text_color=Style.TEXT_ERROR)
            return
        
        self.selected_objeto = objeto
        self.status_label.configure(text=f"Object selected: {objeto}", text_color=Style.TEXT_SUCCESS)
        self.mostrar_partes_cuerpo()
    
    def mostrar_partes_cuerpo(self):
        # Clear previous content
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        partes_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="Select Body Part:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        partes_label.pack(anchor="w", pady=(0, 8))
        
        partes = [f"{k} - {v}" for k, v in PARTES_CUERPO]
        self.parte_combobox = ctk.CTkComboBox(
            self.dynamic_frame,
            values=partes,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            button_color=Style.BTN_SECONDARY,
            button_hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS)
        )
        self.parte_combobox.pack(fill="x", pady=(0, 12))
        
        seleccionar_parte_btn = create_button(
            self.dynamic_frame,
            text="Select Part",
            command=self.seleccionar_parte,
            height=36,
            font_size=11
        )
        seleccionar_parte_btn.pack(fill="x", pady=(0, 10))
    
    def seleccionar_parte(self):
        parte = self.parte_combobox.get()
        if not parte:
            self.status_label.configure(text="Select a body part.", text_color=Style.TEXT_ERROR)
            return
        
        self.selected_parte = parte.split(" - ")[0]
        self.status_label.configure(text=f"Part selected: {self.selected_parte}", text_color=Style.TEXT_SUCCESS)
        self.mostrar_objeto_poner()
    
    def mostrar_objeto_poner(self):
        # Clear previous content
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        objeto_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="Object to Apply:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        objeto_label.pack(anchor="w", pady=(0, 8))
        
        self.objeto_poner_entry = create_entry(
            self.dynamic_frame,
            placeholder="Object name (without _on)",
            height=36
        )
        self.objeto_poner_entry.pack(fill="x", pady=(0, 12))
        
        self.generar_btn = create_button(
            self.dynamic_frame,
            text="Generate Modified SWF",
            command=self.generar_y_modificar,
            color=Style.BTN_TERTIARY,
            height=40,
            font_size=12
        )
        self.generar_btn.pack(fill="x", pady=(0, 10))
    
    def generar_y_modificar(self):
        objeto_poner = self.objeto_poner_entry.get().strip()
        if not objeto_poner:
            self.status_label.configure(text="Enter object name to apply.", text_color=Style.TEXT_ERROR)
            return
        
        self.selected_objeto_poner = objeto_poner
        self.status_label.configure(text="Generating and modifying SWF...", text_color=Style.TEXT_SECONDARY)
        swf_name = self.swf_entry.get().strip()
        swf_path = os.path.join("swf_cache", f"{swf_name}.swf")
        
        if not os.path.exists(swf_path):
            self.status_label.configure(text="SWF not found for modification.", text_color=Style.TEXT_ERROR)
            return
        
        from pathlib import Path
        import shutil
        import subprocess
        import time
        import re
        
        temp_dir = Path("temp_trucar").resolve()
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        
        ffdec_bat = os.path.abspath("ffdec/ffdec.bat")
        swf_path_abs = os.path.abspath(swf_path)
        
        extract_cmd = f'"{ffdec_bat}" -export script "{temp_dir}" "{swf_path_abs}"'
        result = subprocess.run(extract_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            self.status_label.configure(text=f"Error extracting scripts: {result.stderr}", text_color=Style.TEXT_ERROR)
            return
        
        scripts_dir = temp_dir / "scripts"
        
        self.status_label.configure(text="Verifying if SWF is modifiable...", text_color=Style.TEXT_SECONDARY)
        
        cloth_mambo_file = scripts_dir / "ClothMamboAsset.as"
        
        if not cloth_mambo_file.exists():
            error_msg = "❌ This SWF cannot be modified\n\nThe SWF file does not contain the ClothMamboAsset class required for modifying clothing objects.\n\nOnly SWFs that already have this class can be modified."
            self.mostrar_mensaje_error(error_msg)
            self.status_label.configure(text="❌ SWF not modifiable - missing ClothMamboAsset", text_color=Style.TEXT_ERROR)
            return
        
        self.status_label.configure(text="✓ SWF modifiable confirmed", text_color=Style.TEXT_SUCCESS)
        
        as_file = scripts_dir / f"{self.selected_objeto}.as"
        if not as_file.exists():
            self.status_label.configure(text=f"File {self.selected_objeto}.as not found.", text_color=Style.TEXT_ERROR)
            return
        
        with open(as_file, "r", encoding="utf-8") as f:
            contenido_original = f.read()
        
        match = re.search(r'\[Embed\(source="[^"]+", symbol="([^"]+)"\)\]', contenido_original)
        if not match:
            self.status_label.configure(text="Could not extract symbol from original file.", text_color=Style.TEXT_ERROR)
            return
        symbol_original = match.group(1)
        
        codigo_as = self.generar_codigo_actionscript(symbol_original)
        with open(as_file, "w", encoding="utf-8", newline='\n') as f:
            f.write(codigo_as)
        
        time.sleep(0.5)
        
        trucados_dir = os.path.join("swf_cache", "trucados")
        encode_dir = os.path.join("output_sacar_objetos", "trucados")
        os.makedirs(trucados_dir, exist_ok=True)
        os.makedirs(encode_dir, exist_ok=True)
        
        out_swf = os.path.join(trucados_dir, f"{swf_name}_trucado.swf")
        out_swf_abs = os.path.abspath(out_swf)
        
        self.status_label.configure(text=f"Importing modified object {self.selected_objeto}...", text_color=Style.TEXT_SECONDARY)
        
        final_import_dir = temp_dir / "final_import"
        final_import_dir.mkdir(exist_ok=True)
        final_as_file = final_import_dir / f"{self.selected_objeto}.as"
        shutil.copy(as_file, final_as_file)
        
        final_import_dir_abs = os.path.abspath(final_import_dir)
        
        import_cmd = f'"{ffdec_bat}" -importScript "{swf_path_abs}" "{out_swf_abs}" "{final_import_dir_abs}"'
        result2 = subprocess.run(import_cmd, shell=True, capture_output=True, text=True)
        
        if result2.returncode != 0:
            error_msg = f"Error importing modified object:\nSTDOUT: {result2.stdout}\nSTDERR: {result2.stderr}\nCommand: {import_cmd}"
            self.mostrar_mensaje_error(error_msg)
            self.status_label.configure(text="Error importing modified object.", text_color=Style.TEXT_ERROR)
            return
        
        try:
            safe_swf = swf_name.replace("/", "_").replace("\\", "_")
            encode_path = os.path.join(encode_dir, f"{self.selected_objeto}_{safe_swf}_trucado_encode.txt")
            
            try:
                from scripts.ctk_dialogs import ask_integer
                qty = ask_integer(self.root, "Quantity", "Enter object quantity:", initialvalue=1, minvalue=1)
            except Exception:
                qty = 1

            if qty is None:
                self.status_label.configure(text="Encode generation cancelled", text_color=Style.TEXT_SECONDARY)
                return

            encode_content = self.swf_processor.generate_encode([self.selected_objeto], swf_name, qty=qty)
            
            import base64
            encode_b64 = base64.b64encode(encode_content.encode("utf-8")).decode("utf-8")
            
            with open(encode_path, "w", encoding="utf-8") as f:
                f.write(encode_b64)
            
            info_text = f"✅ Process completed\n\nModified SWF:\n{out_swf}\n\nSpecial encode:\n{encode_path}\n\nBoth files saved successfully."
            self.mostrar_mensaje_exito(info_text)
            self.status_label.configure(text="✅ Modified SWF generated successfully", text_color=Style.TEXT_SUCCESS)
            
        except Exception as e:
            self.status_label.configure(text=f"SWF generated but error saving encode: {e}", text_color=Style.TEXT_ERROR)
        
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
    
    def generar_codigo_actionscript(self, symbol):
        nombre_clase = self.selected_objeto
        parte = self.selected_parte
        objeto_poner = self.selected_objeto_poner
        
        codigo = f"""package
{{
   [Embed(source="/_assets/assets.swf", symbol="{symbol}")]
   public dynamic class {nombre_clase} extends ClothMamboAsset
   {{
      public function {nombre_clase}()
      {{
         super();
         addFrameScript(0,frame1);
      }}
      internal function frame1() : *
      {{
         clothes = {{"{parte}":"{objeto_poner}_on"}};
      }}
   }}
}}
"""
        return codigo
    
    def mostrar_mensaje_exito(self, mensaje):
        top = create_modal(self.root, "✅ Process Completed", 600, 250)
        
        frame = ctk.CTkFrame(
            top,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_SECONDARY,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        label = ctk.CTkLabel(
            frame,
            text=mensaje,
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SUCCESS,
            justify="left"
        )
        label.pack(padx=20, pady=30)
        
        btn = create_button(
            frame,
            text="Close",
            command=top.destroy,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        btn.pack(pady=10)
    
    def mostrar_mensaje_error(self, mensaje):
        top = create_modal(self.root, "❌ Error", 700, 400)
        
        frame = ctk.CTkFrame(
            top,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_SECONDARY,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        error_label = ctk.CTkLabel(
            frame,
            text="Error Details:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS, "bold"),
            text_color=Style.TEXT_ERROR
        )
        error_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        text = ctk.CTkTextbox(
            frame,
            width=660,
            height=300,
            corner_radius=Style.RADIUS_S,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            font=("Consolas", Style.FONT_SIZE_XS)
        )
        text.pack(padx=10, pady=(0, 10))
        text.insert("1.0", mensaje)
        text.configure(state="disabled")
        
        btn = create_button(
            frame,
            text="Close",
            command=top.destroy,
            color=Style.BTN_TERTIARY,
            height=36,
            font_size=11
        )
        btn.pack(pady=5)