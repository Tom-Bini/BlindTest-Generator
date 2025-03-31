import os
import json

class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.cache_file = "music_cache.json"
        self.music_dir = r"C:\Users\Tom\Music"
        
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.music_dir = config.get('music_dir', r"C:\Users\Tom\Music")
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {str(e)}")

    def save_config(self):
        try:
            config = {
                'music_dir': self.music_dir
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
            
    def load_cache(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
            
    def save_cache(self, cache_data):
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du cache: {str(e)}") 