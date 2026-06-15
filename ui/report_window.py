# ui/report_window.py
import customtkinter as ctk
from tkinter import ttk, messagebox

class ReportWindow(ctk.CTkToplevel):
    def __init__(self, parent, df, on_confirm_callback):
        super().__init__(parent)
        self.title("Tomada de Decisão - Sincronização")
        self.geometry("950x550")
        self.df = df
        self.on_confirm = on_confirm_callback
        
        # Garante que a janela fique por cima
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Análise de Consistência Hidrológica (Importado = 1)", font=("Roboto", 18, "bold")).pack(pady=15)

        # Container para a Treeview (Tabela)
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Estilização da Treeview para combinar com o tema escuro
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        cols = ("Estação", "Data", "Situação")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Inserção dos dados
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row['EstacaoCodigo'], row['Data'], row['Situacao']))

        # Botão de Confirmação Final
        ctk.CTkButton(self, text="EXECUTAR SINCRONIZAÇÃO NO SQL SERVER", 
                      fg_color="#7a2a2a", hover_color="#5a1f1f",
                      height=45, font=("Roboto", 14, "bold"),
                      command=self.confirmar).pack(pady=20)

    def confirmar(self):
        if messagebox.askyesno("Confirmar Ação", "Deseja aplicar as exclusões e atualizações na base de produção?"):
            self.on_confirm(self.df)
            self.destroy()
