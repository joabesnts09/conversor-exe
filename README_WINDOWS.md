# 💼 Conversor Financeiro - Windows

Aplicativo moderno para converter extratos bancários (Asaas e Mercado Pago) de PDF para Excel com verificação automática de totais.

## 🖥️ Requisitos do Sistema

- **Windows 10/11** (64-bit)
- **Python 3.8+** (recomendado: Python 3.11+)
- **4GB RAM** mínimo
- **100MB** espaço em disco

## 🚀 Instalação Rápida

### Método 1: Instalação Automática
```cmd
# Execute no Prompt de Comando (CMD) ou PowerShell
install_windows.bat
```

### Método 2: Instalação Manual

#### 1. Instalar Python
- Acesse: https://www.python.org/downloads/
- Baixe Python 3.8 ou superior
- **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"

#### 2. Instalar Dependências
```cmd
# No Prompt de Comando
pip install -r requirements.txt
```

## 🎯 Como Usar

### Executar o Aplicativo

#### Opção 1: Script Python
```cmd
python conversor_gui_moderno.py
```

#### Opção 2: Script de Execução
```cmd
run_conversor.bat
```

#### Opção 3: Executável (se gerado)
```cmd
dist\ConversorFinanceiro.exe
```

### Gerar Executável

#### Método 1: Script Automático
```cmd
build_executable.bat
```

#### Método 2: PowerShell (Recomendado)
```powershell
powershell -ExecutionPolicy Bypass -File build_windows.ps1
```

#### Método 3: Manual
```cmd
pyinstaller --onefile --windowed --icon=app_icon.ico --name="ConversorFinanceiro" conversor_gui_moderno.py
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

### Python não encontrado
```
❌ Python não encontrado!
```
**Solução**: Instale Python de https://www.python.org/downloads/ e marque "Add Python to PATH"

### Erro de dependências
```
❌ ModuleNotFoundError: No module named 'customtkinter'
```
**Solução**: Execute `pip install -r requirements.txt`

### Drag & Drop não funciona
- Certifique-se de que o TkinterDnD2 está instalado
- Reinicie o aplicativo
- Use o botão "Selecionar Arquivos" como alternativa

### Executável não funciona
- Certifique-se de que o Windows Defender não bloqueou o arquivo
- Execute como administrador se necessário
- Verifique se todas as dependências estão instaladas

### Erro de permissão no PowerShell
```
ExecutionPolicy: Restricted
```
**Solução**: Execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 📁 Estrutura de Arquivos

```
conversor/
├── conversor_gui_moderno.py    # Aplicativo principal
├── requirements.txt            # Dependências
├── install_windows.bat         # Instalação automática
├── build_windows.ps1           # Build PowerShell
├── build_windows.bat           # Build CMD
├── run_conversor.bat           # Script de execução
├── app_icon.ico               # Ícone do aplicativo
├── dist/                      # Executável gerado
│   └── ConversorFinanceiro.exe
└── README_WINDOWS.md          # Esta documentação
```

## 🎨 Interface

- **Título**: "💼 Conversor Financeiro - PDF para Excel"
- **Ícone personalizado** na barra de tarefas
- **Tema azul moderno**
- **Área de drag & drop** com bordas
- **Barra de progresso** animada
- **Histórico** com bordas contínuas

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique os logs no terminal
2. Execute `python conversor_gui_moderno.py` para ver mensagens de erro
3. Certifique-se de que todas as dependências estão instaladas

## 🔄 Atualizações

Para atualizar o aplicativo:
```cmd
# Atualizar dependências
pip install --upgrade -r requirements.txt

# Regenerar executável
build_executable.bat
```

## 🎉 Pronto!

O Conversor Financeiro está pronto para uso no Windows! 🚀


