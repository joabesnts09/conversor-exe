#!/bin/bash

# Script de Atualização - Conversor Financeiro
# Este script atualiza o Conversor Financeiro e suas dependências

echo "🔄 Atualizando Conversor Financeiro..."
echo "===================================="

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

# Atualizar pip
echo "🔄 Atualizando pip..."
pip install --upgrade pip

# Atualizar dependências Python
echo "📦 Atualizando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade -r requirements.txt
else
    echo "❌ requirements.txt não encontrado!"
    exit 1
fi

# Verificar se há atualizações do sistema
echo "🔄 Verificando atualizações do sistema..."
sudo apt update

# Atualizar dependências do sistema
echo "📦 Atualizando dependências do sistema..."
sudo apt upgrade -y \
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

# Regenerar executável se existir
if [ -f "dist/ConversorFinanceiro" ]; then
    echo "🔨 Regenerando executável..."
    if [ -f "build_executable.sh" ]; then
        ./build_executable.sh
    else
        echo "⚠️ Script build_executable.sh não encontrado"
    fi
fi

# Verificar instalação
echo "🔍 Verificando instalação..."
if [ -f "check_dependencies.sh" ]; then
    ./check_dependencies.sh
else
    echo "⚠️ Script check_dependencies.sh não encontrado"
fi

echo ""
echo "✅ Atualização concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Para executar: python3 conversor_gui_moderno.py"
echo "   2. Para executar (script): ./run_conversor.sh"
echo "   3. Para executar (executável): ./dist/ConversorFinanceiro"
echo ""
echo "🎉 Conversor Financeiro foi atualizado com sucesso!"


