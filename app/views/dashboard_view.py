import streamlit as st
import plotly.express as px
from controllers.data_controller import (
    obter_consumo,
    obter_pendentes,
    obter_nao_consumidos_nao_recebidos,
    obter_transformacao,
    obter_vendas_por_produto,
    obter_pedidos_pendentes,
    obter_entradas_mercadorias,
    obter_anomalias,
)

def exibir_dashboard():
    st.set_page_config(page_title="Dashboard Systock", layout="wide")

    st.title("📊 Dashboard de Dados Systock")

    # Criação de abas para organizar o conteúdo
    aba1, aba2, aba3 = st.tabs([
        "📦 Consumo e Pendências",
        "📊 Resumo Geral",
        "🚨 Anomalias e Transformações"
    ])

    # Aba 1: Consumo e Pendências
    with aba1:
        col1, col2 = st.columns(2)

        # Coluna 1: Consumo por produto
        with col1:
            st.subheader("Consumo por Produto - Fevereiro de 2025")
            df_consumo = obter_consumo()
            if not df_consumo.empty:
                fig_consumo = px.bar(
                    df_consumo,
                    x="produto_id",
                    y="total_consumo",
                    title="Consumo por Produto",
                    labels={"produto_id": "Produto", "total_consumo": "Total Consumido"},
                )
                st.plotly_chart(fig_consumo, use_container_width=True)
            else:
                st.warning("Nenhum dado de consumo encontrado.")

        # Coluna 2: Produtos com requisição pendente
        with col2:
            st.subheader("Produtos com Requisição Pendente")
            df_pendentes = obter_pendentes()
            if not df_pendentes.empty:
                fig_pendentes = px.pie(
                    df_pendentes,
                    names="produto_id",
                    values="qtde_pendente",
                    title="Produtos Pendentes",
                )
                st.plotly_chart(fig_pendentes, use_container_width=True)
            else:
                st.warning("Nenhum dado de pendências encontrado.")

    # Aba 2: Resumo Geral
    with aba2:
        st.subheader("Resumo Geral")
        col1, col2 = st.columns(2)

        # Coluna 1: Produtos não consumidos e não recebidos
        with col1:
            st.subheader("Produtos Não Consumidos e Não Recebidos")
            df_nao_consumidos = obter_nao_consumidos_nao_recebidos()
            if not df_nao_consumidos.empty:
                st.dataframe(df_nao_consumidos)
            else:
                st.warning("Nenhum dado de produtos não consumidos ou não recebidos encontrado.")

        # Coluna 2: Transformações de dados
        with col2:
            st.subheader("Transformações de Dados")
            df_transformacao = obter_transformacao()
            if not df_transformacao.empty:
                st.dataframe(df_transformacao)
            else:
                st.warning("Nenhum dado de transformação encontrado.")

    # Aba 3: Anomalias e Transformações
    with aba3:
        st.subheader("Detecção de Anomalias")
        df_anomalias = obter_anomalias()
        if not df_anomalias.empty:
            st.dataframe(df_anomalias)
        else:
            st.warning("Nenhuma anomalia encontrada.")

        st.subheader("Entradas de Mercadorias")
        df_entradas = obter_entradas_mercadorias()
        if not df_entradas.empty:
            st.dataframe(df_entradas)
        else:
            st.warning("Nenhum dado de entradas encontrado.")