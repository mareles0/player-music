"""
Reprodutor de Música - Estilo Spotify
Aplicação para reproduzir músicas de uma pasta local
"""
import sys
from components.player import MusicPlayer

def main():
    """Função principal que inicializa o player"""
    app = MusicPlayer()
    app.run()

if __name__ == "__main__":
    main()
