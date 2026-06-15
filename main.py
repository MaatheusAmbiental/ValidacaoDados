# main.py
import customtkinter as ctk 
from tkinter import messagebox
from ui.main_window import MainWindow
from ui.report_window import ReportWindow
from core.processor import HydroProcessor
from core.schemas import (CHUVA_CONFIG, CHUVA2_CONFIG, CHUVA24_CONFIG, 
                          COTAS_CONFIG, COTAS24_CONFIG, 
                          VAZOES_CONFIG, VAZOES24_CONFIG)

class HydroApp:
    def __init__(self):
        self.mapping = {
            "Chuvas": CHUVA_CONFIG,
            "Chuvas2": CHUVA2_CONFIG,
            "Chuvas24": CHUVA24_CONFIG,
            "Cotas": COTAS_CONFIG,
            "Cotas24": COTAS24_CONFIG,
            "Vazoes": VAZOES_CONFIG,
            "Vazoes24": VAZOES24_CONFIG
        }
        self.view = MainWindow(on_process_callback=self.executar_validacao)
        self.view.type_menu.configure(values=list(self.mapping.keys()))
        self.processor = None

    def executar_validacao(self):
        resp = self.view.resp_entry.get()
        ano = self.view.year_entry.get()
        
        if not resp.isdigit() or not ano.isdigit():
            messagebox.showwarning("Erro", "Responsável e Ano devem ser numéricos.")
            return

        auth = {
            "windows_auth": self.view.win_auth_var.get(),
            "user": self.view.user_entry.get(),
            "password": self.view.pwd_entry.get()
        }

        tipo_selecionado = self.view.type_menu.get()
        config = self.mapping[tipo_selecionado]

        try:
            self.view.btn_run.configure(state="disabled", text="Processando...")
            self.view.update()

            self.processor = HydroProcessor(config, auth)
            df, resumo = self.processor.process(resp, ano)

            self.view.card_ok.update_value(resumo['Idêntico'])
            self.view.card_diff.update_value(resumo['Diferente'])
            self.view.card_null.update_value(resumo['Inexistente'])

            if not df.empty:
                self.report = ReportWindow(self.view, df, self.sincronizar_banco)
            else:
                messagebox.showinfo("Vazio", "Nenhum dado pendente (Importado=1) encontrado.")

        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Falha na SQL: {str(e)}")
        finally:
            self.view.btn_run.configure(state="normal", text="INICIAR COMPARAÇÃO")

    def sincronizar_banco(self, df):
        conn = self.processor._get_connection()
        cursor = conn.cursor()
        cfg = self.processor.config
        tabela = cfg['table']
        cols = cfg['value_cols'] + cfg['status_cols'] + cfg.get('extra_exact_cols', [])
        
        try:
            for _, row in df.iterrows():
                if row['Situacao'] == 'Idêntico':
                    cursor.execute(f"DELETE FROM {tabela} WHERE RegistroID = ?", row['RegistroID_file'])
                elif row['Situacao'] == 'Inexistente':
                    cursor.execute(f"UPDATE {tabela} SET Importado = 0 WHERE RegistroID = ?", row['RegistroID_file'])
                elif row['Situacao'] == 'Diferente':
                    cursor.execute(f"SELECT {','.join(cols)} FROM {tabela} WHERE RegistroID = ?", row['RegistroID_file'])
                    dados = cursor.fetchone()
                    set_clause = ", ".join([f"{c}=?" for c in cols])
                    cursor.execute(f"UPDATE {tabela} SET {set_clause}, Importado = 0 WHERE RegistroID = ?", list(dados) + [row['RegistroID_db']])
                    cursor.execute(f"DELETE FROM {tabela} WHERE RegistroID = ?", row['RegistroID_file'])
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Base sincronizada com sucesso!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro na sincronização: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    app = HydroApp()
    app.view.mainloop()
