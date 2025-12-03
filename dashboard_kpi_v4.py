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
    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Egressos", len(df))
    
    with col2:
        if 'salary' in df.columns:
            st.metric("Salário Médio", f"R$ {df['salary'].mean():,.2f}")
        else:
            st.metric("Salário Médio", "N/A")
    
    with col3:
        if 'employed' in df.columns:
            employed = (df['employed'] == 'Sim').sum()
            employment_rate = (employed / len(df)) * 100
            st.metric("Taxa de Empregabilidade", f"{employment_rate:.1f}%")
        else:
            st.metric("Taxa de Empregabilidade", "N/A")
    
    st.divider()
    
    # Display raw data
    st.subheader("Dados Carregados")
    st.dataframe(df.head(10))
    
    st.info("Dashboard em desenvolvimento. Mais gráficos e análises em breve!")
else:
    st.warning("Dados não disponíveis")

# Seção de Gráficos
if df is not None and len(df) > 0:
    st.divider()
    st.subheader("Análise Gráfica")
    
    # Gráfico 1: Salário por Setor
    st.write("#### Salário Médio por Setor")
    salary_by_sector = df.groupby('sector')['salary'].mean().sort_values(ascending=False)
    fig1 = px.bar(salary_by_sector, x=salary_by_sector.index, y=salary_by_sector.values, labels={'x': 'Setor', 'y': 'Salário Médio'}, color=salary_by_sector.values, color_continuous_scale='viridis')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Empregabilidade por Estado
    st.write("#### Taxa de Empregabilidade por Estado")
    employment_by_state = (df[df['employed'] == 'Sim'].groupby('state').size() / df.groupby('state').size() * 100).sort_values(ascending=False)
    fig2 = px.bar(employment_by_state, x=employment_by_state.index, y=employment_by_state.values, labels={'x': 'Estado', 'y': 'Taxa de Empregabilidade (%)'}, color=employment_by_state.values, color_continuous_scale='blues')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico 3: Distribuição de Salários
    st.write("#### Distribuição de Salários")
    fig3 = px.histogram(df, x='salary', nbins=10, labels={'salary': 'Salário', 'count': 'Quantidade'}, color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig3, use_container_width=True)
    
    # Gráfico 4: Egressos por Ano
    st.write("#### Egressos Admitidos por Ano")
    egressos_por_ano = df['admission_year'].value_counts().sort_index()
    fig4 = px.line(egressos_por_ano, x=egressos_por_ano.index, y=egressos_por_ano.values, labels={'x': 'Ano', 'y': 'Quantidade'}, markers=True)
    st.plotly_chart(fig4, use_container_width=True)
