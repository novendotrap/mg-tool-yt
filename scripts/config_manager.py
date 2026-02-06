import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.get_defaults()
        else:
            return self.get_defaults()

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_defaults(self):
        return {
            "fiddler_path": str(Path.home() / "Documents" / "Fiddler2"),
            "mundo_gaturro_cache_path": str(Path(os.getenv('APPDATA')) / "MundoGaturro")
        }

    def get_fiddler_path(self):
        return self.config.get("fiddler_path", self.get_defaults()["fiddler_path"])

    def set_fiddler_path(self, path):
        self.config["fiddler_path"] = path
        self.save_config()

    def get_mundo_gaturro_cache_path(self):
        return self.config.get("mundo_gaturro_cache_path", self.get_defaults()["mundo_gaturro_cache_path"])

    def set_mundo_gaturro_cache_path(self, path):
        self.config["mundo_gaturro_cache_path"] = path
        self.save_config()
