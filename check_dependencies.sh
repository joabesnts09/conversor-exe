#!/bin/bash

# Script de Verificação de Dependências - Conversor Financeiro
# Este script verifica se todas as dependências estão instaladas corretamente

echo "🔍 Verificando dependências do Conversor Financeiro..."
echo "=================================================="

# Função para verificar comando
check_command() {
    if command -v "$1" &> /dev/null; then
        echo "✅ $1: $(command -v $1)"
        return 0
    else
        echo "❌ $1: Não encontrado"
        return 1
    fi
}

# Função para verificar módulo Python
check_python_module() {
    if python3 -c "import $1" 2>/dev/null; then
        version=$(python3 -c "import $1; print($1.__version__)" 2>/dev/null || echo "versão desconhecida")
        echo "✅ $1: $version"
        return 0
    else
        echo "❌ $1: Não encontrado"
        return 1
    fi
}

# Verificar Python
echo ""
echo "🐍 Verificando Python..."
check_command "python3"
check_command "pip3"

# Verificar versão do Python
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "   Versão: $python_version"

# Verificar se a versão é compatível (3.8+)
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "✅ Versão do Python compatível (3.8+)"
else
    echo "❌ Versão do Python incompatível (requer 3.8+)"
fi

# Verificar dependências do sistema
echo ""
echo "📦 Verificando dependências do sistema..."
system_deps=(
    "python3-tk"
    "python3-dev"
    "libssl-dev"
    "libffi-dev"
    "libxml2-dev"
    "libxslt1-dev"
    "zlib1g-dev"
    "libjpeg-dev"
    "libpng-dev"
    "libfreetype6-dev"
    "liblcms2-dev"
    "libwebp-dev"
    "libharfbuzz-dev"
    "libfribidi-dev"
    "libxcb1-dev"
)

for dep in "${system_deps[@]}"; do
    if dpkg -l | grep -q "^ii.*$dep "; then
        echo "✅ $dep: Instalado"
    else
        echo "❌ $dep: Não instalado"
    fi
done

# Verificar módulos Python
echo ""
echo "🐍 Verificando módulos Python..."
python_modules=(
    "customtkinter"
    "tkinterdnd2"
    "pandas"
    "numpy"
    "openpyxl"
    "pdfminer"
    "pypdfium2"
    "PIL"
    "dateutil"
    "pytz"
    "cryptography"
    "bcrypt"
    "requests"
    "urllib3"
    "certifi"
    "charset_normalizer"
    "idna"
    "six"
    "packaging"
)

missing_modules=0
for module in "${python_modules[@]}"; do
    if ! check_python_module "$module"; then
        ((missing_modules++))
    fi
done

# Verificar PyInstaller (opcional)
echo ""
echo "🔨 Verificando PyInstaller (opcional)..."
check_python_module "PyInstaller"

# Verificar arquivos do projeto
echo ""
echo "📁 Verificando arquivos do projeto..."
project_files=(
    "conversor_gui_moderno.py"
    "requirements.txt"
    "install.sh"
    "uninstall.sh"
    "check_dependencies.sh"
    "README.md"
)

for file in "${project_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file: Encontrado"
    else
        echo "❌ $file: Não encontrado"
    fi
done

# Verificar executável (se existir)
if [ -f "dist/ConversorFinanceiro" ]; then
    echo "✅ dist/ConversorFinanceiro: Encontrado"
    if [ -x "dist/ConversorFinanceiro" ]; then
        echo "✅ Executável tem permissão de execução"
    else
        echo "❌ Executável não tem permissão de execução"
        echo "   Execute: chmod +x dist/ConversorFinanceiro"
    fi
else
    echo "ℹ️ dist/ConversorFinanceiro: Não encontrado (execute ./build_executable.sh para criar)"
fi

# Resumo
echo ""
echo "📊 RESUMO:"
echo "=========="

if [ $missing_modules -eq 0 ]; then
    echo "✅ Todas as dependências Python estão instaladas!"
else
    echo "❌ $missing_modules módulo(s) Python não encontrado(s)"
    echo "   Execute: ./install.sh para instalar dependências"
fi

# Verificar se o app pode ser executado
echo ""
echo "🚀 Teste de execução..."
if python3 -c "
import customtkinter
import tkinterdnd2
import pandas
import openpyxl
import pdfminer
import pypdfium2
from PIL import Image
print('✅ Todas as dependências principais estão disponíveis')
" 2>/dev/null; then
    echo "✅ O aplicativo pode ser executado!"
    echo "   Execute: python3 conversor_gui_moderno.py"
else
    echo "❌ O aplicativo não pode ser executado devido a dependências faltando"
    echo "   Execute: ./install.sh para instalar dependências"
fi

echo ""
echo "🎉 Verificação concluída!"


