"""
Script de instalação e verificação do ambiente
"""
import sys
import subprocess

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_dependencies():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def verify_installation():
    """Verifica se tudo está instalado"""
    print("\n🔍 Verificando instalação...")
    
    modules = {
        'pygame': 'Reprodução de áudio',
        'mutagen': 'Leitura de metadados',
        'win32api': 'Teclas de mídia (pywin32)',
        'PIL': 'Processamento de imagens (Pillow)',
        'tkinter': 'Interface gráfica'
    }
    
    all_ok = True
    for module, desc in modules.items():
        try:
            __import__(module)
            print(f"✅ {desc}")
        except ImportError:
            print(f"❌ {desc} - {module} não encontrado")
            all_ok = False
    
    return all_ok

def main():
    """Função principal"""
    print("="*60)
    print("  🎵 Music Player - Setup")
    print("="*60 + "\n")
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not verify_installation():
        print("\n⚠️  Algumas dependências falharam")
        print("   Tente instalar manualmente:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("  ✅ Tudo pronto!")
    print("="*60)
    print("\n▶️  Execute: python main.py")

if __name__ == '__main__':
    main()
