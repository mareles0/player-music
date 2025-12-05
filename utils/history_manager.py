"""
Gerenciador de histórico de reprodução
Mantém registro das últimas músicas tocadas
"""
import json
from pathlib import Path
from datetime import datetime

class HistoryManager:
    """Gerencia o histórico de reprodução"""
    
    def __init__(self, max_entries=50):
        self.config_dir = Path.home() / '.music_player'
        self.history_file = self.config_dir / 'history.json'
        self.config_dir.mkdir(exist_ok=True)
        self.max_entries = max_entries
        self.history = self.load_history()
    
    def load_history(self):
        """Carrega histórico do arquivo"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            return []
    
    def save_history(self):
        """Salva histórico no arquivo"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
            return False
    
    def add_entry(self, music_path, music_name):
        """Adiciona entrada ao histórico"""
        entry = {
            'path': music_path,
            'name': music_name,
            'timestamp': datetime.now().isoformat()
        }
        
        # Remove entradas antigas do mesmo arquivo
        self.history = [h for h in self.history if h['path'] != music_path]
        
        # Adiciona no início
        self.history.insert(0, entry)
        
        # Limita tamanho do histórico
        self.history = self.history[:self.max_entries]
        
        self.save_history()
    
    def get_history(self, limit=None):
        """Retorna histórico (limitado opcionalmente)"""
        if limit:
            return self.history[:limit]
        return self.history
    
    def clear_history(self):
        """Limpa todo o histórico"""
        self.history = []
        self.save_history()
