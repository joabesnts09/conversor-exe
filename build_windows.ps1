# Script PowerShell para gerar executável do Conversor Financeiro para Windows
# Execute: powershell -ExecutionPolicy Bypass -File build_windows.ps1

Write-Host "🔨 Gerando executável do Conversor Financeiro para Windows..." -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado! Instale Python 3.8+ primeiro." -ForegroundColor Red
    Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se pip está instalado
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip não encontrado! Reinstale Python com pip." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se PyInstaller está instalado
try {
    python -c "import PyInstaller" 2>$null
    Write-Host "✅ PyInstaller encontrado" -ForegroundColor Green
} catch {
    Write-Host "📦 Instalando PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Instalar dependências
Write-Host "📦 Instalando/atualizando dependências..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "⚠️ requirements.txt não encontrado, instalando dependências manualmente..." -ForegroundColor Yellow
    $dependencies = @(
        "customtkinter",
        "tkinterdnd2", 
        "pandas",
        "numpy",
        "openpyxl",
        "pdfminer.six",
        "pypdfium2",
        "pillow",
        "python-dateutil",
        "pytz",
        "cryptography",
        "bcrypt",
        "requests",
        "urllib3",
        "certifi",
        "charset-normalizer",
        "idna",
        "six",
        "packaging"
    )
    
    foreach ($dep in $dependencies) {
        Write-Host "   Instalando $dep..." -ForegroundColor Cyan
        pip install $dep
    }
}

# Criar ícone se não existir
if (-not (Test-Path "app_icon.ico")) {
    Write-Host "🎨 Criando ícone..." -ForegroundColor Yellow
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
}

# Verificar se o arquivo principal existe
if (-not (Test-Path "conversor_gui_moderno.py")) {
    Write-Host "❌ conversor_gui_moderno.py não encontrado!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Gerar executável para Windows
Write-Host "🔨 Gerando executável para Windows..." -ForegroundColor Yellow
pyinstaller --onefile --windowed --icon=app_icon.ico --name="ConversorFinanceiro" conversor_gui_moderno.py

# Verificar se o executável foi criado
if (Test-Path "dist\ConversorFinanceiro.exe") {
    Write-Host "✅ Executável criado com sucesso!" -ForegroundColor Green
    Write-Host "📁 Localização: dist\ConversorFinanceiro.exe" -ForegroundColor Cyan
    
    # Obter tamanho do arquivo
    $fileSize = (Get-Item "dist\ConversorFinanceiro.exe").Length / 1MB
    Write-Host "📊 Tamanho: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host "❌ Erro ao criar executável!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Limpar arquivos temporários
Write-Host "🧹 Limpando arquivos temporários..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "ConversorFinanceiro.spec") { Remove-Item -Force "ConversorFinanceiro.spec" }

Write-Host ""
Write-Host "🎉 Processo concluído com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Execute: dist\ConversorFinanceiro.exe" -ForegroundColor White
Write-Host "   2. Ou navegue até a pasta dist e clique duas vezes no executável" -ForegroundColor White
Write-Host ""
Write-Host "🚀 O Conversor Financeiro está pronto para Windows!" -ForegroundColor Green

Read-Host "Pressione Enter para sair"


