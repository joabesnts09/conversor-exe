# 💼 Conversor Financeiro - PDF para Excel

Aplicativo moderno para converter extratos bancários (Asaas e Mercado Pago) de PDF para Excel com verificação automática de totais.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey.svg)

## ✨ Funcionalidades

- ✅ **Drag & Drop** de arquivos PDF
- ✅ **Conversão automática** para Excel
- ✅ **Verificação de totais** (PDF vs Excel)
- ✅ **Histórico de conversões** com bordas contínuas
- ✅ **Interface moderna** com CustomTkinter
- ✅ **Suporte a múltiplos arquivos**
- ✅ **Logs detalhados** de conversão
- ✅ **Ícone personalizado** na barra de tarefas
- ✅ **Executável standalone** (não precisa do Python)

## 🏦 Bancos Suportados

- **Asaas**: Extratos bancários do Asaas
- **Mercado Pago**: Extratos do Mercado Pago

## 🖥️ Requisitos do Sistema

### Linux
- **Ubuntu 20.04+** ou similar
- **Python 3.8+**
- **4GB RAM** mínimo
- **100MB** espaço em disco

### Windows
- **Windows 10/11** (64-bit)
- **Python 3.8+** (recomendado: Python 3.11+)
- **4GB RAM** mínimo
- **100MB** espaço em disco

## 🚀 Instalação Rápida

### Linux

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/conversor-financeiro.git
cd conversor-financeiro

# 2. Instalar dependências
./install.sh

# 3. Executar
python3 conversor_gui_moderno.py

# 4. Gerar executável (opcional)
./build_executable.sh
```

### Windows

```cmd
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/conversor-financeiro.git
cd conversor-financeiro

# 2. Instalar dependências
install_windows.bat

# 3. Executar
python conversor_gui_moderno.py

# 4. Gerar executável (opcional)
powershell -ExecutionPolicy Bypass -File build_windows.ps1
```

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

## 🎯 Como Usar

1. **Inicie o aplicativo**
2. **Arraste arquivos PDF** para a área de drag & drop
3. **Aguarde a conversão** automática
4. **Verifique os totais** no histórico
5. **Baixe os arquivos Excel** gerados

## 📁 Estrutura do Projeto

```
conversor-financeiro/
├── conversor_gui_moderno.py    # Aplicativo principal
├── requirements.txt            # Dependências Python
├── app_icon.ico               # Ícone do aplicativo
├── README.md                  # Este arquivo
├── README_WINDOWS.md          # Documentação Windows
├── README_MODERNO.md          # Documentação técnica
├── CHANGELOG.md               # Histórico de mudanças
├── .gitignore                 # Arquivos ignorados pelo Git
│
├── Scripts Linux/
│   ├── install.sh             # Instalação automática
│   ├── uninstall.sh           # Desinstalação
│   ├── update.sh              # Atualização
│   ├── build_executable.sh    # Gerar executável
│   └── check_dependencies.sh  # Verificar dependências
│
├── Scripts Windows/
│   ├── install_windows.bat    # Instalação automática
│   ├── build_windows.bat      # Gerar executável (CMD)
│   └── build_windows.ps1      # Gerar executável (PowerShell)
│
└── dist/                      # Executáveis gerados
    ├── ConversorFinanceiro    # Linux
    └── ConversorFinanceiro.exe # Windows
```

## 🔧 Scripts Disponíveis

### Linux
- `./install.sh` - Instalação automática
- `./uninstall.sh` - Desinstalação
- `./update.sh` - Atualização de dependências
- `./build_executable.sh` - Gerar executável
- `./check_dependencies.sh` - Verificar dependências

### Windows
- `install_windows.bat` - Instalação automática
- `build_windows.bat` - Gerar executável (CMD)
- `build_windows.ps1` - Gerar executável (PowerShell)

## 🎨 Interface

- **Título**: "💼 Conversor Financeiro - PDF para Excel"
- **Ícone personalizado** na barra de tarefas
- **Tema azul moderno** com CustomTkinter
- **Área de drag & drop** com bordas e animações
- **Barra de progresso** animada
- **Histórico** com bordas contínuas e separadores
- **Logs em tempo real** no terminal

## 🐛 Solução de Problemas

### Python não encontrado
**Solução**: Instale Python 3.8+ e certifique-se de que está no PATH

### Dependências não instaladas
**Solução**: Execute o script de instalação correspondente ao seu sistema

### Drag & Drop não funciona
**Solução**: 
- Certifique-se de que o TkinterDnD2 está instalado
- Reinicie o aplicativo
- Use o botão "Selecionar Arquivos" como alternativa

### Executável não funciona
**Solução**:
- Certifique-se de que o antivírus não bloqueou o arquivo
- Execute como administrador se necessário
- Verifique se todas as dependências estão instaladas

## 📊 Exemplo de Uso

1. **Arraste** um extrato PDF do Asaas ou Mercado Pago
2. **Aguarde** a conversão automática
3. **Verifique** se os totais correspondem
4. **Baixe** o arquivo Excel gerado
5. **Consulte** o histórico para ver todas as conversões

## 🔄 Atualizações

Para atualizar o aplicativo:

### Linux
```bash
./update.sh
```

### Windows
```cmd
pip install --upgrade -r requirements.txt
```

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique os logs no terminal
2. Execute o aplicativo para ver mensagens de erro
3. Certifique-se de que todas as dependências estão instaladas
4. Abra uma issue no GitHub

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🎉 Agradecimentos

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Interface moderna
- [TkinterDnD2](https://github.com/pmgagne/tkinterdnd2) - Drag & Drop
- [Pandas](https://pandas.pydata.org/) - Manipulação de dados
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel
- [PDFMiner](https://pdfminersix.readthedocs.io/) - Extração de PDF

---

**🚀 O Conversor Financeiro está pronto para uso!**