import os
import platform
import shutil
import base64
from pathlib import Path
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import subprocess
import sys

class SWFProcessor:
    def __init__(self):
        self.cdn_base_url = "https://cdn-ar.mundogaturro.com/juego/assets/"
    def download_swf(self, swf_name):
        if not swf_name.lower().endswith('.swf'):
            swf_name += '.swf'
        swf_dir = Path("swf_cache")
        swf_dir.mkdir(exist_ok=True)
        swf_path = Path(swf_name)
        if len(swf_path.parts) > 1:
            full_local_dir = swf_dir / swf_path.parent
            full_local_dir.mkdir(parents=True, exist_ok=True)
            local_file = swf_dir / swf_path
        else:
            local_file = swf_dir / swf_name
        url = f"{self.cdn_base_url}{swf_name}"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
            }
            response = requests.get(url, headers=headers, timeout=180, stream=True, verify=False)
            if response.status_code == 200:
                with open(local_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                size = os.path.getsize(local_file)
                if size > 0:
                    return str(local_file), None
                else:
                    os.remove(local_file)
                    return None, f"Error: El archivo descargado está vacío (0 bytes)."
            elif response.status_code == 404:
                return None, f"Error 404: El SWF '{swf_name}' no fue encontrado en el servidor. Revisa el nombre."
            elif response.status_code == 403:
                return None, f"Error 403: Acceso denegado para el SWF '{swf_name}'."
            else:
                return None, f"Error HTTP {response.status_code} al descargar '{swf_name}'."
        except requests.exceptions.ConnectionError:
            return None, "Error de red: No se pudo conectar al CDN de Mundo Gaturro."
        except requests.exceptions.Timeout:
            return None, "Error de red: Tiempo de espera agotado (Timeout)."
        except Exception as e:
            return None, f"Error inesperado al descargar: {str(e)}"
    def extract_classes(self, swf_file):
        if not shutil.which("java"):
            return [], "Error: Java no está instalado o no está en el PATH. FFDec requiere Java."
            
        if platform.system() == "Windows":
            ffdec_path = "ffdec/ffdec.bat"
            if not os.path.exists(ffdec_path):
                return [], "Error: ffdec.bat no encontrado"
            cmd = f'"{ffdec_path}" -format script:as -export script "temp_extract" "{swf_file}"'
        else:
            ffdec_jar = "ffdec/ffdec.jar"
            if not os.path.exists(ffdec_jar):
                return [], "Error: ffdec.jar no encontrado"
            cmd = f'java -jar "{ffdec_jar}" -format script:as -export script "temp_extract" "{swf_file}"'
        if os.path.exists("temp_extract"):
            shutil.rmtree("temp_extract")
        os.makedirs("temp_extract", exist_ok=True)
        try:
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                err_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
                return [], f"Error FFDec: {err_msg}"
        except subprocess.TimeoutExpired:
            return [], "Error: Timeout al extraer clases"
        except Exception as e:
            return [], f"Error: {str(e)}"
        scripts_dir = Path("temp_extract") / "scripts"
        if not scripts_dir.exists():
            return [], "Error: No se generaron scripts"
        classes = []
        for as_file in scripts_dir.glob("*.as"):
            class_name = as_file.stem
            classes.append({'name': class_name})
        try:
            shutil.rmtree("temp_extract")
        except:
            pass
        return classes, "Éxito"
    def filter_classes(self, classes, filter_type):
        class_names = [cls['name'] for cls in classes]
        if filter_type == "trucables":
            filtered = []
            for cls in classes:
                name = cls['name']
                if not name.endswith('_on'):
                    on_version = name + '_on'
                    if on_version in class_names:
                        filtered.append(name)
            return filtered
        elif filter_type == "restantes":
            return [cls['name'] for cls in classes 
                   if (not cls['name'].endswith('_on') and 
                       'Asset' not in cls['name'] and 
                       not cls['name'].endswith('_so'))]
        else:
            return []
    def combine_filters(self, classes):
        trucables = set(self.filter_classes(classes, "trucables"))
        restantes = set(self.filter_classes(classes, "restantes"))
        combined = trucables.union(restantes)
        return list(combined)
    def generate_encode(self, classes, swf_name, qty=1):
        """Genera el encode. `qty` es la cantidad por objeto (entero >=1).
        Si `classes` está vacío devuelve None."""
        try:
            qty_int = int(qty)
            if qty_int < 1:
                qty_int = 1
        except Exception:
            qty_int = 1

        if not classes:
            return None
        resultado = 'INICIO: DO\n    on activate A1\n\n'
        for i in range(len(classes)):
            seccion_actual = f'A{i + 1}'
            seccion_siguiente = f'A{i + 2}' if i < len(classes) - 1 else 'INICIO'
            resultado += f'{seccion_actual}: DO\n'
            resultado += f'    user.state get\n'
            resultado += f'    inventory.add {qty_int} {swf_name}.{classes[i]}\n'
            resultado += f'    after 1 {seccion_siguiente}\n\n'

        return resultado
    def get_exact_command(self, swf_name):
        # normalize name: accept with or without .swf
        name = swf_name
        if name.lower().endswith('.swf'):
            name = name[:-4]
        return f"EXACT:{self.cdn_base_url}{name}.swf"

    def get_exact_command_with_size(self, swf_name, timeout=20):
        """Return EXACT URL with appended size parameter obtained
        by running the `extract_swf_size.py` helper script.
        Falls back to the plain EXACT URL if the helper fails.
        Format: EXACT:https://.../name.swf?size=12345
        """
        # normalize base name
        name = swf_name
        if name.lower().endswith('.swf'):
            name = name[:-4]
        base_url = f"{self.cdn_base_url}{name}.swf"

        # locate helper script
        script_path = os.path.join('scripts', 'extract_swf_size.py')
        if not os.path.exists(script_path):
            return f"EXACT:{base_url}"

        try:
            cmd = [sys.executable, script_path, name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                out = result.stdout.strip()
                if out:
                    # last non-empty line
                    last = out.splitlines()[-1].strip()
                    if last.isdigit():
                        # Append the size as a lone query parameter per spec: ?{number}
                        return f"EXACT:{base_url}?{last}"
        except Exception:
            pass

        return f"EXACT:{base_url}"
    def generate_swf_url_visual(self, user_input):
        base_url = "https://cdn-ar.mundogaturro.com/juego/assets/"
        return f"{base_url}{user_input}.swf"
