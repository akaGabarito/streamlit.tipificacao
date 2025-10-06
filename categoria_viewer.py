import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Categorias de Documentos",
    page_icon="📄",
    layout="wide"
)

# Título
st.title("📄 Categorias de Documentos")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('data/categoria_doc.csv')
    return df

df = load_data()

# Exibir dados
st.subheader("Categorias Disponíveis")

# Criar colunas para cada categoria
cols = st.columns(len(df.columns))

for idx, col_name in enumerate(df.columns):
    with cols[idx]:
        st.markdown(f"### {col_name}")
        # Filtrar valores não vazios
        docs = df[col_name].dropna().tolist()
        for doc in docs:
            if doc.strip():  # Verificar se não está vazio
                st.markdown(f"- {doc}")

# Tabela completa
st.subheader("Tabela Completa")
st.dataframe(df, use_container_width=True)

# Estatísticas
st.subheader("Estatísticas")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Categorias", len(df.columns))

with col2:
    total_docs = df.notna().sum().sum()
    st.metric("Total de Documentos", int(total_docs))

with col3:
    st.metric("Docs Identificatórios", df['IDENTIFICATORIO'].notna().sum())

with col4:
    st.metric("Docs Financeiros", df['FINANCEIROS'].notna().sum())
