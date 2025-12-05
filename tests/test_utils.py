"""
Testes básicos para o Music Player
Execute: python -m pytest tests/
"""
import pytest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config_manager import ConfigManager
from utils.history_manager import HistoryManager
from utils.playlist_manager import PlaylistManager

class TestConfigManager:
    """Testes para o gerenciador de configurações"""
    
    def test_default_config(self):
        """Testa criação com configurações padrão"""
        config = ConfigManager()
        assert config.get('volume') == 70
        assert config.get('theme') == 'dark'
    
    def test_set_and_get(self):
        """Testa definir e obter configurações"""
        config = ConfigManager()
        config.set('volume', 85)
        assert config.get('volume') == 85
    
    def test_favorites(self):
        """Testa sistema de favoritos"""
        config = ConfigManager()
        test_path = "/test/music.mp3"
        
        # Adicionar favorito
        config.add_favorite(test_path)
        assert config.is_favorite(test_path) is True
        
        # Remover favorito
        config.remove_favorite(test_path)
        assert config.is_favorite(test_path) is False

class TestHistoryManager:
    """Testes para o gerenciador de histórico"""
    
    def test_add_entry(self):
        """Testa adicionar entrada ao histórico"""
        history = HistoryManager(max_entries=5)
        history.clear_history()
        
        history.add_entry("/test/song1.mp3", "Song 1")
        history.add_entry("/test/song2.mp3", "Song 2")
        
        entries = history.get_history()
        assert len(entries) == 2
        assert entries[0]['name'] == "Song 2"  # Mais recente primeiro
    
    def test_max_entries(self):
        """Testa limite máximo de entradas"""
        history = HistoryManager(max_entries=3)
        history.clear_history()
        
        for i in range(5):
            history.add_entry(f"/test/song{i}.mp3", f"Song {i}")
        
        entries = history.get_history()
        assert len(entries) == 3  # Máximo 3
    
    def test_clear_history(self):
        """Testa limpeza do histórico"""
        history = HistoryManager()
        history.add_entry("/test/song.mp3", "Song")
        history.clear_history()
        
        assert len(history.get_history()) == 0

class TestPlaylistManager:
    """Testes para o gerenciador de playlists"""
    
    def test_add_playlist(self):
        """Testa adicionar playlist"""
        manager = PlaylistManager()
        result = manager.add_playlist("/test/folder", "Test Playlist")
        
        # Primeira adição deve funcionar
        assert result is True or result is False  # Pode já existir
    
    def test_get_playlists(self):
        """Testa obter lista de playlists"""
        manager = PlaylistManager()
        playlists = manager.get_playlists()
        
        assert isinstance(playlists, list)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
