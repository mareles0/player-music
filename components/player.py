"""
Player de Música com Interface Gráfica
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

class MusicPlayer:
    """Classe principal do reprodutor de música"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Player - Estilo Spotify")
        self.root.geometry("900x600")
        self.root.minsize(400, 300)
        self.root.configure(bg="#121212")
        
        # Define ícone do aplicativo
        self.set_app_icon()
        
        # Inicializa pygame mixer
        pygame.mixer.init()
        
        # Variáveis do player
        self.music_loader = MusicLoader()
        self.playlist_manager = PlaylistManager()
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        self.current_folder = None
        self.current_playlist = None
        self.is_mini_mode = False
        self.shuffle_mode = False
        self.shuffle_history = []  # Músicas já tocadas no shuffle
        self.shuffle_queue = []    # Fila de músicas para tocar
        self.song_length = 0       # Duração total da música em segundos
        self.song_position = 0     # Posição atual da música
        
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
        
        # Container horizontal: Playlists à esquerda, conteúdo principal à direita
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
        
        remove_playlist_btn = tk.Button(playlist_btn_frame, text="🗑", 
                                        font=("Arial", 9),
                                        bg="#282828", fg="white",
                                        command=self.remove_selected_playlist,
                                        borderwidth=0, padx=8, pady=4,
                                        cursor="hand2")
        remove_playlist_btn.pack(side=tk.LEFT, padx=5)
        
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
        
        self.mini_btn = tk.Button(top_buttons_frame, text="📐", 
                                  font=("Arial", 14),
                                  bg="#282828", fg="white",
                                  command=self.toggle_mini_mode,
                                  borderwidth=0, padx=10, pady=5,
                                  cursor="hand2")
        self.mini_btn.pack(side=tk.RIGHT, padx=5)
        
        load_btn = tk.Button(top_buttons_frame, text="📁", 
                            font=("Arial", 14),
                            bg="#1DB954", fg="white",
                            command=self.load_folder,
                            borderwidth=0, padx=10, pady=5,
                            cursor="hand2")
        load_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame central - Lista de músicas (responsivo)
        self.list_container = tk.Frame(self.main_content, bg="#181818", 
                                       relief=tk.FLAT, borderwidth=2)
        self.list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, 
                                 padx=15, pady=10)
        
        list_header = tk.Frame(self.list_container, bg="#282828", height=40)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        list_label = tk.Label(list_header, text="📚 Biblioteca de Músicas", 
                             font=("Arial", 12, "bold"), 
                             bg="#282828", fg="white")
        list_label.pack(anchor=tk.W, padx=15, pady=10)
        
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
        
        # Container de informação da música atual (card estilo Spotify)
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
        
        # Container de controles (fixo na parte inferior)
        self.control_container = tk.Frame(self.main_content, bg="#181818", 
                                          relief=tk.FLAT, borderwidth=2)
        self.control_container.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 15))
        
        control_inner = tk.Frame(self.control_container, bg="#181818")
        control_inner.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Botões de controle centralizados
        btn_frame = tk.Frame(control_inner, bg="#181818")
        btn_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(btn_frame, text="⏮", 
                                  font=("Arial", 18),
                                  bg="#282828", fg="white",
                                  command=self.previous_song,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.prev_btn.pack(side=tk.LEFT, padx=8)
        
        self.play_btn = tk.Button(btn_frame, text="▶", 
                                  font=("Arial", 24),
                                  bg="#1DB954", fg="white",
                                  command=self.play_pause,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.play_btn.pack(side=tk.LEFT, padx=8)
        
        self.next_btn = tk.Button(btn_frame, text="⏭", 
                                  font=("Arial", 18),
                                  bg="#282828", fg="white",
                                  command=self.next_song,
                                  borderwidth=0, 
                                  width=3, height=1,
                                  cursor="hand2")
        self.next_btn.pack(side=tk.LEFT, padx=8)
        
        self.shuffle_btn = tk.Button(btn_frame, text="🔀", 
                                     font=("Arial", 18),
                                     bg="#282828", fg="white",
                                     command=self.toggle_shuffle,
                                     borderwidth=0, 
                                     width=3, height=1,
                                     cursor="hand2")
        self.shuffle_btn.pack(side=tk.LEFT, padx=8)
        
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
                                      cursor="hand2")
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT)
    
    def load_folder(self):
        """Carrega músicas de uma pasta selecionada"""
        folder = filedialog.askdirectory(title="Selecione a pasta com músicas")
        if folder:
            self.current_folder = folder
            music_list = self.music_loader.load_folder(folder)
            
            # Atualiza a listbox
            self.music_listbox.delete(0, tk.END)
            for music in music_list:
                self.music_listbox.insert(tk.END, music['name'])
            
            if music_list:
                # Pergunta se deseja salvar como playlist
                save = messagebox.askyesno("Salvar Playlist", 
                                          f"{len(music_list)} música(s) carregada(s)!\n\n"
                                          "Deseja salvar esta pasta como playlist?")
                if save:
                    name = simpledialog.askstring("Nome da Playlist", 
                                                 "Digite um nome para a playlist:",
                                                 initialvalue=Path(folder).name)
                    if name:
                        if self.playlist_manager.add_playlist(folder, name):
                            self.load_saved_playlists()
                            messagebox.showinfo("Sucesso", "Playlist salva com sucesso!")
            else:
                messagebox.showwarning("Aviso", 
                                      "Nenhuma música encontrada na pasta!")
    
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
            for music in music_list:
                self.music_listbox.insert(tk.END, music['name'])
            
            # Atualiza seleção visual na playlist
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
                    messagebox.showinfo("Sucesso", "Playlist adicionada com sucesso!")
                    
                    # Carrega automaticamente a nova playlist
                    self.load_playlist(folder)
                else:
                    messagebox.showwarning("Aviso", "Esta playlist já existe!")
    
    def remove_selected_playlist(self):
        """Remove a playlist selecionada"""
        selection = self.playlist_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma playlist para remover!")
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
                
                # Limpa a lista de músicas se era a playlist atual
                if self.current_playlist == playlist['path']:
                    self.music_listbox.delete(0, tk.END)
                    self.current_playlist = None
                    self.root.title("Music Player - Estilo Spotify")
    
    def on_song_double_click(self, event):
        """Evento de duplo clique em uma música"""
        selection = self.music_listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_music()
    
    def play_music(self):
        """Reproduz a música atual"""
        if self.current_index < 0:
            return
        
        music = self.music_loader.get_music_by_index(self.current_index)
        if music:
            try:
                pygame.mixer.music.load(music['path'])
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self.play_btn.config(text="⏸")
                self.current_song_label.config(text=f"♫ {music['name']}")
                
                # Obtém duração da música
                try:
                    from mutagen import File
                    audio = File(music['path'])
                    if audio and audio.info:
                        self.song_length = int(audio.info.length)
                    else:
                        self.song_length = 0
                except:
                    # Se mutagen não estiver disponível, usa estimativa
                    self.song_length = 0
                
                self.song_position = 0
                
                # Destaca a música na lista
                self.music_listbox.selection_clear(0, tk.END)
                self.music_listbox.selection_set(self.current_index)
                self.music_listbox.see(self.current_index)
                
                # Inicia o update do tempo
                self.update_time()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao reproduzir música: {e}")
    
    def play_pause(self):
        """Alterna entre play e pause"""
        # Se há música carregada e tocando
        if self.is_playing and not self.is_paused:
            # Pausa
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(text="▶")
        elif self.is_playing and self.is_paused:
            # Despausa
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.config(text="⏸")
        elif self.current_index >= 0:
            # Inicia música atual
            self.play_music()
        elif self.music_listbox.size() > 0:
            # Se nenhuma música está selecionada, toca a primeira
            self.current_index = 0
            self.play_music()
    
    def next_song(self):
        """Toca a próxima música"""
        if self.music_listbox.size() == 0:
            return
        
        if self.shuffle_mode:
            self.play_next_shuffle()
        else:
            self.current_index = (self.current_index + 1) % self.music_listbox.size()
            self.play_music()
    
    def previous_song(self):
        """Toca a música anterior"""
        if self.music_listbox.size() == 0:
            return
        
        self.current_index = (self.current_index - 1) % self.music_listbox.size()
        self.play_music()
    
    def change_volume(self, val):
        """Altera o volume"""
        self.volume = float(val) / 100
        pygame.mixer.music.set_volume(self.volume)
        # Atualiza estado de mute
        if self.volume > 0:
            self.is_muted = False
    
    def format_time(self, seconds):
        """Formata segundos em MM:SS"""
        if seconds < 0:
            seconds = 0
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def update_time(self):
        """Atualiza o tempo de reprodução"""
        if self.is_playing and not self.is_paused:
            # Verifica se a música terminou
            if not pygame.mixer.music.get_busy():
                self.next_song()
                return
            
            # Atualiza posição atual
            try:
                # pygame.mixer.music.get_pos() retorna milissegundos desde o início
                pos_ms = pygame.mixer.music.get_pos()
                if pos_ms > 0:
                    self.song_position = pos_ms / 1000.0
                else:
                    self.song_position += 1
                
                # Atualiza label de tempo
                current_time = self.format_time(self.song_position)
                if self.song_length > 0:
                    total_time = self.format_time(self.song_length)
                    self.time_label.config(text=f"{current_time} / {total_time}")
                else:
                    self.time_label.config(text=f"{current_time} / --:--")
            except:
                pass
        
        self.root.after(1000, self.update_time)
    
    def toggle_mini_mode(self):
        """Alterna entre modo completo e mini player"""
        self.is_mini_mode = not self.is_mini_mode
        
        if self.is_mini_mode:
            # Modo mini - esconde lista e playlists, reduz tamanho
            self.list_container.pack_forget()
            self.playlist_panel.pack_forget()
            self.root.geometry("500x320")
            self.root.minsize(450, 320)
            self.mini_btn.config(text="📊")
        else:
            # Modo completo - restaura layout original
            # Re-empacota painel de playlists
            self.playlist_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 5), pady=15)
            self.playlist_panel.pack_propagate(False)
            
            # Garante que main_content está empacotado
            self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Re-empacota lista de músicas no lugar correto
            # Primeiro garante a ordem: top_frame, list_container, info_container, control_container
            self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
            
            self.list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, 
                                    padx=15, pady=10)
            
            self.info_container.pack(side=tk.TOP, fill=tk.X, padx=15, pady=(0, 10))
            
            self.control_container.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 15))
            
            # Restaura tamanho e configurações
            self.root.geometry("900x600")
            self.root.minsize(400, 300)
            self.mini_btn.config(text="📐")
            
            # Força atualização do layout
            self.root.update_idletasks()
    
    def on_resize(self, event):
        """Ajusta elementos quando a janela é redimensionada"""
        # Evento de redimensionamento - permite responsividade
        pass
    
    def toggle_shuffle(self):
        """Alterna modo shuffle on/off"""
        self.shuffle_mode = not self.shuffle_mode
        
        if self.shuffle_mode:
            # Ativa shuffle
            self.shuffle_btn.config(bg="#1DB954")
            self.initialize_shuffle()
            messagebox.showinfo("Shuffle Ativado", 
                              "Modo aleatório ativado!\n\n"
                              "As músicas serão tocadas em ordem aleatória.\n"
                              "O histórico é salvo para não repetir.")
        else:
            # Desativa shuffle
            self.shuffle_btn.config(bg="#282828")
            self.shuffle_history.clear()
            self.shuffle_queue.clear()
    
    def initialize_shuffle(self):
        """Inicializa o modo shuffle criando fila aleatória"""
        total_songs = self.music_listbox.size()
        if total_songs == 0:
            return
        
        # Cria lista de todos os índices
        all_indices = list(range(total_songs))
        
        # Remove a música atual da lista se houver
        if self.current_index >= 0 and self.current_index in all_indices:
            all_indices.remove(self.current_index)
        
        # Embaralha
        random.shuffle(all_indices)
        
        # Define como fila
        self.shuffle_queue = all_indices
        self.shuffle_history = []
        
        # Adiciona música atual ao histórico se houver
        if self.current_index >= 0:
            self.shuffle_history.append(self.current_index)
    
    def play_next_shuffle(self):
        """Toca a próxima música no modo shuffle"""
        # Se a fila acabou, todas as músicas foram tocadas
        if len(self.shuffle_queue) == 0:
            # Reinicia o shuffle excluindo o histórico
            messagebox.showinfo("Shuffle", 
                              "Todas as músicas foram tocadas!\n\n"
                              "Reiniciando playlist em modo aleatório.")
            self.initialize_shuffle()
            
            if len(self.shuffle_queue) == 0:
                return
        
        # Pega próxima música da fila
        self.current_index = self.shuffle_queue.pop(0)
        self.shuffle_history.append(self.current_index)
        self.play_music()
        
        # Salva histórico
        self.save_shuffle_history()
    
    def save_shuffle_history(self):
        """Salva histórico de músicas tocadas no shuffle"""
        if not self.current_playlist:
            return
        
        try:
            import json
            history_file = Path.home() / ".music_player" / "shuffle_history.json"
            history_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Carrega histórico existente
            history_data = {}
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
            
            # Salva histórico da playlist atual
            history_data[self.current_playlist] = {
                'history': self.shuffle_history[-50:],  # Últimas 50
                'queue': self.shuffle_queue
            }
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar histórico shuffle: {e}")
    
    def load_shuffle_history(self):
        """Carrega histórico de shuffle salvo"""
        if not self.current_playlist:
            return
        
        try:
            import json
            history_file = Path.home() / ".music_player" / "shuffle_history.json"
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                if self.current_playlist in history_data:
                    data = history_data[self.current_playlist]
                    self.shuffle_history = data.get('history', [])
                    self.shuffle_queue = data.get('queue', [])
        except Exception as e:
            print(f"Erro ao carregar histórico shuffle: {e}")
    
    def set_app_icon(self):
        """Define o ícone da janela do aplicativo"""
        try:
            # Tenta carregar o arquivo .ico
            icon_path = Path(__file__).parent.parent / 'assets' / 'spotify.ico'
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
            else:
                # Se não houver .ico, tenta usar PNG
                icon_png = Path(__file__).parent.parent / 'assets' / 'spotify.png'
                if icon_png.exists():
                    from PIL import Image, ImageTk
                    img = Image.open(str(icon_png))
                    photo = ImageTk.PhotoImage(img)
                    self.root.iconphoto(True, photo)
                    # Guarda referência para não ser coletado pelo garbage collector
                    self.root._icon_photo = photo
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o ícone: {e}")
    
    def setup_media_keys(self):
        """Configura atalhos de teclado para controle de mídia"""
        # Teclas de espaço para play/pause
        self.root.bind('<space>', lambda e: self.play_pause())
        
        # Teclas de seta para navegação
        self.root.bind('<Left>', lambda e: self.previous_song())
        self.root.bind('<Right>', lambda e: self.next_song())
        
        # Teclas de volume
        self.root.bind('<Up>', lambda e: self.increase_volume())
        self.root.bind('<Down>', lambda e: self.decrease_volume())
        
        # Tecla M para mute
        self.root.bind('m', lambda e: self.toggle_mute())
        self.root.bind('M', lambda e: self.toggle_mute())
        
        # Atalhos adicionais
        self.root.bind('<Control-Right>', lambda e: self.next_song())
        self.root.bind('<Control-Left>', lambda e: self.previous_song())
        self.root.bind('<Control-space>', lambda e: self.play_pause())
        
        # Variável para rastrear mute
        self.is_muted = False
        self.volume_before_mute = self.volume
    
    def toggle_mute(self):
        """Alterna entre mudo e volume normal"""
        if self.is_muted:
            # Restaura volume
            pygame.mixer.music.set_volume(self.volume_before_mute)
            self.volume_slider.set(int(self.volume_before_mute * 100))
            self.is_muted = False
        else:
            # Salva volume atual e muta
            self.volume_before_mute = self.volume
            pygame.mixer.music.set_volume(0)
            self.volume_slider.set(0)
            self.is_muted = True
    
    def increase_volume(self):
        """Aumenta o volume em 5%"""
        current = self.volume_slider.get()
        new_volume = min(100, current + 5)
        self.volume_slider.set(new_volume)
        self.change_volume(new_volume)
    
    def decrease_volume(self):
        """Diminui o volume em 5%"""
        current = self.volume_slider.get()
        new_volume = max(0, current - 5)
        self.volume_slider.set(new_volume)
        self.change_volume(new_volume)
    
    def on_close(self):
        """Evento ao fechar a janela"""
        # Para o listener de teclas de mídia
        if hasattr(self, 'media_listener'):
            self.media_listener.stop()
        
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()
