"""
Script para gerar o executável (.exe) do Music Player
Uso: python build_exe.py
"""
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...\n")
    
    required = {
        'pygame': 'pygame==2.5.2',
        'mutagen': 'mutagen==1.47.0',
        'win32api': 'pywin32==306',  # pywin32 usa win32api como módulo
        'PyInstaller': 'pyinstaller==6.3.0'
    }
    
    missing = []
    for module, package in required.items():
        try:
            if module == 'PyInstaller':
                __import__('PyInstaller')
            elif module == 'win32api':
                __import__('win32api')
            else:
                __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} não instalado")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Instale as dependências faltantes:")
        print(f"   pip install {' '.join(missing)}")
        sys.exit(1)
    
    print("\n✅ Todas as dependências instaladas!\n")

def get_icon():
    """Encontra o ícone na pasta assets"""
    assets_path = Path(__file__).parent / 'assets'
    
    if not assets_path.exists():
        return None
    
    # Procura pelo ícone do Spotify
    icon_path = assets_path / 'spotify.ico'
    if icon_path.exists() and icon_path.stat().st_size > 0:
        print(f"🎨 Ícone: {icon_path.name}")
        return str(icon_path)
    
    return None

def build_exe():
    """Gera o executável usando PyInstaller"""
    print("🔨 Iniciando build do executável...\n")
    
    icon_path = get_icon()
    
    # Comando PyInstaller
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=MusicPlayer',
        '--clean',
        '--noconfirm',
    ]
    
    if icon_path:
        cmd.append(f'--icon={icon_path}')
    
    cmd.append('main.py')
    
    print("📝 Executando:", ' '.join(cmd))
    print("\n" + "="*60)
    
    # Executa o PyInstaller
    try:
        subprocess.run(cmd, check=True)
        
        print("="*60)
        print("\n✅ Build concluído com sucesso!")
        
        # Verifica o executável gerado
        exe_path = Path(__file__).parent / 'dist' / 'MusicPlayer.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📂 Executável: {exe_path}")
            print(f"📊 Tamanho: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError:
        print("\n❌ Erro ao gerar executável")
        sys.exit(1)

def main():
    """Função principal"""
    print("="*60)
    print("  🎵 Music Player - Build System")
    print("="*60 + "\n")
    
    check_dependencies()
    build_exe()
    
    print("\n" + "="*60)
    print("  ✨ Pronto para distribuir!")
    print("="*60)

if __name__ == '__main__':
    main()
