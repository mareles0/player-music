"""
Utilitário para capturar teclas de mídia globais do Windows
"""
import threading
try:
    import win32api
    import win32con
    MEDIA_KEYS_AVAILABLE = True
except ImportError:
    MEDIA_KEYS_AVAILABLE = False

class MediaKeyListener:
    """Listener para teclas de mídia do Windows"""
    
    def __init__(self, on_play_pause=None, on_next=None, on_previous=None, on_volume_up=None, on_volume_down=None, on_mute=None):
        self.on_play_pause = on_play_pause
        self.on_next = on_next
        self.on_previous = on_previous
        self.on_volume_up = on_volume_up
        self.on_volume_down = on_volume_down
        self.on_mute = on_mute
        self.running = False
        self.thread = None
    
    def start(self):
        """Inicia o listener em uma thread separada"""
        if not MEDIA_KEYS_AVAILABLE:
            print("⚠️  pywin32 não disponível. Teclas de mídia globais não funcionarão.")
            return False
        
        if self.running:
            return True
        
        self.running = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Para o listener"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _listen(self):
        """Loop principal de escuta (rodando em thread separada)"""
        # Códigos de teclas de mídia do Windows
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1
        VK_MEDIA_STOP = 0xB2
        VK_MEDIA_PLAY_PAUSE = 0xB3
        VK_VOLUME_MUTE = 0xAD
        VK_VOLUME_DOWN = 0xAE
        VK_VOLUME_UP = 0xAF
        
        last_state = {}
        
        while self.running:
            try:
                # Verifica Play/Pause
                if win32api.GetAsyncKeyState(VK_MEDIA_PLAY_PAUSE) & 0x8000:
                    if not last_state.get('play_pause', False):
                        if self.on_play_pause:
                            self.on_play_pause()
                        last_state['play_pause'] = True
                else:
                    last_state['play_pause'] = False
                
                # Verifica Next
                if win32api.GetAsyncKeyState(VK_MEDIA_NEXT_TRACK) & 0x8000:
                    if not last_state.get('next', False):
                        if self.on_next:
                            self.on_next()
                        last_state['next'] = True
                else:
                    last_state['next'] = False
                
                # Verifica Previous
                if win32api.GetAsyncKeyState(VK_MEDIA_PREV_TRACK) & 0x8000:
                    if not last_state.get('prev', False):
                        if self.on_previous:
                            self.on_previous()
                        last_state['prev'] = True
                else:
                    last_state['prev'] = False
                
                # Verifica Mute
                if win32api.GetAsyncKeyState(VK_VOLUME_MUTE) & 0x8000:
                    if not last_state.get('mute', False):
                        if self.on_mute:
                            self.on_mute()
                        last_state['mute'] = True
                else:
                    last_state['mute'] = False
                
                # Verifica Volume Up
                if win32api.GetAsyncKeyState(VK_VOLUME_UP) & 0x8000:
                    if not last_state.get('vol_up', False):
                        if self.on_volume_up:
                            self.on_volume_up()
                        last_state['vol_up'] = True
                else:
                    last_state['vol_up'] = False
                
                # Verifica Volume Down
                if win32api.GetAsyncKeyState(VK_VOLUME_DOWN) & 0x8000:
                    if not last_state.get('vol_down', False):
                        if self.on_volume_down:
                            self.on_volume_down()
                        last_state['vol_down'] = True
                else:
                    last_state['vol_down'] = False
                
                # Pequeno delay para não sobrecarregar CPU
                import time
                time.sleep(0.05)
            except Exception as e:
                print(f"Erro no listener de teclas: {e}")
                break
