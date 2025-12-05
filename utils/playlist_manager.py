"""
Gerenciador de Playlists - Salva e carrega pastas de músicas
"""
import json
import os
from pathlib import Path
from typing import List, Dict

class PlaylistManager:
    """Classe para gerenciar playlists (pastas salvas)"""
    
    def __init__(self):
        self.config_file = Path.home() / ".music_player" / "playlists.json"
        self.playlists: List[Dict] = []
        self.ensure_config_dir()
        self.load_playlists()
    
    def ensure_config_dir(self):
        """Garante que o diretório de configuração existe"""
        config_dir = self.config_file.parent
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_playlists(self) -> List[Dict]:
        """Carrega playlists salvas do arquivo JSON"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.playlists = data.get('playlists', [])
                    # Remove playlists de pastas que não existem mais
                    self.playlists = [p for p in self.playlists if os.path.exists(p['path'])]
            except Exception as e:
                print(f"Erro ao carregar playlists: {e}")
                self.playlists = []
        return self.playlists
    
    def save_playlists(self):
        """Salva playlists no arquivo JSON"""
        try:
            data = {'playlists': self.playlists}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar playlists: {e}")
    
    def add_playlist(self, path: str, name: str = None) -> bool:
        """
        Adiciona uma nova playlist (pasta)
        
        Args:
            path: Caminho da pasta
            name: Nome personalizado (opcional, usa nome da pasta se não fornecido)
            
        Returns:
            True se adicionada com sucesso
        """
        if not os.path.exists(path):
            return False
        
        # Verifica se já existe
        for playlist in self.playlists:
            if playlist['path'] == path:
                return False
        
        # Nome padrão é o nome da pasta
        if not name:
            name = Path(path).name
        
        playlist = {
            'name': name,
            'path': path,
            'added_date': str(Path(path).stat().st_mtime)
        }
        
        self.playlists.append(playlist)
        self.save_playlists()
        return True
    
    def remove_playlist(self, path: str) -> bool:
        """Remove uma playlist pelo caminho"""
        original_length = len(self.playlists)
        self.playlists = [p for p in self.playlists if p['path'] != path]
        
        if len(self.playlists) < original_length:
            self.save_playlists()
            return True
        return False
    
    def get_playlists(self) -> List[Dict]:
        """Retorna lista de playlists"""
        return self.playlists
    
    def get_playlist_by_path(self, path: str) -> Dict:
        """Retorna playlist específica pelo caminho"""
        for playlist in self.playlists:
            if playlist['path'] == path:
                return playlist
        return None
    
    def rename_playlist(self, path: str, new_name: str) -> bool:
        """Renomeia uma playlist"""
        for playlist in self.playlists:
            if playlist['path'] == path:
                playlist['name'] = new_name
                self.save_playlists()
                return True
        return False
