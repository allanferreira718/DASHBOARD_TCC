import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Dashboard de Empregabilidade", layout="wide")

# Title
st.title("Dashboard de Empregabilidade de Egressos (2019-2024)")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cleaned_data.csv')
        return df
    except:
        st.error("Erro ao carregar os dados. Verifique se cleaned_data.csv está no repositório.")
        return None

df = load_data()

if df is not None:
    # ====== FILTROS NA SIDEBAR ======
    st.sidebar.header("Filtros")
    
    # Filtro de Estado
    estados = sorted(df['state'].unique())
    selected_states = st.sidebar.multiselect("Estados", estados, default=estados)
    
    # Filtro de Setor
    setores = sorted(df['sector'].unique())
    selected_sectors = st.sidebar.multiselect("Setores", setores, default=setores)
    
    # Filtro de Empregabilidade
    employment_status = sorted(df['employed'].unique())
    selected_employment = st.sidebar.multiselect("Status de Emprego", employment_status, default=employment_status)
    
    # Filtro de Range de Salário
    salary_min, salary_max = st.sidebar.slider(
        "Range de Salário",
        int(df['salary'].min()),
        int(df['salary'].max()),
        (int(df['salary'].min()), int(df['salary'].max()))
    )
    
    # Filtro de Ano de Admissão
    years = sorted(df['admission_year'].unique())
    selected_years = st.sidebar.multiselect("Anos de Admissão", years, default=years)
    
    # Aplicar filtros ao dataframe
    filtered_df = df[
        (df['state'].isin(selected_states)) &
        (df['sector'].isin(selected_sectors)) &
        (df['employed'].isin(selected_employment)) &
        (df['salary'].between(salary_min, salary_max)) &
        (df['admission_year'].isin(selected_years))
    ]
    
    st.sidebar.info(f"Total de registros selecionados: {len(filtered_df)} de {len(df)}")
    
    # ====== KPIs ======
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Egressos", len(filtered_df))
    
    with col2:
        if 'salary' in filtered_df.columns and len(filtered_df) > 0:
            st.metric("Salário Médio", f"R$ {filtered_df['salary'].mean():,.2f}")
        else:
            st.metric("Salário Médio", "N/A")
    
    with col3:
        if 'employed' in filtered_df.columns and len(filtered_df) > 0:
            employed = (filtered_df['employed'] == 'Sim').sum()
            employment_rate = (employed / len(filtered_df)) * 100
            st.metric("Taxa de Empregabilidade", f"{employment_rate:.1f}%")
        else:
            st.metric("Taxa de Empregabilidade", "N/A")
    
    st.divider()
    
    # ====== DADOS CARREGADOS ======
    st.subheader("Dados Carregados")
    st.dataframe(filtered_df.head(10))
    
    # ====== SEÇÃO DE GRÁFICOS ======
    if len(filtered_df) > 0:
        st.divider()
        st.subheader("Análise Gráfica")
        
        # Gráfico 1: Salário por Setor
        st.write("#### Salário Médio por Setor")
        salary_by_sector = filtered_df.groupby('sector')['salary'].mean().sort_values(ascending=False)
        if len(salary_by_sector) > 0:
            fig1 = px.bar(salary_by_sector, x=salary_by_sector.index, y=salary_by_sector.values, labels={'x': 'Setor', 'y': 'Salário Médio'}, color=salary_by_sector.values, color_continuous_scale='viridis')
            st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Empregabilidade por Estado
        st.write("#### Taxa de Empregabilidade por Estado")
        employment_by_state = (filtered_df[filtered_df['employed'] == 'Sim'].groupby('state').size() / filtered_df.groupby('state').size() * 100).sort_values(ascending=False)
        if len(employment_by_state) > 0:
            fig2 = px.bar(employment_by_state, x=employment_by_state.index, y=employment_by_state.values, labels={'x': 'Estado', 'y': 'Taxa de Empregabilidade (%)'}, color=employment_by_state.values, color_continuous_scale='blues')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfico 3: Distribuição de Salários
        st.write("#### Distribuição de Salários")
        if len(filtered_df) > 0:
            fig3 = px.histogram(filtered_df, x='salary', nbins=10, labels={'salary': 'Salário', 'count': 'Quantidade'}, color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig3, use_container_width=True)
        
        # Gráfico 4: Egressos por Ano
        st.write("#### Egressos Admitidos por Ano")
        egressos_por_ano = filtered_df['admission_year'].value_counts().sort_index()
        if len(egressos_por_ano) > 0:
            fig4 = px.line(egressos_por_ano, x=egressos_por_ano.index, y=egressos_por_ano.values, labels={'x': 'Ano', 'y': 'Quantidade'}, markers=True)
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
else:
    st.error("Erro ao carregar os dados.")
