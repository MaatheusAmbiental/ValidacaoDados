# ui/main_window.py
import customtkinter as ctk
from ui.components import HeaderLabel, StatusCard

class MainWindow(ctk.CTk):
    def __init__(self, on_process_callback):
        super().__init__()
        self.on_process_callback = on_process_callback
        
        self.title("Validador Hidrológico Pro")
        self.geometry("900x680")
        self._setup_ui()

    def _setup_ui(self):
        HeaderLabel(self, text="Sincronização de Dados Hidrológicos").pack(pady=20)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- LADO ESQUERDO: CONFIGURAÇÕES E FILTROS ---
        left_frame = ctk.CTkFrame(main_container, width=320)
        left_frame.pack(side="left", fill="both", padx=10, pady=10)

        ctk.CTkLabel(left_frame, text="Configurações de Tabela", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        
        # Menu de opções (populado dinamicamente no main.py)
        self.type_menu = ctk.CTkOptionMenu(left_frame, values=["Chuvas", "Chuvas2", "Chuvas24", "Cotas", "Cotas24", "Vazoes", "Vazoes24"])
        self.type_menu.pack(pady=10, padx=20, fill="x")

        # Seção de Filtros (Responsável e Ano)
        ctk.CTkLabel(left_frame, text="Filtros de Busca", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.filter_frame = ctk.CTkFrame(left_frame)
        self.filter_frame.pack(pady=5, padx=20, fill="x")
        
        self.resp_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="Cód. Responsável (Número)")
        self.resp_entry.pack(pady=5, padx=10, fill="x")
        
        self.year_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="Ano (YYYY)")
        self.year_entry.pack(pady=5, padx=10, fill="x")

        # Seção de Autenticação
        ctk.CTkLabel(left_frame, text="Autenticação SQL", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        self.auth_frame = ctk.CTkFrame(left_frame)
        self.auth_frame.pack(pady=5, padx=20, fill="x")
        
        self.win_auth_var = ctk.BooleanVar(value=True)
        self.chk_win = ctk.CTkCheckBox(self.auth_frame, text="Windows Authentication", 
                                       variable=self.win_auth_var, command=self.toggle_auth)
        self.chk_win.pack(pady=10, padx=10)

        self.user_entry = ctk.CTkEntry(self.auth_frame, placeholder_text="Usuário SQL", state="disabled")
        self.user_entry.pack(pady=5, padx=10, fill="x")
        
        self.pwd_entry = ctk.CTkEntry(self.auth_frame, placeholder_text="Senha SQL", show="*", state="disabled")
        self.pwd_entry.pack(pady=5, padx=10, fill="x")

        # Botão de Ação Principal
        self.btn_run = ctk.CTkButton(left_frame, text="INICIAR COMPARAÇÃO", 
                                     fg_color="#2d5a27", hover_color="#1e3d1a",
                                     height=45, font=("Roboto", 14, "bold"),
                                     command=self.on_process_callback)
        self.btn_run.pack(side="bottom", pady=25, padx=20, fill="x")

        # --- LADO DIREITO: DASHBOARD DE RESULTADOS ---
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(right_frame, text="Resumo da Análise de Consistência", font=("Roboto", 16, "bold")).pack(pady=15)

        self.card_ok = StatusCard(right_frame, "Idênticos (Exclusão Segura)", color="#2d5a27")
        self.card_ok.pack(pady=10, padx=30, fill="x")

        self.card_diff = StatusCard(right_frame, "Diferentes (Update Necessário)", color="#7a2a2a")
        self.card_diff.pack(pady=10, padx=30, fill="x")

        self.card_null = StatusCard(right_frame, "Inexistentes (Migrar para Permanente)", color="#4a4a4a")
        self.card_null.pack(pady=10, padx=30, fill="x")

    def toggle_auth(self):
        """Ativa/Desativa campos de login baseado no checkbox de Autenticação Windows"""
        state = "disabled" if self.win_auth_var.get() else "normal"
        self.user_entry.configure(state=state)
        self.pwd_entry.configure(state=state)
        if state == "disabled":
            self.user_entry.delete(0, 'end')
            self.pwd_entry.delete(0, 'end')
