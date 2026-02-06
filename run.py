import customtkinter as ctk
import os
from tkinter import PhotoImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ModernLauncher:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MG Tools")
        self.root.geometry("400x620")
        self.root.resizable(False, False)
        
        # Fondo completamente negro tipo Vercel
        self.root.configure(fg_color="#000000")
        
        # Cargar icono desde la carpeta images
        self.set_window_icon()
        
        # Centrar ventana en pantalla
        self.center_window()
        
        self.build_ui()
        self.root.mainloop()
    
    def set_window_icon(self):
        """Carga el icono desde la carpeta images"""
        # Rutas a probar (en orden de preferencia)
        icon_paths = [
            "images/ico.ico",     # Primero intentar con ICO (mejor para Windows)
            "images/ico.jpg",     # Luego JPG
            "ico.ico",            # Por si está en la raíz
            "ico.jpg",            # Por si está en la raíz
        ]
        
        icon_loaded = False
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    # Método 1: Para archivos ICO (Windows)
                    if icon_path.endswith('.ico'):
                        self.root.iconbitmap(icon_path)
                        print(f"Icono ICO cargado: {icon_path}")
                        icon_loaded = True
                        break
                    # Método 2: Para archivos JPG/PNG (multi-plataforma)
                    else:
                        icon = PhotoImage(file=icon_path)
                        self.root.iconphoto(True, icon)
                        print(f"Icono JPG/PNG cargado: {icon_path}")
                        icon_loaded = True
                        break
                except Exception as e:
                    print(f"Error cargando {icon_path}: {e}")
                    continue
        
        if not icon_loaded:
            print("⚠️ Advertencia: No se pudo cargar ningún icono.")
            print("Asegúrate de que existe 'images/ico.ico' o 'images/ico.jpg'")
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def build_ui(self):
        # Frame principal ultra minimalista
        main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=0,
            fg_color="#000000",
            border_width=0
        )
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Encabezado minimalista
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            height=100
        )
        header_frame.pack(fill="x", pady=(10, 20))
        header_frame.pack_propagate(False)
        
        # Título con tipografía más fina (usando weight normal)
        title = ctk.CTkLabel(
            header_frame,
            text="MG Tools",
            font=("SF Pro Display", 28, "normal"),
            text_color="#ffffff"
        )
        title.pack(pady=(20, 0))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Select a tool",
            font=("SF Pro Display", 12),
            text_color="#666666"
        )
        subtitle.pack(pady=(5, 0))
        
        # Frame para botones con más espacio
        buttons_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="both", expand=True, pady=10)
        
        # Botones principales en escala de grises
        buttons_data = [
            ("Aplicar en Mundo Gaturro", self.launch_aplicar, "#1a1a1a"),
            ("Sacar Objetos", self.launch_sacar_objetos, "#222222"),
            ("Trucar Ropa", self.launch_trucar, "#2a2a2a"),
            ("Trucar Tiendas/Portales", self.launch_trucar_tiendas, "#333333"),
        ]
        
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                font=("SF Pro Display", 13),
                corner_radius=8,
                height=48,
                border_width=0,
                fg_color=color,
                hover_color=self.adjust_brightness(color, 40),
                text_color="#e0e0e0"
            )
            btn.pack(fill="x", pady=4)
        
        # Separador sutil
        separator = ctk.CTkFrame(
            buttons_frame,
            height=1,
            fg_color="#222222"
        )
        separator.pack(fill="x", pady=(20, 15))
        
        # Botón de configuración con borde sutil
        config_btn = ctk.CTkButton(
            buttons_frame,
            text="Settings",
            font=("SF Pro Display", 12),
            command=self.launch_config,
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1a1a1a",
            text_color="#888888",
            border_width=1,
            border_color="#333333"
        )
        config_btn.pack(fill="x", pady=(0, 20))
        
        # Footer ultra minimalista
        footer_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            height=30
        )
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        # Versión centrada
        version = ctk.CTkLabel(
            footer_frame,
            text="v2.0",
            font=("SF Pro Display", 10),
            text_color="#444444"
        )
        version.pack(side="left")
        
        # Autor alineado a la derecha
        author = ctk.CTkLabel(
            footer_frame,
            text="naw",
            font=("SF Pro Display", 10),
            text_color="#444444"
        )
        author.pack(side="right")
        
        # URL centrada
        url = ctk.CTkLabel(
            footer_frame,
            text="mgtools.vercel.app",
            font=("SF Pro Display", 10),
            text_color="#555555"
        )
        url.pack(expand=True)
    
    def adjust_brightness(self, hex_color, adjustment):
        """Ajusta el brillo de un color hex"""
        hex_color = hex_color.lstrip('#')
        r = max(0, min(255, int(hex_color[0:2], 16) + adjustment))
        g = max(0, min(255, int(hex_color[2:4], 16) + adjustment))
        b = max(0, min(255, int(hex_color[4:6], 16) + adjustment))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def launch_aplicar(self):
        self.root.destroy()
        from scripts.fiddler_rule_creator import FiddlerRuleCreator
        app = FiddlerRuleCreator()
        app.create_aplicar_reglas_panel()
    
    def launch_sacar_objetos(self):
        self.root.destroy()
        from scripts.fiddler_rule_creator import FiddlerRuleCreator
        app = FiddlerRuleCreator()
        app.create_sacar_objetos_panel()
    
    def launch_trucar(self):
        self.root.destroy()
        from scripts.trucar_launcher import TrucarLauncher
        app = TrucarLauncher()
        app.start()
    
    def launch_trucar_tiendas(self):
        self.root.destroy()
        from scripts.trucar_tiendas import TrucarTiendasLauncher
        app = TrucarTiendasLauncher()
        app.start()
    
    def launch_config(self):
        from scripts.config_window import ConfigWindow
        ConfigWindow(self.root)

if __name__ == "__main__":
    ModernLauncher()