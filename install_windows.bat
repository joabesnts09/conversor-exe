@echo off
REM Script de Instalação - Conversor Financeiro para Windows
REM Execute este script no Windows para instalar todas as dependências

echo 🚀 Instalando Conversor Financeiro para Windows...
echo ================================================

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 Para instalar o Python:
    echo    1. Acesse: https://www.python.org/downloads/
    echo    2. Baixe Python 3.8 ou superior
    echo    3. Durante a instalação, marque "Add Python to PATH"
    echo    4. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado: 
python --version

REM Verificar se pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip não encontrado! Reinstale Python com pip.
    pause
    exit /b 1
)

echo ✅ pip encontrado:
pip --version

REM Atualizar pip
echo.
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo.
echo 📦 Instalando dependências Python...
if exist "requirements.txt" (
    echo 📄 Usando requirements.txt...
    pip install -r requirements.txt
) else (
    echo 📄 Instalando dependências manualmente...
    pip install customtkinter tkinterdnd2 pandas openpyxl pdfminer.six pypdfium2 pillow numpy python-dateutil pytz cryptography bcrypt requests urllib3 certifi charset-normalizer idna six packaging pyinstaller
)

REM Verificar instalação
echo.
echo 🔍 Verificando instalação...
python -c "
try:
    import customtkinter
    print('✅ CustomTkinter: OK')
except ImportError as e:
    print(f'❌ CustomTkinter: {e}')

try:
    import tkinterdnd2
    print('✅ TkinterDnD2: OK')
except ImportError as e:
    print(f'❌ TkinterDnD2: {e}')

try:
    import pandas
    print('✅ Pandas: OK')
except ImportError as e:
    print(f'❌ Pandas: {e}')

try:
    import openpyxl
    print('✅ OpenPyXL: OK')
except ImportError as e:
    print(f'❌ OpenPyXL: {e}')

try:
    import pdfminer
    print('✅ PDFMiner: OK')
except ImportError as e:
    print(f'❌ PDFMiner: {e}')

try:
    import pypdfium2
    print('✅ PyPDFium2: OK')
except ImportError as e:
    print(f'❌ PyPDFium2: {e}')

try:
    from PIL import Image
    print('✅ Pillow: OK')
except ImportError as e:
    print(f'❌ Pillow: {e}')

try:
    import numpy
    print('✅ NumPy: OK')
except ImportError as e:
    print(f'❌ NumPy: {e}')
"

REM Criar script de execução
echo.
echo 📝 Criando script de execução...
echo @echo off > run_conversor.bat
echo REM Script para executar o Conversor Financeiro >> run_conversor.bat
echo echo 🚀 Iniciando Conversor Financeiro... >> run_conversor.bat
echo python conversor_gui_moderno.py >> run_conversor.bat
echo pause >> run_conversor.bat

echo ✅ Script de execução criado: run_conversor.bat

REM Criar script para gerar executável
echo.
echo 📝 Criando script para gerar executável...
echo @echo off > build_executable.bat
echo REM Script para gerar executável do Conversor Financeiro >> build_executable.bat
echo echo 🔨 Gerando executável... >> build_executable.bat
echo pyinstaller --onefile --windowed --icon=app_icon.ico --name="ConversorFinanceiro" conversor_gui_moderno.py >> build_executable.bat
echo echo ✅ Executável criado em: dist\ConversorFinanceiro.exe >> build_executable.bat
echo pause >> build_executable.bat

echo ✅ Script de build criado: build_executable.bat

echo.
echo ✅ Instalação concluída!
echo.
echo 📋 Próximos passos:
echo    1. Para executar: python conversor_gui_moderno.py
echo    2. Para executar (script): run_conversor.bat
echo    3. Para gerar executável: build_executable.bat
echo.
echo 🎉 Conversor Financeiro está pronto para Windows!
pause


