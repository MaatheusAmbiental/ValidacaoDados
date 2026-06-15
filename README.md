# Validador de Dados Hidrológico Pro 🌊

markdown
![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![SQL Server](https://img.shields.io/badge/database-SQL_Server-red.svg)

![Interface Principal](screenshots/main_view.png)
![Relatório de Decisão](screenshots/report_view.png)

O **Validador Hidrológico Pro** é uma ferramenta de desktop desenvolvida em Python para automação, auditoria e sincronização de dados hidrológicos (Chuvas, Cotas e Vazões). O sistema realiza a comparação entre arquivos de importação e a base de dados permanente do SQL Server, permitindo uma gestão eficiente e segura dos dados.

## 🚀 Funcionalidades

- **Comparação Inteligente:** Validação linha a linha com "Regra de Ouro" (tolerância de 0,1 para decimais).
- **Dashboard Gerencial:** Visualização rápida do percentual de dados Idênticos, Diferentes e Inexistentes.
- **Tomada de Decisão Automatizada:**
    - **Dados Idênticos:** Exclusão automática de duplicatas no banco.
    - **Dados Inexistentes:** Promoção de registros importados para o status Permanente (`Importado = 0`).
    - **Dados Diferentes:** Identificação exata da divergência e realização de `UPDATE` preservando o `RegistroID` original.
- **Suporte Multi-Tabelas:** Compatível com `dbo.Chuvas24`, `dbo.Cotas24`, `dbo.Vazoes24` e versões anteriores.
- **Segurança de Dados:** Suporte a Windows Authentication e SQL Server Authentication.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Interface Gráfica:** `CustomTkinter` (Modern UI)
- **Processamento de Dados:** `Pandas` e `NumPy`
- **Banco de Dados:** `pyodbc` (Conexão com SQL Server)
- **Portabilidade:** `PyInstaller` (Geração de executável único `.exe`)

## 📋 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter as seguintes bibliotecas instaladas:

- bash
pip install pandas customtkinter pyodbc python-dotenv openpyxl

⚙️ Configuração
Clone o repositório.

Necessário ter o ODBC Driver for SQL Server (pyodbc)

Configure o arquivo .env na raiz do projeto com as informações do seu servidor:

Snippet de código
DB_SERVER=SEU_SERVIDOR,1433
DB_NAME=NOME_DO_BANCO
🖥️ Como Executar
Para rodar a aplicação em modo de desenvolvimento:

Bash
python main.py
Para gerar o executável (.exe):

Bash
build.bat
📊 Fluxo de Trabalho (Business Logic)
Seleção: O usuário escolhe o tipo de dado (Chuva/Cota/Vazão) e seleciona o arquivo Excel/CSV.

Processamento: O sistema cruza os dados do arquivo com o banco de dados via key_cols (Estação, Data, Nível de Consistência).

Análise: Uma janela de relatório detalha cada inconsistência encontrada.

Sincronização: Com um clique, o sistema executa os comandos SQL necessários para manter a base íntegra e sem duplicidades.

👤 Autor
Matheus Castro – Engenheiro Ambiental
Especialista em Automação de Dados Hidrológicos e GIS.

Projeto desenvolvido para otimização de processos de consistência de dados da Agência Nacional de Águas (ANA).
