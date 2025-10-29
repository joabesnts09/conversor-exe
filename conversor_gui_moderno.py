#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica Moderna do Conversor Financeiro
Interface moderna e intuitiva com CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
import time
import queue
import multiprocessing
from datetime import datetime
from conversor_financeiro import ConversorFinanceiro

# Importar tkinterdnd2 para drag & drop real
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️ tkinterdnd2 não disponível. Drag & drop será simulado.")

# Função para executar conversão em processo separado
def run_conversion_process(pdf_path, output_path, result_queue):
    """Executa conversão em processo separado para evitar bloqueio"""
    try:
        from conversor_financeiro import ConversorFinanceiro
        converter = ConversorFinanceiro()
        result = converter.convert_with_verification(pdf_path, output_path)
        result_queue.put(result)
    except Exception as e:
        result_queue.put({'success': False, 'error': str(e)})

# Proteção para multiprocessing
if __name__ == '__main__':
    multiprocessing.freeze_support()

# Configurar tema do CustomTkinter
ctk.set_appearance_mode("light")  # "light" ou "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class ConversorGUIModerno:
    def __init__(self):
        # Criar janela principal com suporte a drag & drop
        if DRAG_DROP_AVAILABLE:
            # IMPORTANTE: TkinterDnD deve ser inicializado ANTES de qualquer widget
            self.root = TkinterDnD.Tk()
            # NÃO forçar inicialização manual - deixar o tkinterdnd2 fazer isso
        else:
            self.root = ctk.CTk()
        
        # Configurar título e ícone IMEDIATAMENTE após criar a janela
        self.root.title("💼 Conversor Financeiro - PDF para Excel")
        self.root.geometry("900x800")
        self.root.minsize(800, 700)
        
        # Configurar ícone IMEDIATAMENTE (antes do drag & drop)
        self.setup_icon_immediately()
        
        # Configurar drag & drop com múltiplas tentativas
        self.setup_robust_drag_drop()
    
    def setup_icon_immediately(self):
        """Configura ícone imediatamente após criar a janela"""
        try:
            # Método mais direto para tkinterdnd2
            # Criar um ícone simples
            icon_image = tk.PhotoImage(width=16, height=16)
            
            # Preencher com cor azul
            icon_image.put("#3B82F6", (0, 0, 16, 16))
            
            # Adicionar um símbolo branco (ponto central)
            icon_image.put("#FFFFFF", (6, 6, 10, 10))
            
            # Tentar definir o ícone usando diferentes métodos
            try:
                # Método 1: iconphoto
                self.root.iconphoto(True, icon_image)
                print("✅ Ícone configurado com iconphoto")
            except:
                try:
                    # Método 2: iconbitmap (se disponível)
                    self.root.iconbitmap(icon_image)
                    print("✅ Ícone configurado com iconbitmap")
                except:
                    print("⚠️ Não foi possível configurar ícone")
            
            # Manter referência
            self.app_icon = icon_image
            
        except Exception as e:
            print(f"❌ Erro ao configurar ícone imediatamente: {e}")
        
        # Variáveis
        self.selected_files = []
        self.conversion_history = []
        self.is_converting = False
        self.loading_active = False
        self.conversion_thread = None
        self.conversion_queue = queue.Queue()
        
        # Criar interface
        self.create_widgets()
        
        # Forçar inicialização completa da interface
        self.root.update_idletasks()
        self.root.update()
        
        # Centralizar janela
        self.center_window()
        
        # Iniciar polling da queue
        self.poll_queue()
        
        # Configurar fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_robust_drag_drop(self):
        """Configura drag & drop de forma mais robusta com múltiplas tentativas"""
        if not DRAG_DROP_AVAILABLE:
            print("⚠️ Drag & drop não disponível - usando apenas clique")
            return
        
        # Tentar configurar drag & drop imediatamente
        self._attempt_drag_drop_setup()
        
        # Agendar tentativas adicionais para garantir que funcione
        self.root.after(100, self._retry_drag_drop_setup)
        self.root.after(500, self._retry_drag_drop_setup)
        self.root.after(1000, self._final_drag_drop_setup)
    
    def _attempt_drag_drop_setup(self):
        """Tenta configurar drag & drop"""
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_root_drop_files)
            print("✅ Drag & drop configurado com sucesso")
            return True
        except Exception as e:
            print(f"⚠️ Tentativa de drag & drop falhou: {e}")
            return False
    
    def _retry_drag_drop_setup(self):
        """Tenta reconfigurar drag & drop"""
        try:
            # Tentar reconfigurar
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_root_drop_files)
            print("✅ Drag & drop reconfigurado com sucesso")
        except Exception as e:
            print(f"⚠️ Reconfiguração de drag & drop falhou: {e}")
    
    def _final_drag_drop_setup(self):
        """Configuração final de drag & drop"""
        try:
            # Última tentativa
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_root_drop_files)
            print("✅ Drag & drop configurado definitivamente")
        except Exception as e:
            print(f"❌ Falha final no drag & drop: {e}")
            print("⚠️ Usando sistema de clique apenas")
    
    def poll_queue(self):
        """Processa mensagens da queue de conversão"""
        try:
            while True:
                message = self.conversion_queue.get_nowait()
                if message['type'] == 'status':
                    self.status_label.configure(text=message['text'])
                elif message['type'] == 'result':
                    if message['success']:
                        self.add_to_history(message['result'], message['filename'])
                    self.log_message(message['log'])
                elif message['type'] == 'finish':
                    self.finish_conversion()
                    break
        except queue.Empty:
            pass
        
        # Agendar próxima verificação
        self.root.after(100, self.poll_queue)
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_smooth_scroll(self):
        """Configura scroll suave para o frame principal"""
        # Bind eventos de scroll do mouse
        self.main_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.main_frame.bind("<Button-4>", self.on_mousewheel)  # Linux scroll up
        self.main_frame.bind("<Button-5>", self.on_mousewheel)  # Linux scroll down
        
        # Bind para todos os widgets filhos
        self.bind_mousewheel_to_children(self.main_frame)
    
    def bind_mousewheel_to_children(self, widget):
        """Aplica scroll do mouse para todos os widgets filhos"""
        widget.bind("<MouseWheel>", self.on_mousewheel)
        widget.bind("<Button-4>", self.on_mousewheel)
        widget.bind("<Button-5>", self.on_mousewheel)
        
        for child in widget.winfo_children():
            self.bind_mousewheel_to_children(child)
    
    def on_mousewheel(self, event):
        """Manipula o scroll do mouse"""
        # Scroll suave
        if event.delta:
            # Windows/Mac
            delta = -1 * (event.delta / 120)
        else:
            # Linux
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                delta = 0
        
        # Aplicar scroll
        self.main_frame._parent_canvas.yview_scroll(int(delta), "units")
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal com scroll (usando CTkScrollableFrame como no log)
        self.main_frame = ctk.CTkScrollableFrame(
            self.root, 
            fg_color="transparent",
            scrollbar_button_color=("#4B5563", "#374151"),
            scrollbar_button_hover_color=("#6B7280", "#4B5563"),
            scrollbar_fg_color=("#E5E7EB", "#374151")
        )
        self.main_frame.pack(fill="both", expand=True, padx=(20, 5), pady=20)
        
        # Título principal
        self.create_header()
        
        # Seção de seleção de arquivos
        self.create_file_section()
        
        # Seção de progresso com animação
        self.create_progress_section()
        
        # Seção de histórico
        self.create_history_section()
        
        # Seção de destino de salvamento
        self.create_output_section()
        
        # Configurar scroll suave após criar todos os widgets
        self.setup_smooth_scroll()
    
    def create_header(self):
        """Cria o cabeçalho da aplicação"""
        # Frame do cabeçalho
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="💼 Conversor Financeiro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#14375e")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Converte extratos bancários (Asaas e Mercado Pago) para Excel com verificação automática",
            font=ctk.CTkFont(size=14),
            text_color=("gray10", "gray90"),
            wraplength=800
        )
        subtitle_label.pack()
    
    def create_file_section(self):
        """Cria a seção de seleção de arquivos"""
        # Frame da seção
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        # Título da seção
        section_title = ctk.CTkLabel(
            file_frame,
            text="📁 Seleção de Arquivos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))
        
        # Área de drag & drop
        self.create_drag_drop_area(file_frame)
        
        # Label com arquivos selecionados
        self.files_label = ctk.CTkLabel(
            file_frame,
            text="Nenhum arquivo selecionado",
            font=ctk.CTkFont(size=12),
            text_color=("gray30", "gray70")
        )
        self.files_label.pack(pady=(10, 15))
        
        # Informações sobre bancos suportados
        info_label = ctk.CTkLabel(
            file_frame,
            text="💡 Suporta: Asaas e Mercado Pago (detecção automática)",
            font=ctk.CTkFont(size=12),
            text_color=("gray30", "gray70")
        )
        info_label.pack(pady=(0, 20))
        
        # Botão para converter (centralizado e maior)
        self.convert_btn = ctk.CTkButton(
            file_frame,
            text="🔄 Converter",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200,
            command=self.start_conversion,
            state="disabled",
            fg_color=("#10B981", "#059669"),
            hover_color=("#059669", "#047857"),
            text_color=("#FFFFFF", "#F0F0F0"),
            cursor="hand2"
        )
        self.convert_btn.pack(pady=(0, 20))
    
    def create_drag_drop_area(self, parent):
        """Cria área de drag & drop simples e confiável"""
        # Frame principal para drag & drop
        self.drag_drop_frame = ctk.CTkFrame(
            parent,
            height=200,
            border_width=2,
            border_color=("#3B82F6", "#1E40AF"),
            fg_color=("#F8FAFC", "#1F2937"),
            corner_radius=12
        )
        self.drag_drop_frame.pack(fill="x", padx=20, pady=10)
        self.drag_drop_frame.pack_propagate(False)
        
        # Ícone
        self.drag_icon = ctk.CTkLabel(
            self.drag_drop_frame,
            text="📁",
            font=ctk.CTkFont(size=48),
            text_color=("#3B82F6", "#60A5FA")
        )
        self.drag_icon.pack(pady=(20, 10))
        
        # Texto principal
        self.drag_text = ctk.CTkLabel(
            self.drag_drop_frame,
            text="📁 Arraste arquivos PDF aqui ou clique para selecionar",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1F2937", "#F9FAFB")
        )
        self.drag_text.pack(pady=(0, 5))
        
        # Texto secundário
        self.drag_subtext = ctk.CTkLabel(
            self.drag_drop_frame,
            text="✨ Suporta múltiplos arquivos simultaneamente",
            font=ctk.CTkFont(size=14),
            text_color=("#6B7280", "#9CA3AF")
        )
        self.drag_subtext.pack()
        
        # Configurar eventos diretamente no frame principal
        self.drag_drop_frame.bind("<Button-1>", self.on_drag_area_click)
        self.drag_icon.bind("<Button-1>", self.on_drag_area_click)
        self.drag_text.bind("<Button-1>", self.on_drag_area_click)
        self.drag_subtext.bind("<Button-1>", self.on_drag_area_click)
        
        # Configurar cursor
        self.drag_drop_frame.configure(cursor="hand2")
        self.drag_icon.configure(cursor="hand2")
        self.drag_text.configure(cursor="hand2")
        self.drag_subtext.configure(cursor="hand2")
        
        # Configurar drag & drop também na área específica (fallback)
        self.setup_drag_drop_area_events()
        
        # Estado inicial
        self.drag_drop_state = "empty"
    
    def setup_drag_drop_area_events(self):
        """Configura drag & drop também na área específica como fallback"""
        if not DRAG_DROP_AVAILABLE:
            return
        
        try:
            # Configurar drag & drop na área específica também
            self.drag_drop_frame.drop_target_register(DND_FILES)
            self.drag_drop_frame.dnd_bind('<<Drop>>', self.on_drop_files)
            self.drag_drop_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.drag_drop_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            print("✅ Drag & drop configurado na área específica")
        except Exception as e:
            print(f"⚠️ Erro ao configurar drag & drop na área específica: {e}")
    
    def setup_drag_drop_events(self):
        """Configura os eventos de drag & drop e clique"""
        # Eventos de hover para feedback visual
        self.drag_drop_frame.bind("<Enter>", self.on_mouse_enter)
        self.drag_drop_frame.bind("<Leave>", self.on_mouse_leave)
        self.drag_icon.bind("<Enter>", self.on_mouse_enter)
        self.drag_icon.bind("<Leave>", self.on_mouse_leave)
        self.drag_text.bind("<Enter>", self.on_mouse_enter)
        self.drag_text.bind("<Leave>", self.on_mouse_leave)
        self.drag_subtext.bind("<Enter>", self.on_mouse_enter)
        self.drag_subtext.bind("<Leave>", self.on_mouse_leave)
    
    
    def _ensure_interface_ready(self):
        """Garante que a interface esteja completamente pronta"""
        try:
            # Forçar atualização da interface
            self.root.update_idletasks()
            self.root.update()
            
            print("✅ Interface completamente inicializada")
            
        except Exception as e:
            print(f"❌ Erro ao garantir interface pronta: {e}")
    
    
    
    def on_drag_area_click(self, event):
        """Abre o seletor de arquivos quando clica na área"""
        self.select_files()
    
    def on_root_drop_files(self, event):
        """Manipula arquivos arrastados para a janela principal (mais confiável)"""
        try:
            print(f"🎯 Evento de drop recebido: {event}")
            print(f"🎯 Dados do evento: {event.data}")
            
            # Obter lista de arquivos
            files = self.root.tk.splitlist(event.data)
            print(f"🎯 Arquivos recebidos: {files}")
            
            # Filtrar apenas arquivos PDF
            pdf_files = []
            for file_path in files:
                if file_path.lower().endswith('.pdf') and os.path.isfile(file_path):
                    pdf_files.append(file_path)
                    print(f"✅ Arquivo PDF válido: {file_path}")
                else:
                    print(f"❌ Arquivo inválido: {file_path}")
            
            print(f"🎯 Total de arquivos PDF válidos: {len(pdf_files)}")
            
            if pdf_files:
                self.selected_files = pdf_files
                self.files_label.configure(text=f"{len(pdf_files)} arquivo(s) selecionado(s)")
                self.convert_btn.configure(state="normal", text_color=("#FFFFFF", "#F0F0F0"))
                self.drag_drop_state = "files_selected"
                self.update_drag_drop_appearance()
                self.log_message(f"📁 {len(pdf_files)} arquivo(s) adicionado(s) via drag & drop")
                print(f"✅ {len(pdf_files)} arquivo(s) processado(s) com sucesso")
            else:
                self.log_message("❌ Nenhum arquivo PDF válido foi arrastado")
                print("❌ Nenhum arquivo PDF encontrado nos arquivos arrastados")
        except Exception as e:
            error_msg = f"❌ Erro ao processar arquivos arrastados: {str(e)}"
            self.log_message(error_msg)
            print(f"❌ Erro detalhado: {e}")
            import traceback
            traceback.print_exc()
    
    def on_drop_files(self, event):
        """Manipula arquivos arrastados para a área específica (fallback)"""
        # Redirecionar para a função principal
        self.on_root_drop_files(event)
    
    def on_drag_enter(self, event):
        """Quando arquivos são arrastados sobre a área"""
        self.drag_drop_state = "hover"
        self.update_drag_drop_appearance()
    
    def on_drag_leave(self, event):
        """Quando arquivos saem da área de drag"""
        if self.selected_files:
            self.drag_drop_state = "files_selected"
        else:
            self.drag_drop_state = "empty"
        self.update_drag_drop_appearance()
    
    def on_mouse_enter(self, event):
        """Quando o mouse entra na área"""
        if self.drag_drop_state == "empty":
            self.drag_drop_state = "hover"
            self.update_drag_drop_appearance()
    
    
    def on_mouse_leave(self, event):
        """Quando o mouse sai da área"""
        if self.drag_drop_state == "hover":
            if self.selected_files:
                self.drag_drop_state = "files_selected"
            else:
                self.drag_drop_state = "empty"
            self.update_drag_drop_appearance()
    
    def update_drag_drop_appearance(self):
        """Atualiza a aparência da área de drag & drop"""
        if self.drag_drop_state == "empty":
            # Estado vazio
            self.drag_drop_frame.configure(
                fg_color=("#F8FAFC", "#1F2937"),
                border_color=("#3B82F6", "#1E40AF"),
                border_width=2
            )
            self.drag_icon.configure(text="📁")
            self.drag_text.configure(
                text="📁 Arraste arquivos PDF aqui ou clique para selecionar",
                text_color=("#1F2937", "#F9FAFB")
            )
            self.drag_subtext.configure(
                text="✨ Suporta múltiplos arquivos simultaneamente",
                text_color=("#6B7280", "#9CA3AF")
            )
            
        elif self.drag_drop_state == "hover":
            # Estado hover
            self.drag_drop_frame.configure(
                fg_color=("#EBF8FF", "#1E3A8A"),
                border_color=("#3B82F6", "#1E40AF"),
                border_width=3
            )
            self.drag_icon.configure(text="📂")
            self.drag_text.configure(
                text="📂 Solte os arquivos aqui!",
                text_color=("#1E40AF", "#3B82F6")
            )
            self.drag_subtext.configure(
                text="Arquivos PDF serão processados automaticamente",
                text_color=("#1E40AF", "#3B82F6")
            )
            
        elif self.drag_drop_state == "files_selected":
            # Estado com arquivos selecionados
            self.drag_drop_frame.configure(
                fg_color=("#F0FDF4", "#064E3B"),
                border_color=("#10B981", "#059669"),
                border_width=2
            )
            self.drag_icon.configure(text="✅")
            self.drag_text.configure(
                text=f"{len(self.selected_files)} arquivo(s) selecionado(s)",
                text_color=("#059669", "#10B981")
            )
            self.drag_subtext.configure(
                text="Clique para selecionar outros arquivos",
                text_color=("#059669", "#10B981")
            )
    
    def create_progress_section(self):
        """Cria a seção de status"""
        # Frame da seção
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        # Título da seção
        section_title = ctk.CTkLabel(
            progress_frame,
            text="📊 Status",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))
        
        # Frame do status
        progress_content_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Label de status principal
        self.status_label = ctk.CTkLabel(
            progress_content_frame,
            text="Pronto para converter",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#10B981", "#059669")
        )
        self.status_label.pack()
        
        # Barra de progresso (inicialmente oculta)
        self.progress_bar = ctk.CTkProgressBar(
            progress_content_frame,
            width=200,
            height=20,
            progress_color=("#3B82F6", "#1E40AF"),
            fg_color=("#E5E7EB", "#374151")
        )
        # Não fazer pack inicialmente - será mostrada apenas quando necessário
        
        # Label de loading (inicialmente oculto)
        self.loading_label = ctk.CTkLabel(
            progress_content_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("#3B82F6", "#1E40AF")
        )
        self.loading_label.pack(pady=(5, 0))
    
    def create_history_section(self):
        """Cria a seção de histórico"""
        # Frame da seção
        history_frame = ctk.CTkFrame(self.main_frame)
        history_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título da seção
        section_title = ctk.CTkLabel(
            history_frame,
            text="📋 Histórico de Conversões",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))
        
        # Frame dos botões
        buttons_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Botão limpar histórico
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpar Histórico",
            font=ctk.CTkFont(size=12),
            height=35,
            command=self.clear_history,
            fg_color=("#EF4444", "#DC2626"),
            hover_color=("#DC2626", "#B91C1C"),
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=(0, 10))
        
        # Botão exportar histórico
        export_btn = ctk.CTkButton(
            buttons_frame,
            text="📤 Exportar Histórico",
            font=ctk.CTkFont(size=12),
            height=35,
            command=self.export_history,
            fg_color=("#8B5CF6", "#7C3AED"),
            hover_color=("#7C3AED", "#6D28D9"),
            cursor="hand2"
        )
        export_btn.pack(side="left")
        
        # Frame da tabela
        table_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Criar novo histórico com Canvas
        self.create_new_history_table(table_frame)
    
    def create_new_history_table(self, parent):
        """Cria nova tabela de histórico simples com bordas contínuas"""
        # Frame principal do histórico
        history_container = ctk.CTkFrame(parent)
        history_container.pack(fill="both", expand=True)
        
        # Frame para o conteúdo do histórico
        self.history_content_frame = ctk.CTkFrame(history_container, fg_color="transparent")
        self.history_content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar cabeçalho fixo
        self.create_fixed_header()
        
        # Frame para os itens do histórico
        self.history_items_frame = ctk.CTkFrame(self.history_content_frame, fg_color="transparent")
        self.history_items_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Lista para armazenar itens do histórico
        self.history_items = []
        
        # Inicializar histórico vazio
        self.update_history_display()
    
    def create_fixed_header(self):
        """Cria cabeçalho fixo da tabela"""
        header_frame = ctk.CTkFrame(self.history_content_frame, fg_color="#F3F4F6")
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Configurar grid do cabeçalho (exatamente igual aos itens)
        header_frame.grid_columnconfigure(0, weight=1, minsize=120)  # Data (aumentada)
        header_frame.grid_columnconfigure(1, weight=2, minsize=200)  # Arquivo
        header_frame.grid_columnconfigure(2, weight=1, minsize=80)  # Banco
        header_frame.grid_columnconfigure(3, weight=1, minsize=80)  # Transações
        header_frame.grid_columnconfigure(4, weight=1, minsize=100)  # Total PDF
        header_frame.grid_columnconfigure(5, weight=1, minsize=100)  # Total Excel
        header_frame.grid_columnconfigure(6, weight=1, minsize=80)  # Status
        
        headers = ["Data", "Arquivo", "Banco", "Transações", "Total PDF", "Total Excel", "Status"]
        
        # Configurar alinhamento específico para cada coluna
        alignments = ["center", "w", "center", "center", "center", "center", "center"]
        sticky_configs = ["ew", "ew", "ew", "ew", "ew", "ew", "ew"]
        
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#374151",
                anchor=alignments[i]
            )
            label.grid(row=0, column=i, sticky=sticky_configs[i], padx=5, pady=10)
    
    def create_history_item(self, data):
        """Cria um item do histórico com bordas contínuas"""
        # Frame do item
        item_frame = ctk.CTkFrame(self.history_items_frame, fg_color="#FFFFFF")
        item_frame.pack(fill="x", pady=2)
        
        # Configurar grid do item (exatamente igual ao cabeçalho)
        item_frame.grid_columnconfigure(0, weight=1, minsize=120)  # Data (aumentada)
        item_frame.grid_columnconfigure(1, weight=2, minsize=200)  # Arquivo
        item_frame.grid_columnconfigure(2, weight=1, minsize=80)  # Banco
        item_frame.grid_columnconfigure(3, weight=1, minsize=80)  # Transações
        item_frame.grid_columnconfigure(4, weight=1, minsize=100)  # Total PDF
        item_frame.grid_columnconfigure(5, weight=1, minsize=100)  # Total Excel
        item_frame.grid_columnconfigure(6, weight=1, minsize=80)  # Status
        
        # Adicionar dados
        labels = [
            data['timestamp'],
            data['filename'],
            data['bank_type'].title(),
            str(data['transactions_count']),
            f"R$ {data['pdf_total']:,.2f}",
            f"R$ {data['excel_total']:,.2f}",
            data['status']
        ]
        
        # Configurar alinhamento específico para cada coluna de dados (igual ao cabeçalho)
        data_alignments = ["center", "w", "center", "center", "center", "center", "center"]
        data_sticky_configs = ["ew", "ew", "ew", "ew", "ew", "ew", "ew"]
        
        for i, text in enumerate(labels):
            label = ctk.CTkLabel(
                item_frame,
                text=text,
                font=ctk.CTkFont(size=11),
                text_color="#374151",
                anchor=data_alignments[i]
            )
            label.grid(row=0, column=i, sticky=data_sticky_configs[i], padx=5, pady=8)
        
        # Adicionar linha separadora usando grid
        separator = ctk.CTkFrame(item_frame, fg_color="#E5E7EB", height=1)
        separator.grid(row=1, column=0, columnspan=7, sticky="ew", pady=(0, 0))
        
        return item_frame
    
    def update_history_display(self):
        """Atualiza a exibição do histórico"""
        # Limpar itens existentes
        for item in self.history_items:
            item.destroy()
        self.history_items.clear()
        
        # Criar itens do histórico
        for data in self.conversion_history:
            item = self.create_history_item(data)
            self.history_items.append(item)
    
    def create_output_section(self):
        """Cria a seção de destino de salvamento"""
        # Frame da seção
        output_frame = ctk.CTkFrame(self.main_frame)
        output_frame.pack(fill="x", pady=(0, 20))
        
        # Título da seção
        section_title = ctk.CTkLabel(
            output_frame,
            text="💾 Destino de Salvamento",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))
        
        # Frame dos controles
        controls_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Label do diretório
        dir_label = ctk.CTkLabel(
            controls_frame,
            text="📁 Pasta de destino:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        dir_label.pack(anchor="w", pady=(0, 10))
        
        # Frame para o campo de diretório e botão
        dir_controls_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        dir_controls_frame.pack(fill="x")
        
        # Campo de diretório atual
        self.output_dir_var = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.output_dir_entry = ctk.CTkEntry(
            dir_controls_frame,
            textvariable=self.output_dir_var,
            font=ctk.CTkFont(size=12),
            height=35,
            placeholder_text="Selecione a pasta onde salvar os arquivos..."
        )
        self.output_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botão para navegar
        self.browse_output_btn = ctk.CTkButton(
            dir_controls_frame,
            text="📁",
            font=ctk.CTkFont(size=16),
            width=50,
            height=35,
            command=self.browse_output_directory,
            fg_color=("#3B82F6", "#1E40AF"),
            hover_color=("#2563EB", "#1E3A8A"),
            cursor="hand2"
        )
        self.browse_output_btn.pack(side="right")
        
        # Informações sobre o destino
        info_label = ctk.CTkLabel(
            output_frame,
            text="💡 Os arquivos Excel serão salvos na pasta selecionada",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray80")
        )
        info_label.pack(pady=(0, 20))
    
    def browse_output_directory(self):
        """Permite navegar para escolher o diretório de destino"""
        directory = filedialog.askdirectory(
            title="Selecionar pasta de destino",
            initialdir=self.output_dir_var.get()
        )
        
        if directory:
            self.output_dir_var.set(directory)
            self.log_message(f"📁 Pasta de destino alterada para: {os.path.basename(directory)}")
    
    def select_files(self):
        """Seleciona arquivos PDF para conversão"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            self.files_label.configure(text=f"{len(files)} arquivo(s) selecionado(s)")
            self.convert_btn.configure(state="normal", text_color=("#FFFFFF", "#F0F0F0"))
            self.drag_drop_state = "files_selected"
            self.update_drag_drop_appearance()
            self.log_message(f"📁 {len(files)} arquivo(s) selecionado(s)")
        else:
            self.selected_files = []
            self.files_label.configure(text="Nenhum arquivo selecionado")
            self.convert_btn.configure(state="disabled", text_color=("#FFFFFF", "#F0F0F0"))
            self.drag_drop_state = "empty"
            self.update_drag_drop_appearance()
    
    def start_conversion(self):
        """Inicia o processo de conversão em thread separada"""
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo PDF.")
            return
        
        if self.is_converting:
            return
        
        # Configurar estado de conversão
        self.is_converting = True
        self.convert_btn.configure(state="disabled", text="🔄 Convertendo...", text_color=("#FFFFFF", "#F0F0F0"))
        self.status_label.configure(text="🔄 Convertendo...")
        
        # Iniciar loading
        self.start_loading()
        
        # Iniciar conversão em thread separada
        self.conversion_thread = threading.Thread(target=self.convert_files, daemon=True)
        self.conversion_thread.start()
    
    def start_loading(self):
        """Inicia a animação de loading"""
        self.loading_active = True
        # Mostrar a barra de progresso
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.set(0)
        self.animate_progress()
    
    def animate_progress(self):
        """Anima a barra de progresso"""
        if not self.loading_active:
            return
        
        # Obter valor atual da barra
        current_value = self.progress_bar.get()
        
        # Incrementar progresso
        if current_value < 0.9:  # Não chegar a 100% até a conversão terminar
            new_value = current_value + 0.02
            self.progress_bar.set(new_value)
        else:
            # Resetar para 0.1 quando chegar perto do fim
            self.progress_bar.set(0.1)
        
        # Atualizar texto
        self.loading_label.configure(text="Convertendo...")
        
        # Agendar próxima animação
        self.root.after(100, self.animate_progress)
    
    def stop_loading(self):
        """Para a animação de loading"""
        self.loading_active = False
        self.loading_label.configure(text="")
        # Ocultar a barra de progresso
        self.progress_bar.pack_forget()
        self.progress_bar.set(0)
    
    def convert_files(self):
        """Converte os arquivos selecionados usando multiprocessing"""
        try:
            for pdf_path in self.selected_files:
                if not self.is_converting:  # Verificar se ainda está convertendo
                    break
                    
                try:
                    # Enviar status via queue
                    self.conversion_queue.put({
                        'type': 'status',
                        'text': f"🔄 Convertendo: {os.path.basename(pdf_path)}"
                    })
                    
                    # Gerar nome do arquivo de saída
                    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                    output_dir = self.output_dir_var.get()
                    
                    # Garantir que o diretório de destino existe
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir, exist_ok=True)
                    
                    output_path = os.path.join(output_dir, f"{base_name}_convertido.xlsx")
                    
                    # Converter arquivo
                    self.log_message(f"🔄 Convertendo: {os.path.basename(pdf_path)}")
                    
                    # Executar conversão em processo separado
                    result = self.run_conversion_in_process(pdf_path, output_path)
                    
                    if result['success']:
                        # Enviar resultado via queue
                        self.conversion_queue.put({
                            'type': 'result',
                            'success': True,
                            'result': result,
                            'filename': os.path.basename(pdf_path),
                            'log': f"✅ Sucesso: {os.path.basename(pdf_path)} - {result['transactions_count']} transações"
                        })
                    else:
                        # Enviar erro via queue
                        self.conversion_queue.put({
                            'type': 'result',
                            'success': False,
                            'result': None,
                            'filename': os.path.basename(pdf_path),
                            'log': f"❌ Erro: {os.path.basename(pdf_path)} - {result['error']}"
                        })
                    
                except Exception as e:
                    # Enviar erro via queue
                    self.conversion_queue.put({
                        'type': 'result',
                        'success': False,
                        'result': None,
                        'filename': os.path.basename(pdf_path),
                        'log': f"❌ Erro inesperado: {os.path.basename(pdf_path)} - {str(e)}"
                    })
            
            # Finalizar via queue
            if self.is_converting:  # Só finalizar se ainda estiver convertendo
                self.conversion_queue.put({'type': 'finish'})
                self.log_message("🎉 Conversão concluída!")
                
        except Exception as e:
            self.log_message(f"❌ Erro crítico na conversão: {str(e)}")
            self.conversion_queue.put({'type': 'finish'})
    
    def run_conversion_in_process(self, pdf_path, output_path):
        """Executa conversão em processo separado"""
        try:
            # Criar queue para comunicação com processo
            result_queue = multiprocessing.Queue()
            
            # Criar processo para conversão
            process = multiprocessing.Process(
                target=run_conversion_process,
                args=(pdf_path, output_path, result_queue)
            )
            
            # Iniciar processo
            process.start()
            
            # Aguardar resultado com timeout
            try:
                result = result_queue.get(timeout=300)  # 5 minutos timeout
                process.join(timeout=1)  # Aguardar processo finalizar
                return result
            except:
                # Se timeout, terminar processo
                process.terminate()
                process.join()
                return {'success': False, 'error': 'Timeout na conversão'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    
    
    def finish_conversion(self):
        """Finaliza o processo de conversão"""
        # Parar loading
        self.stop_loading()
        
        self.status_label.configure(text="✅ Conversão concluída!")
        self.convert_btn.configure(state="normal", text="🔄 Converter", text_color=("#FFFFFF", "#F0F0F0"))
        self.is_converting = False
        
        # Limpar thread
        self.conversion_thread = None
        
        # Limpar arquivos selecionados e resetar interface
        self.clear_interface_after_conversion()
    
    def clear_interface_after_conversion(self):
        """Limpa a interface após a conversão ser concluída"""
        # Limpar arquivos selecionados
        self.selected_files = []
        
        # Resetar área de drag & drop
        self.drag_drop_state = "empty"
        self.update_drag_drop_appearance()
        
        # Resetar label de arquivos
        self.files_label.configure(text="Nenhum arquivo selecionado")
        
        # Desabilitar botão de conversão
        self.convert_btn.configure(state="disabled", text_color=("#FFFFFF", "#F0F0F0"))
        
        # Resetar status após um pequeno delay
        self.root.after(2000, self.reset_status)  # 2 segundos de delay
    
    def reset_status(self):
        """Reseta o status para o estado inicial"""
        self.status_label.configure(text="Pronto para converter")
    
    def add_to_history(self, result, filename):
        """Adiciona resultado ao histórico"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Determinar status
        if result['totals_match']:
            status = "✅ OK"
        else:
            status = "⚠️ Diferença"
        
        # Adicionar dados do histórico
        history_data = {
            'timestamp': timestamp,
            'filename': filename,
            'bank_type': result['bank_type'],
            'transactions_count': result['transactions_count'],
            'pdf_total': result['pdf_total'],
            'excel_total': result['excel_total'],
            'status': status
        }
        
        # Adicionar à lista de histórico
        self.conversion_history.append(history_data)
        
        # Atualizar exibição do histórico com tratamento de erro
        try:
            self.update_history_display()
        except Exception as e:
            print(f"Erro ao atualizar histórico: {e}")
            # Continuar mesmo com erro no histórico
    
    def clear_history(self):
        """Limpa o histórico de conversões"""
        if messagebox.askyesno("Confirmar", "Deseja limpar todo o histórico?"):
            # Limpar lista de histórico
            self.conversion_history.clear()
            
            # Atualizar exibição
            self.update_history_display()
            
            self.log_message("🗑️ Histórico limpo")
    
    def export_history(self):
        """Exporta o histórico para arquivo"""
        if not self.conversion_history:
            messagebox.showinfo("Info", "Nenhum histórico para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar histórico",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("HISTÓRICO DE CONVERSÕES - CONVERSOR FINANCEIRO\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for entry in self.conversion_history:
                        f.write(f"Data: {entry['timestamp']}\n")
                        f.write(f"Arquivo: {entry['filename']}\n")
                        f.write(f"Banco: {entry['result']['bank_type'].title()}\n")
                        f.write(f"Transações: {entry['result']['transactions_count']}\n")
                        f.write(f"Total PDF: R$ {entry['result']['pdf_total']:,.2f}\n")
                        f.write(f"Total Excel: R$ {entry['result']['excel_total']:,.2f}\n")
                        f.write(f"Status: {'OK' if entry['result']['totals_match'] else 'Diferença'}\n")
                        f.write("-" * 40 + "\n\n")
                
                self.log_message(f"📤 Histórico exportado: {os.path.basename(file_path)}")
                messagebox.showinfo("Sucesso", f"Histórico exportado com sucesso!\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar histórico:\n{str(e)}")
    
    def log_message(self, message):
        """Adiciona mensagem ao log (agora apenas no console)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)  # Log apenas no console
    
    def on_closing(self):
        """Manipula o fechamento da janela"""
        if self.is_converting:
            if messagebox.askokcancel("Sair", "A conversão está em andamento. Deseja realmente sair?"):
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        # Mensagem de boas-vindas
        self.log_message("🚀 Conversor Financeiro iniciado")
        self.log_message("💡 Selecione arquivos PDF para começar")
        
        # Forçar inicialização completa após um delay
        self.root.after(100, self._ensure_interface_ready)
        
        # Iniciar loop principal
        self.root.mainloop()

def main():
    """Função principal"""
    app = ConversorGUIModerno()
    app.run()

if __name__ == "__main__":
    main()
