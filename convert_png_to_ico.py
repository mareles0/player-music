"""
Converte PNG para ICO com todos os tamanhos necessários
"""
from PIL import Image
import os

def convert_png_to_ico():
    """Converte o PNG para ICO com múltiplos tamanhos"""
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    
    # Procura arquivo PNG
    png_files = [f for f in os.listdir(assets_path) if f.lower().endswith('.png')]
    
    if not png_files:
        print("❌ Nenhum arquivo PNG encontrado em assets/")
        return False
    
    png_file = os.path.join(assets_path, png_files[0])
    print(f"📸 PNG encontrado: {png_files[0]}")
    
    # Abre a imagem
    img = Image.open(png_file)
    print(f"📐 Tamanho original: {img.size}")
    
    # Remove transparência se houver e converte para RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Cria versões em diferentes tamanhos
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for size in icon_sizes:
        # Redimensiona mantendo proporção
        img_resized = img.copy()
        img_resized.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Cria nova imagem com fundo se necessário
        new_img = Image.new('RGBA', size, (0, 0, 0, 0))
        
        # Centraliza
        paste_x = (size[0] - img_resized.size[0]) // 2
        paste_y = (size[1] - img_resized.size[1]) // 2
        new_img.paste(img_resized, (paste_x, paste_y), img_resized)
        
        images.append(new_img)
        print(f"  ✓ Criado: {size[0]}x{size[1]}")
    
    # Salva como .ico
    ico_path = os.path.join(assets_path, 'app_icon.ico')
    images[0].save(ico_path, format='ICO', sizes=[img.size for img in images])
    
    print(f"\n✅ Ícone criado: {ico_path}")
    print(f"📊 Tamanho do arquivo: {os.path.getsize(ico_path) / 1024:.1f} KB")
    
    return ico_path

if __name__ == "__main__":
    try:
        convert_png_to_ico()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
