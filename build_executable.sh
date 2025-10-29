#!/bin/bash

# Script para gerar executável do Conversor Financeiro
# Execute: ./build_executable.sh

echo "🔨 Gerando executável do Conversor Financeiro..."

# Verificar se estamos no diretório correto
if [ ! -f "conversor_gui_moderno.py" ]; then
    echo "❌ Arquivo conversor_gui_moderno.py não encontrado!"
    echo "   Execute este script no diretório do projeto."
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "conversor_env" ]; then
    echo "📦 Ativando ambiente virtual..."
    source conversor_env/bin/activate
fi

# Verificar se PyInstaller está instalado
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
fi

# Criar ícone se não existir
if [ ! -f "app_icon.ico" ]; then
    echo "🎨 Criando ícone..."
    python3 -c "
from PIL import Image, ImageDraw
try:
    size = (64, 64)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([4, 4, 60, 60], radius=12, fill=(59, 130, 246, 255))
    draw.rectangle([24, 16, 32, 48], fill=(255, 255, 255, 255))
    draw.polygon([(32, 16), (40, 24), (32, 24)], fill=(255, 255, 255, 255))
    image.save('app_icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('✅ Ícone criado: app_icon.ico')
except Exception as e:
    print(f'⚠️ Erro ao criar ícone: {e}')
"
fi

# Gerar executável
echo "🔨 Gerando executável..."
pyinstaller --onefile --windowed --icon=app_icon.ico --name="ConversorFinanceiro" conversor_gui_moderno.py

# Verificar se o executável foi criado
if [ -f "dist/ConversorFinanceiro" ]; then
    echo "✅ Executável criado com sucesso!"
    echo "📁 Localização: dist/ConversorFinanceiro"
    
    # Obter tamanho do arquivo
    file_size=$(du -h "dist/ConversorFinanceiro" | cut -f1)
    echo "📊 Tamanho: $file_size"
    
    # Tornar executável
    chmod +x "dist/ConversorFinanceiro"
    echo "✅ Permissões de execução configuradas"
else
    echo "❌ Erro ao criar executável!"
    exit 1
fi

# Limpar arquivos temporários
echo "🧹 Limpando arquivos temporários..."
rm -rf build/ ConversorFinanceiro.spec

echo ""
echo "🎉 Processo concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Execute: ./dist/ConversorFinanceiro"
echo "   2. Ou navegue até a pasta dist e execute o arquivo"
echo ""
echo "🚀 O Conversor Financeiro está pronto para uso!"


