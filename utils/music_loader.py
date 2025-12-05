"""
Utilitário para carregar e gerenciar arquivos de música
"""
import os
from pathlib import Path
from typing import List, Dict

class MusicLoader:
    """Classe para carregar e gerenciar arquivos de música"""
    
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}
    
    def __init__(self):
        self.music_files: List[Dict] = []
        self.current_folder = None
    
    def load_folder(self, folder_path: str) -> List[Dict]:
        """
        Carrega todas as músicas de uma pasta
        
        Args:
            folder_path: Caminho da pasta com as músicas
            
        Returns:
            Lista de dicionários com informações das músicas
        """
        self.music_files = []
        self.current_folder = folder_path
        
        if not os.path.exists(folder_path):
            return self.music_files
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                        music_info = {
                            'path': str(file_path),
                            'name': file_path.stem,
                            'extension': file_path.suffix,
                            'folder': root
                        }
                        self.music_files.append(music_info)
        except Exception as e:
            print(f"Erro ao carregar músicas: {e}")
        
        # Ordena por nome
        self.music_files.sort(key=lambda x: x['name'].lower())
        return self.music_files
    
    def get_music_list(self) -> List[Dict]:
        """Retorna a lista de músicas carregadas"""
        return self.music_files
    
    def get_music_by_index(self, index: int) -> Dict:
        """Retorna uma música específica pelo índice"""
        if 0 <= index < len(self.music_files):
            return self.music_files[index]
        return None
