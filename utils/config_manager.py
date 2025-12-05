"""
Gerenciador de configurações do usuário
Salva preferências entre sessões
"""
import json
from pathlib import Path

class ConfigManager:
    """Gerencia configurações persistentes do aplicativo"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.music_player'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        
        # Configurações padrão
        self.default_config = {
            'volume': 70,
            'theme': 'dark',
            'last_folder': None,
            'window_width': 900,
            'window_height': 600,
            'last_playlist': None,
            'shuffle_enabled': False,
            'favorites': []
        }
        
        self.config = self.load_config()
    
    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Mescla com defaults para adicionar novas configurações
                    return {**self.default_config, **loaded}
            return self.default_config.copy()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return self.default_config.copy()
    
    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def get(self, key, default=None):
        """Obtém uma configuração"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Define uma configuração e salva"""
        self.config[key] = value
        self.save_config()
    
    def add_favorite(self, music_path):
        """Adiciona música aos favoritos"""
        favorites = self.config.get('favorites', [])
        if music_path not in favorites:
            favorites.append(music_path)
            self.set('favorites', favorites)
            return True
        return False
    
    def remove_favorite(self, music_path):
        """Remove música dos favoritos"""
        favorites = self.config.get('favorites', [])
        if music_path in favorites:
            favorites.remove(music_path)
            self.set('favorites', favorites)
            return True
        return False
    
    def is_favorite(self, music_path):
        """Verifica se música é favorita"""
        return music_path in self.config.get('favorites', [])
