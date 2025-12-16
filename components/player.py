"""
Player de Música com Interface Gráfica - Versão Melhorada
Melhorias: Animações suaves, barra de progresso clicável, tooltips, melhor UX
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pygame
import os
import random
from pathlib import Path
from utils.music_loader import MusicLoader
from utils.playlist_manager import PlaylistManager
from utils.media_keys import MediaKeyListener
from utils.config_manager import ConfigManager
from utils.history_manager import HistoryManager

class ToolTip:
    """Tooltip personalizado para mostrar dicas ao passar o mouse"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)
    
    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        background="#1DB954", foreground="white",
                        relief=tk.SOLID, borderwidth=1,
                        font=("Arial", 9), padx=8, pady=4)
        label.pack()
    
    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class MusicPlayer:
    """Classe principal do reprodutor de música - Versão Melhorada"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Player - Estilo Spotify")
        self.root.geometry("900x600")
        self.root.minsize(750, 500)
        self.root.configure(bg="#121212")
        
        # Define ícone do aplicativo
        self.set_app_icon()
        
        # Inicializa pygame mixer
        pygame.mixer.init()
        
        # Gerenciadores
        self.config_manager = ConfigManager()
        self.history_manager = HistoryManager()
        self.music_loader = MusicLoader()
        self.playlist_manager = PlaylistManager()
        
        # Variáveis do player
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.volume = self.config_manager.get('volume', 70) / 100
        self.current_folder = self.config_manager.get('last_folder')
        self.current_playlist = self.config_manager.get('last_playlist')
        self.is_mini_mode = False
        self.shuffle_mode = self.config_manager.get('shuffle_enabled', False)
        self.repeat_mode = self.config_manager.get('repeat_mode', 'off')  # off, one, all
        self.shuffle_history = []
        self.shuffle_queue = []
        self.song_length = 0
        self.song_position = 0
        self.current_theme = self.config_manager.get('theme', 'dark')
        self.search_query = ''
        self.is_muted = False
        self.volume_before_mute = self.volume
        self.is_seeking = False  # Para controle da barra de progresso
        
        # Inicializa listener de teclas de mídia
        self.media_listener = MediaKeyListener(
            on_play_pause=self.play_pause,
            on_next=self.next_song,
            on_previous=self.previous_song,
            on_volume_up=self.increase_volume,
            on_volume_down=self.decrease_volume,
            on_mute=self.toggle_mute
        )
        self.media_listener.start()
        
        # Configura a interface
        self.setup_ui()
        
        # Bind para fechar e redimensionar
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind('<Configure>', self.on_resize)
        
        # Bind para teclas de mídia
        self.setup_media_keys()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#1DB954", foreground="white", 
                       font=("Arial", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#1ed760")])
        
        # Container principal
        self.main_container = tk.Frame(self.root, bg="#121212")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Container horizontal
        self.content_wrapper = tk.Frame(self.main_container, bg="#121212")
        self.content_wrapper.pack(fill=tk.BOTH, expand=True)
        
        # Painel de Playlists (esquerda)
        self.playlist_panel = tk.Frame(self.content_wrapper, bg="#000000", width=250)
        self.playlist_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 5), pady=15)
        self.playlist_panel.pack_propagate(False)
        
        # Header do painel de playlists
        playlist_header = tk.Frame(self.playlist_panel, bg="#181818")
        playlist_header.pack(fill=tk.X, pady=(0, 10))
        
        playlist_title = tk.Label(playlist_header, text="📚 Playlists", 
                                  font=("Arial", 13, "bold"),
                                  bg="#181818", fg="#1DB954")
        playlist_title.pack(pady=10)
        
        # Botões de gerenciar playlists
        playlist_btn_frame = tk.Frame(self.playlist_panel, bg="#000000")
        playlist_btn_frame.pack(fill=tk.X, pady=5)
        
        add_playlist_btn = tk.Button(playlist_btn_frame, text="+ Nova", 
                                     font=("Arial", 9),
                                     bg="#1DB954", fg="white",
                                     command=self.add_new_playlist,
                                     borderwidth=0, padx=8, pady=4,
                                     cursor="hand2")
        add_playlist_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(add_playlist_btn, "Adicionar nova playlist")
        
        remove_playlist_btn = tk.Button(playlist_btn_frame, text="🗑", 
                                        font=("Arial", 9),
                                        bg="#282828", fg="white",
                                        command=self.remove_selected_playlist,
                                        borderwidth=0, padx=8, pady=4,
                                        cursor="hand2")
        remove_playlist_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(remove_playlist_btn, "Remover playlist selecionada")
        
        # Lista de playlists
        playlist_scroll_frame = tk.Frame(self.playlist_panel, bg="#000000")
        playlist_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        playlist_scrollbar = tk.Scrollbar(playlist_scroll_frame, bg="#282828")
        playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox = tk.Listbox(playlist_scroll_frame,
                                           yscrollcommand=playlist_scrollbar.set,
                                           bg="#181818", fg="white",
                                           font=("Arial", 10),
                                           selectbackground="#1DB954",
                                           selectforeground="white",
                                           borderwidth=0,
                                           highlightthickness=0,
                                           activestyle='none')
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        playlist_scrollbar.config(command=self.playlist_listbox.yview)
        
        self.playlist_listbox.bind('<<ListboxSelect>>', self.on_playlist_select)
        self.playlist_listbox.bind('<Double-Button-1>', self.on_playlist_double_click)
        
        # Carrega playlists salvas
        self.load_saved_playlists()
        
        # Container do conteúdo principal (direita)
        self.main_content = tk.Frame(self.content_wrapper, bg="#121212")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame superior - Título e botões
        self.top_frame = tk.Frame(self.main_content, bg="#121212", height=60)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
        self.top_frame.pack_propagate(False)
        
        title_label = tk.Label(self.top_frame, text="🎵 Music Player", 
                               font=("Arial", 20, "bold"), 
                               bg="#121212", fg="#1DB954")
        title_label.pack(side=tk.LEFT)
        
        # Botões do topo
        top_buttons_frame = tk.Frame(self.top_frame, bg="#121212")
        top_buttons_frame.pack(side=tk.RIGHT)
        
        # Botão de tema
        self.theme_btn = tk.Button(top_buttons_frame, text="🌙" if self.current_theme == 'dark' else "☀️", 
                                   font=("Arial", 14),
                                   bg="#282828", fg="white",
                                   command=self.toggle_theme,
                                   borderwidth=0, padx=10, pady=5,
                                   cursor="hand2")
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        ToolTip(self.theme_btn, "Alternar tema")
        
        # Botão de histórico
        history_btn = tk.Button(top_buttons_frame, text="📜", 
                               font=("Arial", 14),
                               bg="#282828", fg="white",
                               command=self.show_history,
                               borderwidth=0, padx=10, pady=5,
                               cursor="hand2")
        history_btn.pack(side=tk.RIGHT, padx=5)
        ToolTip(history_btn, "Ver histórico")
        
        self.mini_btn = tk.Button(top_buttons_frame, text="📐", 
                                  font=("Arial", 14),
                                  bg="#282828", fg="white",
                                  command=self.toggle_mini_mode,
                                  borderwidth=0, padx=10, pady=5,
                                  cursor="hand2")
        self.mini_btn.pack(side=tk.RIGHT, padx=5)
        ToolTip(self.mini_btn, "Modo mini player")
        
        load_btn = tk.Button(top_buttons_frame, text="📁", 
                            font=("Arial", 14),
                            bg="#1DB954", fg="white",
                            command=self.load_folder,
                            borderwidth=0, padx=10, pady=5,
                            cursor="hand2")
        load_btn.pack(side=tk.RIGHT, padx=5)
        ToolTip(load_btn, "Carregar pasta de músicas")
        
        # Frame central - Lista de músicas
        self.list_container = tk.Frame(self.main_content, bg="#181818", 
                                       relief=tk.FLAT, borderwidth=2)
        self.list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, 
                                 padx=15, pady=10)
        
        list_header = tk.Frame(self.list_container, bg="#282828", height=40)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        # Label e campo de busca
        list_label_frame = tk.Frame(list_header, bg="#282828")
        list_label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        list_label = tk.Label(list_label_frame, text="📚 Biblioteca de Músicas", 
                             font=("Arial", 12, "bold"), 
                             bg="#282828", fg="white")
        list_label.pack(side=tk.LEFT, anchor=tk.W, padx=15, pady=10)
        
        # Campo de busca
        search_frame = tk.Frame(list_label_frame, bg="#282828")
        search_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        self.search_entry = tk.Entry(search_frame, bg="#181818", fg="white",
                                     font=("Arial", 10),
                                     insertbackground="white",
                                     relief=tk.FLAT, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        self.search_entry.insert(0, "🔍 Buscar...")
        self.search_entry.bind('<FocusIn>', lambda e: self.search_entry.delete(0, tk.END) if self.search_entry.get() == "🔍 Buscar..." else None)
        self.search_entry.bind('<FocusOut>', lambda e: self.search_entry.insert(0, "🔍 Buscar...") if not self.search_entry.get() else None)
        
        # Botão favoritos
        fav_btn = tk.Button(search_frame, text="⭐", 
                           font=("Arial", 12),
                           bg="#282828", fg="#FFD700",
                           command=self.show_favorites,
                           borderwidth=0, padx=8, pady=2,
                           cursor="hand2")
        fav_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(fav_btn, "Ver favoritos")
        
        # Scrollbar e Listbox
        list_scroll_frame = tk.Frame(self.list_container, bg="#181818")
        list_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_scroll_frame, bg="#282828", 
                                troughcolor="#181818")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))
        
        self.music_listbox = tk.Listbox(list_scroll_frame, 
                                        yscrollcommand=scrollbar.set,
                                        bg="#282828", fg="white",
                                        font=("Arial", 11),
                                        selectbackground="#1DB954",
                                        selectforeground="white",
                                        borderwidth=0,
                                        highlightthickness=0,
                                        activestyle='none')
        self.music_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.music_listbox.yview)
        
        self.music_listbox.bind('<Double-Button-1>', self.on_song_double_click)
        self.music_listbox.bind('<Button-3>', self.show_song_context_menu)
        
        # Container de informação da música atual
        self.info_container = tk.Frame(self.main_content, bg="#282828", 
                                       relief=tk.FLAT, borderwidth=2)
        self.info_container.pack(side=tk.TOP, fill=tk.X, padx=15, pady=(0, 10))
        
        info_inner = tk.Frame(self.info_container, bg="#282828")
        info_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Ícone grande da música
        icon_label = tk.Label(info_inner, text="🎵", 
                             font=("Arial", 32),
                             bg="#282828", fg="#1DB954")
        icon_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Informações da música
        info_text_frame = tk.Frame(info_inner, bg="#282828")
        info_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        now_playing_label = tk.Label(info_text_frame, text="Tocando agora", 
                                     font=("Arial", 9),
                                     bg="#282828", fg="#B3B3B3")
        now_playing_label.pack(anchor=tk.W)
        
        self.current_song_label = tk.Label(info_text_frame, 
                                           text="Nenhuma música selecionada", 
                                           font=("Arial", 14, "bold"),
                                           bg="#282828", fg="white")
        self.current_song_label.pack(anchor=tk.W, pady=(2, 5))
        
        self.time_label = tk.Label(info_text_frame, text="00:00 / 00:00", 
                                   font=("Arial", 10),
                                   bg="#282828", fg="#B3B3B3")
        self.time_label.pack(anchor=tk.W)
        
        # NOVA: Barra de progresso interativa
        progress_frame = tk.Frame(info_text_frame, bg="#282828")
        progress_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.progress_canvas = tk.Canvas(progress_frame, height=6, bg="#404040", 
                                        highlightthickness=0, cursor="hand2")
        self.progress_canvas.pack(fill=tk.X)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 6, 
                                                                   fill="#1DB954", outline="")
        
        # Bind para clique na barra de progresso
        self.progress_canvas.bind('<Button-1>', self.seek_music)
        self.progress_canvas.bind('<B1-Motion>', self.seek_music)
        
        # Container de controles
        self.control_container = tk.Frame(self.main_content, bg="#181818", 
                                          relief=tk.FLAT, borderwidth=2)
        self.control_container.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 15))
        
        control_inner = tk.Frame(self.control_container, bg="#181818")
        control_inner.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Botões de controle centralizados
        btn_frame = tk.Frame(control_inner, bg="#181818")
        btn_frame.pack(pady=10)
        
        # Botão de repeat
        self.repeat_btn = tk.Button(btn_frame, text="🔁", 
                                    font=("Arial", 18),
                                    bg="#282828", fg="white",
                                    command=self.toggle_repeat,
                                    borderwidth=0, 
                                    width=3, height=1,
                                    cursor="hand2")
        self.repeat_btn.pack(side=tk.LEFT, padx=8)
        ToolTip(self.repeat_btn, "Modo de repetição")
        
        self.prev_btn = tk.Button(btn_frame, text="⏮", 
                                  font=("Arial", 18),
                                  bg="#282828", fg="white",
                                  command=self.previous_song,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.prev_btn.pack(side=tk.LEFT, padx=8)
        ToolTip(self.prev_btn, "Música anterior")
        
        self.play_btn = tk.Button(btn_frame, text="▶", 
                                  font=("Arial", 24),
                                  bg="#1DB954", fg="white",
                                  command=self.play_pause,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.play_btn.pack(side=tk.LEFT, padx=8)
        ToolTip(self.play_btn, "Play/Pause (Espaço)")
        
        self.next_btn = tk.Button(btn_frame, text="⏭", 
                                  font=("Arial", 18),
                                  bg="#282828", fg="white",
                                  command=self.next_song,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.next_btn.pack(side=tk.LEFT, padx=8)
        ToolTip(self.next_btn, "Próxima música")
        
        self.shuffle_btn = tk.Button(btn_frame, text="🔀", 
                                     font=("Arial", 18),
                                     bg="#1DB954" if self.shuffle_mode else "#282828", 
                                     fg="white",
                                     command=self.toggle_shuffle,
                                     borderwidth=0, 
                                     width=3, height=1,
                                     cursor="hand2")
        self.shuffle_btn.pack(side=tk.LEFT, padx=8)
        ToolTip(self.shuffle_btn, "Modo aleatório")
        
        # Controle de volume estilizado
        volume_frame = tk.Frame(control_inner, bg="#181818")
        volume_frame.pack(pady=10)
        
        volume_label = tk.Label(volume_frame, text="🔊", 
                               font=("Arial", 14),
                               bg="#181818", fg="white")
        volume_label.pack(side=tk.LEFT, padx=10)
        
        self.volume_slider = tk.Scale(volume_frame, 
                                      from_=0, to=100,
                                      orient=tk.HORIZONTAL,
                                      command=self.change_volume,
                                      bg="#181818", fg="white",
                                      highlightthickness=0,
                                      troughcolor="#404040",
                                      activebackground="#1DB954",
                                      sliderrelief=tk.FLAT,
                                      length=250,
                                      width=15,
                                      cursor="hand2",
                                      showvalue=0)  # Esconde valor numérico
        self.volume_slider.set(int(self.volume * 100))
        self.volume_slider.pack(side=tk.LEFT)
        ToolTip(self.volume_slider, "Volume (↑↓ ou M para mute)")
        
        # Label do volume
        self.volume_label = tk.Label(volume_frame, text=f"{int(self.volume * 100)}%", 
                                     font=("Arial", 10),
                                     bg="#181818", fg="#B3B3B3")
        self.volume_label.pack(side=tk.LEFT, padx=10)
    
    def seek_music(self, event):
        """Permite buscar posição na música clicando na barra"""
        if not self.is_playing or self.song_length == 0:
            return
        
        # Calcula posição clicada
        width = self.progress_canvas.winfo_width()
        click_x = event.x
        percentage = max(0, min(1, click_x / width))
        new_position = percentage * self.song_length
        
        try:
            # Para e reinicia música na nova posição
            pygame.mixer.music.stop()
            music = self.music_loader.get_music_by_index(self.current_index)
            if music:
                pygame.mixer.music.load(music['path'])
                pygame.mixer.music.play(start=new_position)
                self.song_position = new_position
                self.is_playing = True
                self.is_paused = False
        except Exception as e:
            print(f"Erro ao buscar posição: {e}")
    
    def toggle_repeat(self):
        """Alterna entre modos de repetição: off -> one -> all -> off"""
        modes = ['off', 'one', 'all']
        current_idx = modes.index(self.repeat_mode)
        self.repeat_mode = modes[(current_idx + 1) % len(modes)]
        self.config_manager.set('repeat_mode', self.repeat_mode)
        
        # Atualiza visual do botão
        if self.repeat_mode == 'off':
            self.repeat_btn.config(bg="#282828", text="🔁")
        elif self.repeat_mode == 'one':
            self.repeat_btn.config(bg="#1DB954", text="🔂")
        else:  # all
            self.repeat_btn.config(bg="#1DB954", text="🔁")
        
        mode_text = {"off": "desativado", "one": "repetir uma", "all": "repetir todas"}
        messagebox.showinfo("Modo de Repetição", f"Repetição: {mode_text[self.repeat_mode]}")
    
    def load_folder(self, folder_path=None):
        """Carrega músicas de uma pasta selecionada"""
        if folder_path is None:
            folder_path = filedialog.askdirectory(title="Selecione a pasta com músicas")
        
        if folder_path:
            self.current_folder = folder_path
            self.config_manager.set('last_folder', folder_path)
            music_list = self.music_loader.load_folder(folder_path)
            
            # Atualiza a listbox com animação suave
            self.music_listbox.delete(0, tk.END)
            for i, music in enumerate(music_list):
                # Adiciona número da música para melhor visualização
                display_name = f"{i+1:03d}. {music['name']}"
                self.music_listbox.insert(tk.END, display_name)
            
            if music_list:
                # Pergunta se deseja salvar como playlist
                if folder_path and not self.config_manager.get('last_folder') == folder_path:
                    save = messagebox.askyesno("Salvar Playlist", 
                                              f"✅ {len(music_list)} música(s) carregada(s)!\n\n"
                                              "Deseja salvar esta pasta como playlist?")
                    if save:
                        name = simpledialog.askstring("Nome da Playlist", 
                                                     "Digite um nome para a playlist:",
                                                     initialvalue=Path(folder_path).name)
                        if name:
                            if self.playlist_manager.add_playlist(folder_path, name):
                                self.load_saved_playlists()
                                messagebox.showinfo("Sucesso", "✅ Playlist salva!")
            else:
                messagebox.showwarning("Aviso", "⚠️ Nenhuma música encontrada na pasta!")
    
    def load_saved_playlists(self):
        """Carrega playlists salvas na listbox"""
        self.playlist_listbox.delete(0, tk.END)
        playlists = self.playlist_manager.get_playlists()
        for playlist in playlists:
            display_name = f"🎵 {playlist['name']}"
            self.playlist_listbox.insert(tk.END, display_name)
    
    def on_playlist_select(self, event):
        """Evento quando uma playlist é selecionada"""
        pass
    
    def on_playlist_double_click(self, event):
        """Evento de duplo clique em uma playlist"""
        selection = self.playlist_listbox.curselection()
        if selection:
            index = selection[0]
            playlists = self.playlist_manager.get_playlists()
            if index < len(playlists):
                playlist = playlists[index]
                self.load_playlist(playlist['path'])
    
    def load_playlist(self, path: str):
        """Carrega músicas de uma playlist específica"""
        if os.path.exists(path):
            self.current_folder = path
            self.current_playlist = path
            music_list = self.music_loader.load_folder(path)
            
            # Atualiza a listbox
            self.music_listbox.delete(0, tk.END)
            for i, music in enumerate(music_list):
                display_name = f"{i+1:03d}. {music['name']}"
                self.music_listbox.insert(tk.END, display_name)
            
            # Atualiza título
            playlist_info = self.playlist_manager.get_playlist_by_path(path)
            if playlist_info:
                self.root.title(f"Music Player - {playlist_info['name']}")
    
    def add_new_playlist(self):
        """Adiciona uma nova playlist"""
        folder = filedialog.askdirectory(title="Selecione a pasta para adicionar como playlist")
        if folder:
            name = simpledialog.askstring("Nome da Playlist", 
                                         "Digite um nome para a playlist:",
                                         initialvalue=Path(folder).name)
            if name:
                if self.playlist_manager.add_playlist(folder, name):
                    self.load_saved_playlists()
                    messagebox.showinfo("Sucesso", "✅ Playlist adicionada!")
                    self.load_playlist(folder)
                else:
                    messagebox.showwarning("Aviso", "⚠️ Esta playlist já existe!")
    
    def remove_selected_playlist(self):
        """Remove a playlist selecionada"""
        selection = self.playlist_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "⚠️ Selecione uma playlist para remover!")
            return
        
        index = selection[0]
        playlists = self.playlist_manager.get_playlists()
        if index < len(playlists):
            playlist = playlists[index]
            confirm = messagebox.askyesno("Confirmar", 
                                         f"Remover a playlist '{playlist['name']}'?\n\n"
                                         "(As músicas não serão deletadas)")
            if confirm:
                self.playlist_manager.remove_playlist(playlist['path'])
                self.load_saved_playlists()
                
                if self.current_playlist == playlist['path']:
                    self.music_listbox.delete(0, tk.END)
                    self.current_playlist = None
                    self.root.title("Music Player - Estilo Spotify")
