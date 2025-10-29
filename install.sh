#!/bin/bash

# Script de Instalação - Conversor Financeiro
# Este script instala todas as dependências necessárias para o Conversor Financeiro

echo "🚀 Instalando Conversor Financeiro..."
echo "=================================="

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
else
    echo "✅ Python 3 encontrado: $(python3 --version)"
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt install python3-pip -y
else
    echo "✅ pip3 encontrado: $(pip3 --version)"
fi

# Criar ambiente virtual (opcional, mas recomendado)
echo ""
echo "📦 Criando ambiente virtual..."
python3 -m venv conversor_env
source conversor_env/bin/activate

# Atualizar pip
echo "🔄 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências do sistema (necessárias para algumas bibliotecas)
echo ""
echo "📋 Instalando dependências do sistema..."
sudo apt update
sudo apt install -y \
    python3-tk \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev

# Instalar dependências Python
echo ""
echo "📦 Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    echo "📄 Usando requirements.txt..."
    pip install -r requirements.txt
else
    echo "📄 Instalando dependências manualmente..."
    pip install \
        customtkinter \
        tkinterdnd2 \
        pandas \
        openpyxl \
        pdfminer.six \
        pypdfium2 \
        pillow \
        numpy \
        python-dateutil \
        pytz \
        cryptography \
        bcrypt \
        charset-normalizer \
        requests \
        urllib3 \
        certifi \
        idna \
        six \
        pyinstaller
fi

# Verificar instalação
echo ""
echo "🔍 Verificando instalação..."
python3 -c "
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

# Criar script de execução
echo ""
echo "📝 Criando script de execução..."
cat > run_conversor.sh << 'EOF'
#!/bin/bash
# Script para executar o Conversor Financeiro

# Ativar ambiente virtual se existir
if [ -d "conversor_env" ]; then
    source conversor_env/bin/activate
fi

# Executar o aplicativo
if [ -f "conversor_gui_moderno.py" ]; then
    echo "🚀 Iniciando Conversor Financeiro..."
    python3 conversor_gui_moderno.py
elif [ -f "dist/ConversorFinanceiro" ]; then
    echo "🚀 Iniciando Conversor Financeiro (executável)..."
    ./dist/ConversorFinanceiro
else
    echo "❌ Arquivo do Conversor Financeiro não encontrado!"
    echo "   Certifique-se de que conversor_gui_moderno.py ou dist/ConversorFinanceiro existe."
fi
EOF

chmod +x run_conversor.sh

# Criar script para gerar executável
echo ""
echo "📝 Criando script para gerar executável..."
cat > build_executable.sh << 'EOF'
#!/bin/bash
# Script para gerar executável do Conversor Financeiro

echo "🔨 Gerando executável do Conversor Financeiro..."

# Ativar ambiente virtual se existir
if [ -d "conversor_env" ]; then
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

# Limpar arquivos temporários
echo "🧹 Limpando arquivos temporários..."
rm -rf build/ ConversorFinanceiro.spec

echo "✅ Executável criado em: dist/ConversorFinanceiro"
echo "🚀 Para executar: ./dist/ConversorFinanceiro"
EOF

chmod +x build_executable.sh

# Criar README
echo ""
echo "📝 Criando README..."
cat > README.md << 'EOF'
# 💼 Conversor Financeiro

Aplicativo moderno para converter extratos bancários (Asaas e Mercado Pago) de PDF para Excel com verificação automática de totais.

## 🚀 Instalação

### Método 1: Instalação Automática
```bash
chmod +x install.sh
./install.sh
```

### Método 2: Instalação Manual
```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3 python3-pip python3-tk python3-dev libssl-dev libffi-dev

# Instalar dependências Python
pip3 install -r requirements.txt
```

## 🎯 Como Usar

### Executar o Aplicativo
```bash
# Método 1: Script Python
python3 conversor_gui_moderno.py

# Método 2: Script de execução
./run_conversor.sh

# Método 3: Executável (se gerado)
./dist/ConversorFinanceiro
```

### Gerar Executável
```bash
./build_executable.sh
```

## ✨ Funcionalidades

- ✅ **Drag & Drop** de arquivos PDF
- ✅ **Conversão automática** para Excel
- ✅ **Verificação de totais** (PDF vs Excel)
- ✅ **Histórico de conversões**
- ✅ **Interface moderna** com CustomTkinter
- ✅ **Suporte a múltiplos arquivos**
- ✅ **Logs detalhados** de conversão

## 🏦 Bancos Suportados

- **Asaas**: Extratos bancários do Asaas
- **Mercado Pago**: Extratos do Mercado Pago

## 📋 Dependências

- Python 3.8+
- CustomTkinter
- TkinterDnD2
- Pandas
- OpenPyXL
- PDFMiner
- PyPDFium2
- Pillow
- NumPy

## 🐛 Solução de Problemas

### Drag & Drop não funciona
- Certifique-se de que o TkinterDnD2 está instalado
- Reinicie o aplicativo
- Use o botão "Selecionar Arquivos" como alternativa

### Erro de dependências
- Execute o script de instalação: `./install.sh`
- Verifique se todas as dependências do sistema estão instaladas

### Executável não funciona
- Certifique-se de que o executável tem permissão de execução: `chmod +x dist/ConversorFinanceiro`
- Execute no terminal para ver mensagens de erro

## 📞 Suporte

Para problemas ou sugestões, verifique os logs no terminal ou interface do aplicativo.
EOF

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Para executar: ./run_conversor.sh"
echo "   2. Para gerar executável: ./build_executable.sh"
echo "   3. Para ler documentação: cat README.md"
echo ""
echo "🎉 Conversor Financeiro está pronto para uso!"


