import streamlit as st
import pandas as pd
from io import StringIO

# Configuração da página
st.set_page_config(page_title="Tratamento de Dados", layout="wide")
st.title("Tratamento de Dados")

# Layout com colunas
col2, col3 = st.columns(2)

# Upload do arquivo Excel
with col3:
    arquivo = st.file_uploader("Envie um arquivo Excel", type=[".xlsx", ".xls"])

# Processamento dos dados
if arquivo is not None:
    st.success("Planilha tratada com sucesso! Baixe os dados no botão ao lado.")
    # Lê todas as abas do Excel como dicionário
    dados = pd.read_excel(arquivo, sheet_name=None)
    
    # Usa a primeira aba como padrão
    primeira_aba = list(dados.keys())[0]
    df = dados[primeira_aba]

    pd.set_option('display.max_columns', None)

    # Filtra apenas as colunas desejadas
    colunas = ['cp_competencia', 'cp_nome_epr', 'cp_salario', 'cp_nome_eve_p', 'cp_eve_val_p']
    df_tratado = df[colunas].copy()

    # Remove linhas com valores nulos em 'cp_nome_eve_p'
    df_tratado.dropna(subset=['cp_nome_eve_p'], inplace=True)

    # Cria tabela pivô
    df_pivot = df_tratado.pivot_table(
        index=['cp_competencia', 'cp_nome_epr', 'cp_salario'],
        columns='cp_nome_eve_p',
        values='cp_eve_val_p',
        aggfunc='first'
    ).reset_index()  # Reset index para facilitar visualização e exportação

    # Exibe a tabela no app
    st.dataframe(df_pivot, width=1000, height=400)
    st.balloons()
    

    # Sidebar com opções de exportação
    with st.sidebar:
        # Seleção de colunas baseadas nas categorias de eventos únicos
        colunas_disponiveis = df['cp_nome_eve_p'].dropna().unique().tolist()
        colunas_selecionadas = st.multiselect(
            "Selecione as colunas que deseja exportar:",
            options=colunas_disponiveis
        )

        # Prepara dados para exportar
        if colunas_selecionadas:
            # Garante que colunas existem na tabela pivô
            colunas_exportar = ['cp_competencia', 'cp_nome_epr', 'cp_salario'] + colunas_selecionadas
            df_exportar = df_pivot[colunas_exportar]

            # Converte DataFrame para CSV em memória
            csv_buffer = StringIO()
            df_exportar.to_excel(csv_buffer)
            csv_data = csv_buffer.getvalue()

            # Botão de download
            st.download_button(
                label="Download dos dados tratados",
                data=csv_data,
                file_name="RH_SIMPLIFICADO.xls",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                icon="⬇️"
            )