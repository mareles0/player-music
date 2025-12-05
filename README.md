# 🎵 Music Player - Estilo Spotify

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-00ADD8?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Um reprodutor de música moderno e intuitivo com interface inspirada no Spotify.

[📥 Download](#-download) • [Recursos](#-recursos) • [Instalação](#-instalação) • [Uso](#-uso) • [Atalhos](#%EF%B8%8F-atalhos-de-teclado) • [Build](#-gerando-executável)

</div>

---

## 📥 Download

### Executável Windows (.exe)

Baixe a versão mais recente compilada e pronta para usar:

**[⬇️ Download MusicPlayer.exe](https://github.com/mareles0/player-music/releases/latest)**

> 💡 **Não precisa instalar Python ou dependências!** Apenas baixe e execute.

---

## 📸 Preview

Interface elegante com tema dark, controles intuitivos e modo mini player.

## ✨ Recursos

### 🎧 Reprodução de Áudio
- **Suporte a múltiplos formatos**: MP3, WAV, OGG, FLAC
- **Controles completos**: Play, Pause, Próxima, Anterior, Stop
- **Barra de progresso interativa**: Clique para navegar na música
- **Exibição de tempo**: Tempo atual e duração total (MM:SS)
- **Controle de volume**: Slider com indicador visual

### 🎲 Modo Aleatório Inteligente
- Reprodução aleatória sem repetições
- Histórico de músicas já tocadas
- Reinicia automaticamente após tocar todas as músicas
- Indicador visual ativo (botão verde)

### 📋 Sistema de Playlists
- Crie e gerencie múltiplas playlists
- Salve suas playlists favoritas
- Carregue playlists rapidamente
- Persistência automática em JSON

### 🎹 Suporte a Teclas de Mídia
- **Teclas do teclado/fone de ouvido**:
  - Play/Pause, Próxima, Anterior
  - Volume Up/Down, Mute
- **Atalhos de teclado**: Espaço, setas, M para mute
- Funciona mesmo com a janela em segundo plano

### 🪟 Modo Mini Player
- Interface compacta (450x280)
- Sempre visível enquanto trabalha
- Alterna facilmente entre os modos
- Mantém todas as funcionalidades

### 🎨 Interface Moderna
- Design inspirado no Spotify
- Tema dark elegante (#121212)
- Cor de destaque verde (#1DB954)
- Responsiva e intuitiva

## 🚀 Instalação

### Pré-requisitos
- Python 3.11 ou superior
- Windows (para suporte completo a teclas de mídia)


## 🎮 Uso

### Primeira Execução

1. Clique em **"Carregar Pasta"** para selecionar uma pasta com músicas
2. As músicas serão listadas automaticamente
3. Clique duplo em uma música para reproduzir
4. Use os controles na parte inferior para navegar

### Criando Playlists

1. Carregue uma pasta com músicas
2. Clique em **"Salvar Playlist"**
3. Digite um nome para a playlist
4. Use **"Carregar Playlist"** para acessar depois

### Modo Aleatório

1. Clique no botão **🔀 Aleatório**
2. As músicas serão reproduzidas em ordem aleatória
3. Não haverá repetições até que todas sejam tocadas
4. O histórico é salvo automaticamente

### Modo Mini

1. Clique em **"Mini Mode"**
2. A janela ficará compacta
3. Clique novamente para voltar ao modo normal

## ⌨️ Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `Espaço` | Play/Pause |
| `→` | Próxima música |
| `←` | Música anterior |
| `↑` | Aumentar volume |
| `↓` | Diminuir volume |
| `M` | Mute/Unmute |

### Teclas de Mídia (Teclado/Fone)

- ⏯️ Play/Pause
- ⏭️ Próxima
- ⏮️ Anterior
- 🔊 Volume Up/Down
- 🔇 Mute

## 🏗️ Estrutura do Projeto

```
music-player/
├── assets/                    # Recursos (ícones)
│   └── spotify.ico
├── components/                # Componentes da interface
│   ├── __init__.py
│   └── player.py             # Classe principal do player
├── utils/                     # Utilitários
│   ├── __init__.py
│   ├── media_keys.py         # Listener de teclas de mídia
│   ├── music_loader.py       # Carregador de músicas
│   └── playlist_manager.py   # Gerenciador de playlists
├── build_exe.py              # Script de build
├── main.py                   # Ponto de entrada
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal
- **tkinter**: Interface gráfica
- **Pygame**: Engine de reprodução de áudio
- **Mutagen**: Leitura de metadados (duração, artista, etc.)
- **PyWin32**: Integração com Windows para teclas de mídia
- **PyInstaller**: Geração de executável
- **Pillow**: Processamento de imagens/ícones

## 📚 Documentação Adicional

- [📱 MOBILE.md](MOBILE.md) - Por que não há versão APK/iOS e alternativas
- [📋 CHANGELOG.md](CHANGELOG.md) - Histórico de versões e mudanças
- [🤝 CONTRIBUTING.md](CONTRIBUTING.md) - Guia para contribuidores
- [🔒 SECURITY.md](SECURITY.md) - Política de segurança
- [🧪 tests/README.md](tests/README.md) - Como executar testes

## 🎯 Roadmap

### v1.1.0 (Próxima Versão)
- [ ] Sistema de favoritos ⭐
- [ ] Histórico de reprodução 📜
- [ ] Busca avançada 🔍
- [ ] Tema claro/escuro 🎨
- [ ] Equalizer de áudio 🎛️

### Futuro
- [ ] Importação de playlists M3U
- [ ] Suporte a mais formatos (AIFF, APE)
- [ ] Lyrics integrados
- [ ] Estatísticas de reprodução
- [ ] Mini visualizador de ondas

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre:
- Como reportar bugs
- Como sugerir funcionalidades
- Padrões de código
- Processo de Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🐛 Problemas Conhecidos

- O suporte a teclas de mídia é específico para Windows
- Alguns formatos de áudio podem não ser suportados dependendo dos codecs instalados
- Performance pode variar com playlists muito grandes (>10.000 músicas)

## 📞 Suporte

- 🐛 **Bugs**: Abra uma [Issue](https://github.com/mareles0/player-music/issues)
- 💡 **Ideias**: Use [Discussions](https://github.com/mareles0/player-music/discussions)
- 🔒 **Segurança**: Veja [SECURITY.md](SECURITY.md)

## ⭐ Agradecimentos

- Comunidade Pygame pelo excelente framework
- Todos os contribuidores que ajudaram a melhorar o projeto
- Usuários que reportam bugs e sugerem melhorias

---

<div align="center">

**Feito com ❤️ usando Python**

[⬆ Voltar ao topo](#-music-player---estilo-spotify)

</div>

## 📧 Contato

Dúvidas ou sugestões? Abra uma [issue](https://github.com/mareles0/music-player/issues)!

---

<div align="center">

Feito com ❤️ e Python

</div>
