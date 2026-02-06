import customtkinter as ctk
import os
from scripts.swf_processor import SWFProcessor
from pathlib import Path
import shutil
import subprocess
import time
import re
from scripts.ctk_dialogs import ask_integer, ask_text, create_modal
from scripts.window_icon import apply_window_icon

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
        TEXT_INFO = "#3498db"
        BTN_PRIMARY = "#2a2a2a"
        BTN_SECONDARY = "#333333"
        BTN_TERTIARY = "#3a3a3a"
        BTN_ACCENT_BLUE = "#3498db"
        BTN_ACCENT_PURPLE = "#9b59b6"
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

SWF_OPTIONS = [
    'virtualGoods',
    'virtualGoods2',
    'virtualGoods3',
    'cassettes'
]

class TrucarTiendasLauncher:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modify Stores/Portals - MG Tools")
        self.root.geometry("500x620")
        self.root.resizable(False, False)
        self.root.configure(fg_color=Style.BG_PRIMARY)
        try:
            apply_window_icon(self.root)
        except Exception:
            pass

        self.center_window()
        self.swf_processor = SWFProcessor()
        self.trucables = []
        self.selected_objeto = None
        self.selected_swf = None
        
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
        # Main frame
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
            text="Modify Stores/Portals",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_L, "normal"),
            text_color=Style.TEXT_PRIMARY
        )
        title.pack(pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Customize store and portal behaviors",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))
        
        # SWF selection
        swf_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        swf_frame.pack(fill="x", pady=(0, 10))
        
        swf_label = ctk.CTkLabel(
            swf_frame,
            text="Select SWF:",
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
            text_color=Style.TEXT_PRIMARY
        )
        swf_label.pack(anchor="w", pady=(0, 8))
        
        self.swf_combobox = ctk.CTkComboBox(
            swf_frame,
            values=SWF_OPTIONS,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            button_color=Style.BTN_SECONDARY,
            button_hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS)
        )
        self.swf_combobox.pack(fill="x", pady=(0, 12))
        self.swf_combobox.set(SWF_OPTIONS[0])
        
        # Buttons row
        buttons_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", pady=(0, 15))
        
        buscar_btn = create_button(
            buttons_frame,
            text="Search SWF",
            command=self.buscar_swf,
            height=36,
            font_size=11
        )
        buscar_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        ver_tiendas_btn = create_button(
            buttons_frame,
            text="View Stores",
            command=self.mostrar_tiendas,
            color=Style.BTN_ACCENT_BLUE,
            height=36,
            font_size=11
        )
        ver_tiendas_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        ver_portales_btn = create_button(
            buttons_frame,
            text="View Portals",
            command=self.mostrar_portales,
            color=Style.BTN_ACCENT_PURPLE,
            height=36,
            font_size=11
        )
        ver_portales_btn.pack(side="left", fill="x", expand=True)
        
        # Status label
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
        
        # Navigation
        nav_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        nav_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        back_btn = ctk.CTkButton(
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
        back_btn.pack(fill="x")
    
    def volver_al_menu(self):
        self.root.destroy()
        from run import ModernLauncher
        ModernLauncher()
    
    def buscar_swf(self):
        swf_name = self.swf_combobox.get().strip()
        if not swf_name:
            self.status_label.configure(text="Select a SWF.", text_color=Style.TEXT_ERROR)
            return
        self.selected_swf = swf_name
        
        swf_path = os.path.join('swf_cache', f'{swf_name}.swf')
        if not os.path.exists(swf_path):
            self.status_label.configure(text="Downloading SWF...", text_color=Style.TEXT_SECONDARY)
            swf_path = self.swf_processor.download_swf(swf_name)
            if not swf_path:
                self.status_label.configure(text="Could not download SWF.", text_color=Style.TEXT_ERROR)
                return
        
        self.status_label.configure(text="Extracting objects...", text_color=Style.TEXT_SECONDARY)
        classes, msg = self.swf_processor.extract_classes(swf_path)
        if not classes:
            self.status_label.configure(text=f'Error extracting classes: {msg}', text_color=Style.TEXT_ERROR)
            return
        
        self.trucables = self.swf_processor.combine_filters(classes)
        if not self.trucables:
            self.status_label.configure(text='No modifiable objects found.', text_color=Style.TEXT_ERROR)
            return
        
        self.status_label.configure(text=f'Objects found: {len(self.trucables)}', text_color=Style.TEXT_SUCCESS)
        self.mostrar_objetos()
    
    def mostrar_objetos(self):
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
            placeholder='Search object...',
            height=36
        )
        self.search_entry.pack(fill="x", pady=(0, 8))
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_objetos())
        
        self.objetos_combobox = ctk.CTkComboBox(
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
        self.objetos_combobox.pack(fill="x", pady=(0, 12))
        
        # Select button
        seleccionar_btn = create_button(
            self.dynamic_frame,
            text='Select Object',
            command=self.seleccionar_objeto,
            height=36,
            font_size=11
        )
        seleccionar_btn.pack(fill="x", pady=(0, 10))
    
    def filter_objetos(self):
        query = ''
        try:
            query = self.search_entry.get().strip().lower()
        except Exception:
            query = ''
        if not query:
            filtered = self.trucables
        else:
            filtered = [t for t in self.trucables if query in t.lower()]
        if not filtered:
            filtered = ['(no results)']
        try:
            self.objetos_combobox.configure(values=filtered)
            if filtered and filtered[0] != '(no results)':
                self.objetos_combobox.set(filtered[0])
        except Exception:
            pass
    
    def seleccionar_objeto(self):
        obj = self.objetos_combobox.get()
        if not obj or obj == '(no results)':
            self.status_label.configure(text='Select an object.', text_color=Style.TEXT_ERROR)
            return
        self.selected_objeto = obj
        self.status_label.configure(text=f'Object selected: {obj}', text_color=Style.TEXT_SUCCESS)
        
        # Ask for behavior
        try:
            behavior = ask_text(self.root, 'Behavior', 'Enter behavior to assign (e.g., gaturroCambiante)')
        except Exception:
            behavior = None

        # Workaround: if modal failed due to parent grab issues, try without parent
        if behavior is None:
            try:
                behavior = ask_text(None, 'Behavior', 'Enter behavior to assign (e.g., gaturroCambiante)')
            except Exception:
                behavior = None

        if behavior is None:
            self.status_label.configure(text='Operation cancelled.', text_color=Style.TEXT_SECONDARY)
            return
        
        # Ask for quantity
        try:
            qty = ask_integer(self.root, 'Quantity', 'Enter object quantity:', initialvalue=1, minvalue=1)
        except Exception:
            qty = 1
        if qty is None:
            self.status_label.configure(text='Operation cancelled.', text_color=Style.TEXT_SECONDARY)
            return
        
        # Continue with modification logic
        self.status_label.configure(text='Generating and modifying SWF...', text_color=Style.TEXT_SECONDARY)
        self.procesar_modificacion(self.selected_swf, self.selected_objeto, behavior, qty)
    
    def mostrar_tiendas(self):
        path = os.path.join('info', 'tiendas.txt')
        if not os.path.exists(path):
            self.status_label.configure(text='File info/tiendas.txt not found.', text_color=Style.TEXT_ERROR)
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.status_label.configure(text=f'Error reading stores: {e}', text_color=Style.TEXT_ERROR)
            return
        
        self.mostrar_dialogo_info('Store Behaviors List', content, Style.BTN_ACCENT_BLUE)
    
    def mostrar_portales(self):
        path = os.path.join('info', 'portales.txt')
        if not os.path.exists(path):
            self.status_label.configure(text='File info/portales.txt not found.', text_color=Style.TEXT_ERROR)
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.status_label.configure(text=f'Error reading portals: {e}', text_color=Style.TEXT_ERROR)
            return
        
        self.mostrar_dialogo_info('Portal Behaviors List', content, Style.BTN_ACCENT_PURPLE)
    
    def mostrar_dialogo_info(self, titulo, contenido, color_accent):
        # Use standardized modal to ensure icon and styling consistency
        top = create_modal(self.root, titulo, 600, 500)
        
        frame = ctk.CTkFrame(
            top,
            corner_radius=Style.RADIUS_M,
            fg_color=Style.BG_SECONDARY,
            border_width=1,
            border_color=Style.BORDER_LIGHT
        )
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text=titulo,
            font=(Style.FONT_FAMILY, Style.FONT_SIZE_S, "bold"),
            text_color=color_accent
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        txt = ctk.CTkTextbox(
            frame,
            width=560,
            height=380,
            corner_radius=Style.RADIUS_S,
            fg_color=Style.BG_TERTIARY,
            border_color=Style.BORDER_MEDIUM,
            text_color=Style.TEXT_PRIMARY,
            font=("Consolas", Style.FONT_SIZE_XS)
        )
        txt.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        txt.insert('1.0', contenido)
        txt.configure(state='disabled')
        
        btn = create_button(
            frame,
            text='Close',
            command=top.destroy,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        btn.pack(pady=(0, 10))
    
    def generar_codigo_actionscript(self, symbol, nombre_clase, behavior):
        codigo = f"""package
{{
   [Embed(source=\"/_assets/assets.swf\", symbol=\"{symbol}\")]
   public dynamic class {nombre_clase} extends NpcMamboAsset
   {{
      public function {nombre_clase}()
      {{
         super();
         addFrameScript(0,frame1);
      }}
      internal function frame1() : *
      {{
         behavior = \"{behavior}\";
      }}
   }}
}}
"""
        return codigo
    
    def procesar_modificacion(self, swf_name, clase, behavior, qty):
        temp_dir = Path('temp_trucar').resolve()
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        
        ffdec_bat = os.path.abspath('ffdec/ffdec.bat')
        swf_path_abs = os.path.abspath(os.path.join('swf_cache', f'{swf_name}.swf'))
        
        extract_cmd = f'"{ffdec_bat}" -export script "{temp_dir}" "{swf_path_abs}"'
        result = subprocess.run(extract_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            self.status_label.configure(text=f'Error extracting scripts: {result.stderr}', text_color=Style.TEXT_ERROR)
            return
        
        scripts_dir = temp_dir / 'scripts'
        as_file = scripts_dir / f'{clase}.as'
        if not as_file.exists():
            self.status_label.configure(text=f'File {clase}.as not found.', text_color=Style.TEXT_ERROR)
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            return
        
        with open(as_file, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
        
        match = re.search(r'\[Embed\(source="[^"]+", symbol="([^"]+)"\)\]', contenido_original)
        if not match:
            self.status_label.configure(text='Could not extract symbol from original file.', text_color=Style.TEXT_ERROR)
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            return
        symbol_original = match.group(1)
        
        codigo_as = self.generar_codigo_actionscript(symbol_original, clase, behavior)
        with open(as_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(codigo_as)
        
        # Prepare import
        trucados_dir = os.path.join('swf_cache', 'trucados')
        encode_dir = os.path.join('output_sacar_objetos', 'trucados')
        os.makedirs(trucados_dir, exist_ok=True)
        os.makedirs(encode_dir, exist_ok=True)
        
        out_swf = os.path.join(trucados_dir, f'{swf_name}_trucado.swf')
        out_swf_abs = os.path.abspath(out_swf)
        
        final_import_dir = temp_dir / 'final_import'
        final_import_dir.mkdir(exist_ok=True)
        final_as_file = final_import_dir / f'{clase}.as'
        shutil.copy(as_file, final_as_file)
        
        final_import_dir_abs = os.path.abspath(final_import_dir)
        import_cmd = f'"{ffdec_bat}" -importScript "{swf_path_abs}" "{out_swf_abs}" "{final_import_dir_abs}"'
        result2 = subprocess.run(import_cmd, shell=True, capture_output=True, text=True)
        if result2.returncode != 0:
            self.status_label.configure(text=f'Error importing modified object: {result2.stderr}', text_color=Style.TEXT_ERROR)
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            return
        
        try:
            safe_swf = swf_name.replace('/', '_').replace('\\', '_')
            encode_path = os.path.join(encode_dir, f'{clase}_{safe_swf}_trucado_encode.txt')
            encode_content = self.swf_processor.generate_encode([clase], swf_name, qty=qty)
            import base64
            encode_b64 = base64.b64encode(encode_content.encode('utf-8')).decode('utf-8')
            with open(encode_path, 'w', encoding='utf-8') as f:
                f.write(encode_b64)
            
            self.mostrar_mensaje_exito(f'✅ Process completed\n\nModified SWF:\n{out_swf}\n\nSpecial encode:\n{encode_path}')
            self.status_label.configure(text='✅ Modified SWF generated successfully', text_color=Style.TEXT_SUCCESS)
        except Exception as e:
            self.status_label.configure(text=f'SWF generated but error saving encode: {e}', text_color=Style.TEXT_ERROR)
        
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
    
    def mostrar_mensaje_exito(self, mensaje):
        top = create_modal(self.root, '✅ Process Completed', 600, 250)
        
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
            justify='left'
        )
        label.pack(padx=20, pady=30)
        
        btn = create_button(
            frame,
            text='Close',
            command=top.destroy,
            color=Style.BTN_SECONDARY,
            height=36,
            font_size=11
        )
        btn.pack(pady=10)