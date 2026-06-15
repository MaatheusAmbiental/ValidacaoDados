# core/processor.py
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class HydroProcessor:
    def __init__(self, config, auth_data):
        self.config = config
        self.auth_data = auth_data

    def _get_connection(self):
        server, db = os.getenv('DB_SERVER'), os.getenv('DB_NAME')
        if self.auth_data['windows_auth']:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={db};Trusted_Connection=yes;'
        else:
            u, p = self.auth_data['user'], self.auth_data['password']
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={db};UID={u};PWD={p};'
        return pyodbc.connect(conn_str, timeout=30)

    def _generate_comparison_sql(self):
        logic = []
        # Valores Decimais (Tolerância 0.1)
        for col in self.config['value_cols']:
            # Blindagem contra NULL: Se um for NULL e outro não, resulta em 0.
            logic.append(f"""(CASE 
                WHEN p.{col} IS NULL AND i.{col} IS NULL THEN 1 
                WHEN p.{col} IS NULL OR i.{col} IS NULL THEN 0
                WHEN ABS(ROUND(p.{col},1) - ROUND(i.{col},1)) <= 0.1 THEN 1 
                ELSE 0 END)""")
        
        # Status e Campos Exatos
        exacts = self.config['status_cols'] + self.config.get('extra_exact_cols', [])
        for col in exacts:
            logic.append(f"""(CASE 
                WHEN p.{col} IS NULL AND i.{col} IS NULL THEN 1 
                WHEN p.{col} IS NULL OR i.{col} IS NULL THEN 0
                WHEN p.{col} = i.{col} THEN 1 
                ELSE 0 END)""")
        
        return " * ".join(logic)

    def process(self, resp_id, ano):
        tabela = self.config['table']
        join_keys = " AND ".join([f"p.{c} = i.{c}" for c in self.config['key_cols']])
        comp_logic = self._generate_comparison_sql()

        query = f"""
        WITH ImportedRecords AS (
            SELECT i.* FROM {tabela} i
            INNER JOIN dbo.Estacao e ON i.EstacaoCodigo = e.Codigo
            WHERE i.Importado = 1 AND i.Temporario = 0 AND i.Removido = 0
            AND e.ResponsavelCodigo = ? AND YEAR(i.Data) = ?
        ),
        PermanentRecords AS (
            SELECT p.* FROM {tabela} p
            INNER JOIN dbo.Estacao e ON p.EstacaoCodigo = e.Codigo
            WHERE p.Importado = 0 AND p.Temporario = 0 AND p.Removido = 0
            AND e.ResponsavelCodigo = ? AND YEAR(p.Data) = ?
        )
        SELECT 
            i.RegistroID AS RegistroID_file,
            p.RegistroID AS RegistroID_db,
            i.EstacaoCodigo, i.Data,
            CASE 
                WHEN p.RegistroID IS NULL THEN 'Inexistente'
                WHEN ISNULL(({comp_logic}), 0) = 1 THEN 'Idêntico'
                ELSE 'Diferente'
            END AS Situacao
        FROM ImportedRecords i
        LEFT JOIN PermanentRecords p ON {join_keys}
        """
        
        conn = self._get_connection()
        try:
            df = pd.read_sql(query, conn, params=[int(resp_id), int(ano), int(resp_id), int(ano)])
            if df.empty:
                return df, {'Idêntico': 0, 'Diferente': 0, 'Inexistente': 0}

            counts = df['Situacao'].value_counts(normalize=True).to_dict()
            resumo = {k: counts.get(k, 0) * 100 for k in ['Idêntico', 'Diferente', 'Inexistente']}
            return df, resumo
        finally:
            conn.close()
