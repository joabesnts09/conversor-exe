#!/bin/bash

# Script de Desinstalação - Conversor Financeiro
# Este script remove o Conversor Financeiro e suas dependências

echo "🗑️ Desinstalando Conversor Financeiro..."
echo "====================================="

# Função para confirmar desinstalação
confirm_uninstall() {
    echo ""
    echo "⚠️ ATENÇÃO: Esta ação irá remover:"
    echo "   - Ambiente virtual (conversor_env/)"
    echo "   - Executável (dist/)"
    echo "   - Arquivos temporários"
    echo "   - Dependências Python (opcional)"
    echo ""
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        return 0
    else
        echo "❌ Desinstalação cancelada."
        exit 1
    fi
}

# Função para remover dependências Python
remove_python_deps() {
    echo ""
    read -p "Deseja remover as dependências Python? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "📦 Removendo dependências Python..."
        
        # Lista de dependências específicas do projeto
        deps=(
            "customtkinter"
            "tkinterdnd2"
            "pandas"
            "openpyxl"
            "pdfminer.six"
            "pypdfium2"
            "pillow"
            "numpy"
            "python-dateutil"
            "pytz"
            "cryptography"
            "bcrypt"
            "charset-normalizer"
            "requests"
            "urllib3"
            "certifi"
            "idna"
            "six"
            "pyinstaller"
        )
        
        for dep in "${deps[@]}"; do
            echo "   Removendo $dep..."
            pip uninstall -y "$dep" 2>/dev/null || true
        done
        
        echo "✅ Dependências Python removidas."
    else
        echo "ℹ️ Dependências Python mantidas."
    fi
}

# Função para remover dependências do sistema
remove_system_deps() {
    echo ""
    read -p "Deseja remover as dependências do sistema? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "📦 Removendo dependências do sistema..."
        
        sudo apt remove -y \
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
            libxcb1-dev 2>/dev/null || true
        
        echo "✅ Dependências do sistema removidas."
    else
        echo "ℹ️ Dependências do sistema mantidas."
    fi
}

# Confirmar desinstalação
confirm_uninstall

# Remover arquivos do projeto
echo "🗑️ Removendo arquivos do projeto..."

# Remover ambiente virtual
if [ -d "conversor_env" ]; then
    echo "   Removendo ambiente virtual..."
    rm -rf conversor_env/
fi

# Remover executável
if [ -d "dist" ]; then
    echo "   Removendo executável..."
    rm -rf dist/
fi

# Remover arquivos temporários
echo "   Removendo arquivos temporários..."
rm -f app_icon.ico
rm -f *.spec
rm -rf build/
rm -rf __pycache__/
rm -f *.pyc
rm -f *.pyo

# Remover scripts gerados
echo "   Removendo scripts gerados..."
rm -f run_conversor.sh
rm -f build_executable.sh

# Remover logs
echo "   Removendo logs..."
rm -f *.log

echo "✅ Arquivos do projeto removidos."

# Perguntar sobre dependências
remove_python_deps
remove_system_deps

# Limpar cache do pip
echo ""
echo "🧹 Limpando cache do pip..."
pip cache purge 2>/dev/null || true

# Limpar cache do apt
echo "🧹 Limpando cache do apt..."
sudo apt autoremove -y 2>/dev/null || true
sudo apt autoclean 2>/dev/null || true

echo ""
echo "✅ Desinstalação concluída!"
echo ""
echo "📋 O que foi removido:"
echo "   - Ambiente virtual (conversor_env/)"
echo "   - Executável (dist/)"
echo "   - Arquivos temporários"
echo "   - Scripts gerados"
echo "   - Cache do sistema"
echo ""
echo "ℹ️ Para reinstalar, execute: ./install.sh"
echo "🎉 Conversor Financeiro foi removido com sucesso!"


