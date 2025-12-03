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
