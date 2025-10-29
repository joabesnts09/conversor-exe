@echo off
REM Script para gerar executável do Conversor Financeiro para Windows
REM Execute este script no Windows com Python e PyInstaller instalados

echo 🔨 Gerando executável do Conversor Financeiro para Windows...

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Verificar se PyInstaller está instalado
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
)

REM Instalar dependências se necessário
echo 📦 Verificando dependências...
pip install -r requirements.txt

REM Criar ícone se não existir
if not exist "app_icon.ico" (
    echo 🎨 Criando ícone...
    python -c "
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
)

REM Gerar executável para Windows
echo 🔨 Gerando executável para Windows...
pyinstaller --onefile --windowed --icon=app_icon.ico --name="ConversorFinanceiro" conversor_gui_moderno.py

REM Limpar arquivos temporários
echo 🧹 Limpando arquivos temporários...
rmdir /s /q build
del ConversorFinanceiro.spec

echo ✅ Executável criado em: dist\ConversorFinanceiro.exe
echo 🚀 Para executar: dist\ConversorFinanceiro.exe
pause


