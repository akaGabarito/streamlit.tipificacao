import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Análise de Mercado", page_icon="🧭", layout="wide")

# Tema Minimalista - Inspirado em Anthropic
st.markdown("""
    <style>
    /* Fundo limpo e claro */
    .stApp {
        background: #f9fafb;
        color: #1f2937;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remover backgrounds de cards desnecessários */
    div[data-testid="stVerticalBlock"] > div {
        background: transparent;
    }

    /* Sidebar clean */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Títulos simples e elegantes */
    h1 {
        color: #111827 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h2, h3 {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
    }

    h4, h5, h6 {
        color: #4b5563 !important;
        font-weight: 500 !important;
    }

    /* Texto legível */
    p, span, label {
        color: #6b7280 !important;
    }

    /* Métricas com destaque */
    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 1.875rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Tabelas limpas */
    .stDataFrame {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }

    /* Botões com efeito glassmorphism */
    .stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(21px) !important;
        -webkit-backdrop-filter: blur(21px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5),
            inset 0 -1px 0 rgba(255, 255, 255, 0.1),
            inset 0 0 12px 6px rgba(255, 255, 255, 0.6) !important;
        color: #111827 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 1px !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.8),
            transparent
        ) !important;
    }

    .stButton > button::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 1px !important;
        height: 100% !important;
        background: linear-gradient(
            180deg,
            rgba(255, 255, 255, 0.8),
            transparent,
            rgba(255, 255, 255, 0.3)
        ) !important;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        transform: translateY(-2px) !important;
        box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.6),
            inset 0 -1px 0 rgba(255, 255, 255, 0.2),
            inset 0 0 16px 8px rgba(255, 255, 255, 0.7) !important;
    }

    /* Botão primary (ativo) */
    .stButton > button[kind="primary"] {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        color: #2563eb !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: rgba(59, 130, 246, 0.25) !important;
    }

    /* Radio e checkboxes clean */
    .stRadio > label, .stCheckbox > label {
        color: #374151 !important;
        font-weight: 400 !important;
    }

    /* Expanders sutis */
    .streamlit-expanderHeader {
        background: transparent !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 6px !important;
        color: #374151 !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: #d1d5db !important;
        background: #f9fafb !important;
    }

    /* Separadores finos */
    hr {
        border-color: #e5e7eb !important;
        margin: 2rem 0 !important;
    }

    /* Tabs clean */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .stTabs [data-baseweb="tab"] {
        color: #6b7280 !important;
        font-weight: 500 !important;
        padding: 0.75rem 0 !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
    }

    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        border-bottom-color: #111827 !important;
        background: transparent !important;
    }

    /* Alertas sutis */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #86efac !important;
        border-radius: 6px !important;
        color: #166534 !important;
    }

    .stInfo {
        background: #eff6ff !important;
        border: 1px solid #93c5fd !important;
        border-radius: 6px !important;
        color: #1e40af !important;
    }

    .stWarning {
        background: #fffbeb !important;
        border: 1px solid #fcd34d !important;
        border-radius: 6px !important;
        color: #92400e !important;
    }

    .stError {
        background: #fef2f2 !important;
        border: 1px solid #fca5a5 !important;
        border-radius: 6px !important;
        color: #991b1b !important;
    }

    /* Inputs e selects limpos */
    .stTextInput > div > div, .stSelectbox > div > div {
        border-color: #e5e7eb !important;
        border-radius: 6px !important;
    }

    /* Remover sombras excessivas */
    * {
        box-shadow: none !important;
    }

    /* Adicionar sombras apenas onde necessário */
    .stDataFrame, .streamlit-expanderHeader {
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares
def normalize_header(s: str) -> str:
    import unicodedata, re
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii","ignore").decode("ascii")
    s = re.sub(r"\s+", " ", s.strip()).upper()

    # Mapear variações comuns de categorias
    mapeamento = {
        'IDENTIFICATORIO': 'IDENTIFICATORIO',
        'FINANCEIRO': 'FINANCEIRO',
        'FINANCEIROS': 'FINANCEIRO',
        'VEICULAR': 'VEICULAR',
        'JURIDICO': 'JURIDICO',
        'JURIDICOS': 'JURIDICO',
        'FUNCIONAL': 'FUNCIONAL',
        'FUNCIONAIS': 'FUNCIONAL'
    }

    return mapeamento.get(s, s)

def load_excel_data(excel_path):
    """
    Carrega dados do Excel com múltiplas abas:
    - Primeira aba: Categorias e tipos de documentos (referência do mercado)
    - Demais abas: Dados de cada empresa (nome da aba = nome da empresa)

    Retorna: (categorias_ref, df_empresas)
    """
    # Carregar todas as abas
    excel_file = pd.ExcelFile(excel_path)

    # Primeira aba = referência de categorias
    primeira_aba = excel_file.sheet_names[0]
    df_ref = pd.read_excel(excel_path, sheet_name=primeira_aba)

    categorias_ref = {}
    for col in df_ref.columns:
        docs = df_ref[col].dropna().tolist()
        docs = [d.strip() for d in docs if d and str(d).strip()]
        if docs:
            categorias_ref[col] = docs

    # Demais abas = empresas
    companies_data = []
    empresas_docs = {}

    for sheet_name in excel_file.sheet_names[1:]:
        empresa_name = sheet_name.strip().upper()
        df_empresa = pd.read_excel(excel_path, sheet_name=sheet_name)

        empresas_docs[empresa_name] = {}

        # Processar cada categoria no arquivo da empresa
        for col in df_empresa.columns:
            categoria_normalizada = normalize_header(col)
            docs = df_empresa[col].dropna().tolist()
            docs = [d.strip() for d in docs if d and str(d).strip()]
            empresas_docs[empresa_name][categoria_normalizada] = set(docs)

    # Criar matriz completa: para cada empresa, categoria e documento do mercado
    for empresa in empresas_docs.keys():
        for cat, docs_mercado in categorias_ref.items():
            cat_normalizada = normalize_header(cat)

            # Documentos que a empresa FAZ nesta categoria
            docs_empresa = empresas_docs[empresa].get(cat_normalizada, set())

            for doc in docs_mercado:
                # Verificar se a empresa faz este documento
                suporte = '✅' if doc in docs_empresa else '❌'

                companies_data.append({
                    'Empresa': empresa,
                    'Categoria': cat,
                    'Tipo de Documento': doc,
                    'Suporte (✅/❌)': suporte,
                    'Tecnologia (tags)': '',
                    'Observações': 'Tipifica' if suporte == '✅' else 'Não tipifica'
                })

    return categorias_ref, pd.DataFrame(companies_data)

def add_score(df: pd.DataFrame) -> pd.DataFrame:
    score_map = {
        "✅": 2,
        "❌": 0, "": 0, None: 0
    }
    return df.assign(score=df["Suporte (✅/❌)"].map(score_map).fillna(0).astype(int))

def calc_category_stats(df: pd.DataFrame, empresa: str, categoria: str) -> dict:
    """Calcula estatísticas de uma empresa em uma categoria específica"""
    cat_data = df[(df["Empresa"] == empresa) & (df["Categoria"] == categoria)]

    total_docs = len(df[df["Categoria"] == categoria]["Tipo de Documento"].unique())
    covered = cat_data[cat_data["score"] == 2]["Tipo de Documento"].nunique()

    return {
        "total": total_docs,
        "covered": covered,
        "coverage_pct": round(covered / total_docs * 100, 1) if total_docs > 0 else 0
    }

def create_category_comparison(df: pd.DataFrame, categorias: list, empresas: list) -> pd.DataFrame:
    """Cria matriz de comparação por categoria"""
    results = []

    for cat in categorias:
        for emp in empresas:
            stats = calc_category_stats(df, emp, cat)
            results.append({
                "Empresa": emp,
                "Categoria": cat,
                "Total Docs": stats["total"],
                "Tipificados": stats["covered"],
                "% Tipificação": stats["coverage_pct"]
            })

    return pd.DataFrame(results)

# Inicializar session state primeiro
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'home'

# Título - apenas na home
if st.session_state.view_mode == 'home':
    st.title(" Benchmarking de Tipificação de Documentos")
    st.subheader("Análise do mercado de tipificação de documentos para mapear oportunidades da Tirrell.")
    st.caption("Separamos a tipificação por categorias para facilitar a comparação.")
    st.markdown("---")

# Configuração do arquivo Excel
EXCEL_PATH = 'data/Pesquisa de mercado - Tipificação.xlsx'

# Carregar dados do Excel
try:
    categorias_ref, df = load_excel_data(EXCEL_PATH)
except Exception as e:
    st.sidebar.error(f"⚠️ Erro ao carregar {EXCEL_PATH}: {e}")
    st.error(f"Não foi possível carregar o arquivo Excel. Verifique se '{EXCEL_PATH}' existe.")
    st.stop()

# ===== SEÇÃO INICIAL: UNIVERSO DE DOCUMENTOS DO MERCADO (APENAS NA HOME) =====
if st.session_state.view_mode == 'home':

    st.header("Universo de Documentos do Mercado")
    st.caption("Categorias e tipos de documentos identificados.")

if st.session_state.view_mode == 'home' and categorias_ref:
    # Criar visualização em colunas
    cols = st.columns(len(categorias_ref))

    total_docs_mercado = sum(len(docs) for docs in categorias_ref.values())

    # Métricas gerais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📁 Total de Categorias", len(categorias_ref))
    with col2:
        st.metric("📄 Total de Documentos", total_docs_mercado)
    with col3:
        media_docs = total_docs_mercado / len(categorias_ref)
        st.metric("📊 Média por Categoria", f"{media_docs:.1f}")

    st.markdown("#### Documentos por Categoria")

    # Tabela detalhada
    tabela_categorias = []
    for cat, docs in categorias_ref.items():
        for idx, doc in enumerate(docs, 1):
            tabela_categorias.append({
                'Categoria': cat,
                'Nº': idx,
                'Tipo de Documento': doc
            })

    df_categorias = pd.DataFrame(tabela_categorias)

    # Criar tabs para cada categoria
    tabs = st.tabs(list(categorias_ref.keys()))

    for idx, (cat, docs) in enumerate(categorias_ref.items()):
        with tabs[idx]:
            cat_df = df_categorias[df_categorias['Categoria'] == cat][['Nº', 'Tipo de Documento']]

            col1, col2 = st.columns([1, 3])

            with col1:
                st.metric(f"Total em {cat}", len(docs))
                st.info(f"**{(len(docs)/total_docs_mercado*100):.1f}%** do mercado")

            with col2:
                st.dataframe(
                    cat_df,
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, len(docs) * 35 + 38)
                )

    # Gráfico de distribuição (colapsado)
    with st.expander("📊 Ver Distribuição de Documentos por Categoria"):
        dist_data = pd.DataFrame([
            {'Categoria': cat, 'Quantidade': len(docs)}
            for cat, docs in categorias_ref.items()
        ])

        chart = alt.Chart(dist_data).mark_bar().encode(
            x=alt.X('Quantidade:Q', title='Número de Documentos'),
            y=alt.Y('Categoria:N', sort='-x', title='Categoria'),
            color=alt.Color('Categoria:N', legend=None),
            tooltip=['Categoria', 'Quantidade']
        ).properties(height=300)

        st.altair_chart(chart, use_container_width=True)

    # Tabela consolidada (expandível)
    with st.expander("📋 Ver Tabela Completa de Todos os Documentos"):
        st.dataframe(
            df_categorias,
            use_container_width=True,
            hide_index=True
        )

if st.session_state.view_mode == 'home':
    st.markdown("---")

# Garantir colunas necessárias
required_cols = ["Empresa", "Categoria", "Tipo de Documento", "Suporte (✅/❌)"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Coluna obrigatória não encontrada: {col}")
        st.error(f"Colunas disponíveis: {list(df.columns)}")
        st.stop()

# Adicionar score
df = add_score(df)

# Identificar empresa principal (necessário para os filtros)
empresa_principal_options = [e for e in df["Empresa"].unique() if "tirrell" in e.lower() or "minha" in e.lower()]
if empresa_principal_options:
    tirrell_name = empresa_principal_options[0]
else:
    # Se não encontrar, usar a primeira empresa como padrão
    empresas_disponiveis = sorted(df["Empresa"].unique().tolist())
    tirrell_name = empresas_disponiveis[0]

# ===== LOGO TIRRELL NO SIDEBAR =====
st.sidebar.markdown("""
<div style="padding: 0.5rem 0 1.5rem 0; margin-bottom: 1rem;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22379.38 6575.22" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" style="width: 100%; height: auto; max-width: 180px;">
        <defs>
            <clipPath id="logo-horizontal_svg__id0">
                <path d="M11.03 11.03h22357.33V6564.2H11.03V11.03z"></path>
            </clipPath>
            <style>
                .logo-horizontal_svg__fil1 {
                    fill: #2b4b60;
                    fill-rule: nonzero;
                }
            </style>
        </defs>
        <g id="logo-horizontal_svg__Camada_x0020_1">
            <g clip-path="url(#logo-horizontal_svg__id0)">
                <g id="logo-horizontal_svg__MarcaOficial_Tirrell_eps">
                    <path d="M5244.6 117.51c-138.19-70.64-305.76-47.61-458.97 63.2l-1008.29 730c-156.09-71.1-344.21-58.81-492.8 48.35-219.78 159.43-269.23 466.82-110.23 686.86 159.25 219.99 466.9 269.28 687.14 110.07 148.48-107.7 218.89-282.69 200.03-453.02l916.69-663.91v3647.76c0 119.23-95.45 303.89-192.53 372.93L2934.02 5974.9c-78.93 56.02-234.11 56.83-313.24 1.47L728.23 4661.77c-96.52-67.66-192.35-250.16-192.35-368.64V621.17l1697.9 1148.25c97.7 66.12 193.04 245.89 193.04 363.2v1374.22c-148.82 84.59-249.51 244.24-249.51 427.66 0 271.46 220.04 491.73 491.42 491.73 271.71 0 491.79-220.27 491.79-491.73 0-183.42-100.76-343.07-249.55-427.66V2132.62c0-279.23-174.35-607.98-405.52-764.3L728.25 166.83C573.23 61.89 405.66 43.38 268.19 116.42 130.12 189.62 51.45 339.03 51.45 526.31v3766.83c0 278.11 172.2 607.43 400.58 766.36l1892.3 1314.8c123.33 85.54 277.44 128.56 431.51 128.56 156.79 0 313.47-44.47 438.41-132.87L5066.3 5054.73c226.18-160.52 396.23-490.7 396.23-767.89V526.32c0-189.23-79.15-338.09-217.89-408.8z" fill="#0a98b1" fill-rule="nonzero"></path>
                    <path style="fill: #2b4b60" d="M19968.53 4395.04h-81.75c-3.51 0-7.35-.55-11.25-.55h-1117.48V1962.81c0-5.95-.15-11.86-.46-17.59v-78.29c0-53.99-43.68-97.63-97.43-97.63h-191.14c-53.87 0-97.31 43.64-97.31 97.63v2703.84c0 108.68 84.51 193.59 193.34 193.59h1403.48c55.35 0 99.96-44.73 99.96-100.16v-169.31c0-54.97-44.61-99.85-99.96-99.85zM22228 4395.04h-73.17c-4.05 0-7.78-.55-11.67-.55h-1117.29V1962.81c0-6.38-.11-12.92-.69-19.29v-76.58c0-53.99-43.76-97.63-97.2-97.63h-191.33c-53.56 0-97.32 43.64-97.32 97.63v2703.84c0 108.68 84.95 193.59 193.23 193.59h1395.43c55.3 0 99.96-44.73 99.96-100.16V4494.9c0-54.97-44.65-99.85-99.96-99.85zM10087.17 1867.16c0-54.22-43.88-97.86-98.26-97.86h-191.13c-54.07 0-97.4 43.64-97.4 97.86v2833.26c0 54.06 43.33 97.9 97.4 97.9h191.13c54.38 0 98.26-43.84 98.26-97.9V1867.16zM9038.26 1803.41H7059.78c-54.96 0-99.45 44.76-99.45 100.19v169.24c0 55.54 44.49 100.16 99.45 100.16h798.03v2527.42c0 54.06 43.36 97.76 97.74 97.76h191.53c53.71 0 97.7-43.71 97.7-97.76V2173h793.48c55.19 0 99.8-44.62 99.8-100.16V1903.6c0-55.43-44.61-100.19-99.8-100.19zM17643.69 4402.86H16341.5v-949.27h779.28l.15.15h191.71c53.84 0 97.59-43.56 97.59-97.83v-165.6c0-53.96-43.75-97.42-97.59-97.42h-971.14v-928.18h1172.32c2.8 0 5.56-.31 8.43-.46h76.75c53.6 0 97.43-43.68 97.43-97.82v-165.46c0-53.96-43.84-97.55-97.43-97.55h-1451.01c-108.09 0-193.23 85.06-193.23 193.59v2573.77c0 108.68 85.14 193.59 193.23 193.59h1495.7c54.26 0 97.4-44.04 97.4-97.97v-165.78c0-54.1-43.14-97.74-97.4-97.74zM15267 4406.31c-.55-1.16-1.55-1.85-1.91-2.4l.08-.54-663.84-885.83c421.52-60.53 718.99-406.05 718.99-852.79 0-491.01-370.44-861.34-861.31-861.34h-846.8c-108.51 0-193.36 84.79-193.36 193.47v2703.76c0 53.84 43.61 97.54 97.52 97.54h191.13c54.5 0 97.82-43.71 97.82-97.54v-1174.7h356.37l848.17 1182.53v-.24l41.5 57.1c31.9 43.73 92.65 53.53 136.21 22.06l155.58-112.35c43.45-31.92 52.98-92.73 21.59-136.43l-97.74-132.3zm-1461.67-1241.26V2164.63h649.1c275.46 0 474.68 210.24 474.68 500.12 0 285.11-198.6 500.3-461.54 500.3h-662.24zM12731.18 4406.31c-.39-1.16-1.08-1.85-2.14-2.4l.28-.54-664.34-885.83c422.09-60.53 719.22-406.05 719.22-852.79 0-491.01-370.17-861.34-861.04-861.34h-846.57c-109.02 0-193.74 84.79-193.74 193.47v2703.76c0 53.84 44.11 97.54 97.68 97.54h191.68c53.98 0 97.74-43.71 97.74-97.54v-1174.7h355.82l792.54 1105.24s.69 0 .69.28l4.48 6.68 50.79 70.33v-.24l41.42 57.1c31.36 43.73 92.26 53.53 136.14 22.06l154.84-112.35c43.91-31.92 53.64-92.73 22.05-136.43l-97.55-132.3zm-1461.23-1241.26V2164.63h648.9c274.71 0 474.53 210.24 474.53 500.12 0 285.11-198.45 500.3-461.59 500.3h-661.84z" class="logo-horizontal_svg__fil1"></path>
                </g>
            </g>
            <path fill="none" stroke-width="22.05" stroke-miterlimit="22.926" d="M11.03 11.03h22357.32V6564.2H11.03z"></path>
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# ===== BOTÃO HOME =====

if st.sidebar.button("Home", use_container_width=True, type="secondary" if st.session_state.view_mode != 'home' else "primary"):
    st.session_state.view_mode = 'home'
    st.rerun()


st.sidebar.markdown("### Análises")


if st.sidebar.button("Comparativo       ", use_container_width=True, type="secondary" if st.session_state.view_mode != 'qualitativa' else "primary"):
    st.session_state.view_mode = 'qualitativa'
    st.rerun()

if st.sidebar.button("Visão Geral", use_container_width=True, type="secondary" if st.session_state.view_mode != 'visao_geral' else "primary"):
    st.session_state.view_mode = 'visao_geral'
    st.rerun()

if st.sidebar.button("Cards por Empresa", use_container_width=True, type="secondary" if st.session_state.view_mode != 'empresas' else "primary"):
    st.session_state.view_mode = 'empresas'
    st.rerun()

if st.sidebar.button("Gaps e Oportunidades", use_container_width=True, type="secondary" if st.session_state.view_mode != 'gaps' else "primary"):
    st.session_state.view_mode = 'gaps'
    st.rerun()

if st.sidebar.button("Tabela Completa", use_container_width=True, type="secondary" if st.session_state.view_mode != 'tabela' else "primary"):
    st.session_state.view_mode = 'tabela'
    st.rerun()

# ===== FILTROS NO INÍCIO DA PÁGINA =====
if st.session_state.view_mode != 'home':
    with st.expander("⚙️ Filtros de Análise", expanded=False):
        st.markdown("""
        <style>
        .filtros-container {
            max-height: 200px;
            overflow-y: auto;
            padding: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

        col_filtros1, col_filtros2 = st.columns(2)

        with col_filtros1:
            st.markdown('<div class="filtros-container">', unsafe_allow_html=True)
            st.markdown("**📁 Categorias**")
            categorias = sorted(df["Categoria"].unique().tolist())

            # Opção para selecionar/desselecionar todas
            select_all_cat = st.checkbox("Selecionar todas as categorias", value=True, key="select_all_cat")

            if select_all_cat:
                cat_sel = categorias
            else:
                cat_sel = []
                for cat in categorias:
                    if st.checkbox(cat, value=False, key=f"cat_{cat}"):
                        cat_sel.append(cat)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_filtros2:
            st.markdown("**🏢 Empresas**")
            empresas = sorted(df["Empresa"].unique().tolist())

            # TIRRELL sempre selecionada
            emp_sel = [tirrell_name]  # TIRRELL sempre incluída
            st.checkbox(f"{tirrell_name} (sua empresa)", value=True, disabled=True, key="emp_tirrell_filter")

            # Outras empresas em grid/colunas
            outras_empresas = [e for e in empresas if e != tirrell_name]

            if outras_empresas:
                # Criar colunas para empresas (2 por linha)
                num_cols = 2
                for i in range(0, len(outras_empresas), num_cols):
                    cols_emp = st.columns(num_cols)
                    for j, emp in enumerate(outras_empresas[i:i+num_cols]):
                        with cols_emp[j]:
                            if st.checkbox(emp, value=True, key=f"emp_{emp}"):
                                emp_sel.append(emp)
else:
    # Na home, usar todos os filtros por padrão
    categorias = sorted(df["Categoria"].unique().tolist())
    cat_sel = categorias
    empresas = sorted(df["Empresa"].unique().tolist())
    emp_sel = empresas

# Validar seleções
if not cat_sel:
    st.warning("⚠️ Selecione pelo menos uma categoria nos filtros")
    st.stop()
if not emp_sel:
    st.warning("⚠️ Selecione pelo menos uma empresa nos filtros")
    st.stop()

# Filtrar dados
df_filtered = df[
    (df["Categoria"].isin(cat_sel)) &
    (df["Empresa"].isin(emp_sel))
].copy()

# ===== TIRRELL VS CONCORRENTES (ANÁLISE QUALITATIVA) =====
if st.session_state.view_mode == 'qualitativa':
    st.header("🎯 Comparativo - Tirrell vs Concorrentes")
    st.caption("Comparação detalhada por categoria mostrando quais documentos cada empresa tipifica")

    if tirrell_name not in emp_sel:
        st.warning("⚠️ Empresa principal (Tirrell) não encontrada nos dados filtrados")
        st.stop()

    # Obter outros concorrentes
    concorrentes = [e for e in emp_sel if e != tirrell_name]

    if not concorrentes:
        st.info("Adicione outras empresas nos filtros para comparar com a Tirrell")
        st.stop()

    # Comparar Tirrell com cada concorrente
    for concorrente in concorrentes:
        with st.expander(f"📊 {tirrell_name} vs {concorrente}", expanded=False):
            # Para cada categoria, criar tabela comparativa
            for cat in cat_sel:
                st.markdown(f"### {cat}")

                # Filtrar dados da categoria para ambas empresas
                cat_data = df_filtered[df_filtered['Categoria'] == cat]

                # Documentos que pelo menos UMA das duas empresas tipifica
                docs_tirrell_cat = set(cat_data[
                    (cat_data['Empresa'] == tirrell_name) &
                    (cat_data['Suporte (✅/❌)'] == '✅')
                ]['Tipo de Documento'])

                docs_concorrente_cat = set(cat_data[
                    (cat_data['Empresa'] == concorrente) &
                    (cat_data['Suporte (✅/❌)'] == '✅')
                ]['Tipo de Documento'])

                # União: documentos que pelo menos uma empresa faz
                docs_relevantes = sorted(docs_tirrell_cat | docs_concorrente_cat)

                if not docs_relevantes:
                    st.info(f"Nenhuma das empresas tipifica documentos {cat}")
                    continue

                # Criar tabela comparativa
                tabela_comp = []
                for doc in docs_relevantes:
                    tabela_comp.append({
                        'Tipo de Documento': doc,
                        tirrell_name: '✅' if doc in docs_tirrell_cat else '❌',
                        concorrente: '✅' if doc in docs_concorrente_cat else '❌'
                    })

                df_comp = pd.DataFrame(tabela_comp)

                # Estatísticas rápidas
                # Total de documentos da categoria no mercado (da aba de referência)
                total_docs_mercado = len(categorias_ref.get(cat, []))
                tirrell_count = len(docs_tirrell_cat)
                concorrente_count = len(docs_concorrente_cat)
                vantagens_count = len(docs_tirrell_cat - docs_concorrente_cat)
                lacunas_count = len(docs_concorrente_cat - docs_tirrell_cat)

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("📊 Total Mercado", total_docs_mercado)
                with col2:
                    st.metric(f"✅ {tirrell_name}", tirrell_count)
                with col3:
                    st.metric(f"✅ {concorrente}", concorrente_count)
                with col4:
                    st.metric("🏆 Vantagens", vantagens_count)
                with col5:
                    st.metric("⚠️ Lacunas", lacunas_count)

                # Exibir tabela com cores
                def highlight_comparison(row):
                    colors = []
                    for col_name in row.index:
                        if col_name == 'Tipo de Documento':
                            colors.append('background-color: #f3f4f6')
                        else:
                            valor = row[col_name]
                            if valor == '✅':
                                colors.append('background-color: #bbf7d0')
                            elif valor == '❌':
                                colors.append('background-color: #fecaca')
                            else:
                                colors.append('background-color: #f3f4f6')
                    return colors

                st.dataframe(
                    df_comp.style.apply(highlight_comparison, axis=1),
                    use_container_width=True,
                    hide_index=True
                )

# ===== VISÃO GERAL POR CATEGORIA =====
if st.session_state.view_mode == 'visao_geral':
    st.header("Visão Geral - Desempenho por Categoria")

    # Criar matriz de comparação
    comp_df = create_category_comparison(df_filtered, cat_sel, emp_sel)

    # Métricas da Tirrell por categoria
    if tirrell_name in emp_sel:
        st.subheader(f"🎯 Desempenho {tirrell_name}")

        tirrell_data = comp_df[comp_df["Empresa"] == tirrell_name]

        cols = st.columns(len(cat_sel))
        for idx, cat in enumerate(cat_sel):
            cat_stats = tirrell_data[tirrell_data["Categoria"] == cat].iloc[0] if not tirrell_data[tirrell_data["Categoria"] == cat].empty else None

            with cols[idx]:
                if cat_stats is not None:
                    st.metric(
                        cat,
                        f"{cat_stats['% Tipificação']}%",
                        f"{cat_stats['Tipificados']}/{cat_stats['Total Docs']}"
                    )

    st.markdown("---")

    # Ranking por categoria
    st.subheader("Ranking por Categoria")

    for cat in cat_sel:
        cat_data = comp_df[comp_df["Categoria"] == cat].sort_values("% Tipificação", ascending=False)

        with st.expander(f"{cat}"):
            # Destacar Tirrell
            def highlight_tirrell(row):
                if row["Empresa"] == tirrell_name:
                    return ['background-color: #e0f2fe'] * len(row)
                return [''] * len(row)

            st.dataframe(
                cat_data.style.apply(highlight_tirrell, axis=1),
                use_container_width=True
            )

    # Heatmap de tipificação por categoria
    st.markdown("---")
    st.subheader("Heatmap de Tipificação por Categoria")

    pivot = comp_df.pivot_table(
        index="Empresa",
        columns="Categoria",
        values="% Tipificação",
        aggfunc="first"
    )

    plot_df = pivot.reset_index().melt(id_vars="Empresa", var_name="Categoria", value_name="Tipificação %")

    chart = alt.Chart(plot_df).mark_rect().encode(
        x=alt.X('Categoria:N'),
        y=alt.Y('Empresa:N', sort='-x', axis=alt.Axis(labelLimit=200)),
        color=alt.Color('Tipificação %:Q',
                       scale=alt.Scale(scheme='blues'),
                       legend=alt.Legend(title="Tipificação %")),
        tooltip=["Empresa", "Categoria", alt.Tooltip("Tipificação %", format=".1f")]
    ).properties(height=max(400, len(pivot) * 50))

    st.altair_chart(chart, use_container_width=True)


# ===== CARDS POR EMPRESA =====
if st.session_state.view_mode == 'empresas':
    st.header("🏢 Análise Detalhada por Empresa")
    st.caption("Desempenho de cada empresa agrupado por categoria")

    # Ordenar empresas: TIRRELL primeiro, depois as outras em ordem alfabética
    empresas_ordenadas = [tirrell_name] + sorted([e for e in emp_sel if e != tirrell_name])

    for emp in empresas_ordenadas:
        emp_data = df_filtered[df_filtered["Empresa"] == emp]

        # Card da empresa
        is_tirrell = emp == tirrell_name
        emoji = "🎯" if is_tirrell else "🏢"

        with st.expander(f"{emoji} {emp}" + (" (Principal)" if is_tirrell else ""), expanded=is_tirrell):

            # Métricas gerais
            total_tipificado = emp_data[emp_data["score"] == 2]["Tipo de Documento"].nunique()
            total_gaps = emp_data[emp_data["score"] == 0]["Tipo de Documento"].nunique()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Tipificados", total_tipificado)
            with col2:
                st.metric("❌ Lacunas", total_gaps)

            st.markdown("---")

            # Análise por categoria
            for cat in cat_sel:
                cat_data = emp_data[emp_data["Categoria"] == cat]

                if cat_data.empty:
                    continue

                st.markdown(f"#### 📁 {cat}")

                # Métricas da categoria
                cat_total = (cat_data["score"] == 2).sum()
                cat_gaps = (cat_data["score"] == 0).sum()
                cat_coverage = round(cat_total / len(cat_data) * 100, 1) if len(cat_data) > 0 else 0

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("% Tipificação", f"{cat_coverage}%")
                with col2:
                    st.metric("✅", cat_total)
                with col3:
                    st.metric("❌", cat_gaps)

                # Lista de documentos
                doc_list = cat_data[["Tipo de Documento", "Suporte (✅/❌)", "Tecnologia (tags)", "Observações"]].copy()
                doc_list = doc_list.rename(columns={"Suporte (✅/❌)": "Status"})

                # Aplicar cores por status
                def color_status(row):
                    colors = []
                    for col in row.index:
                        if col == "Status":
                            if row[col] == "✅":
                                colors.append('background-color: #bbf7d0')
                            elif row[col] == "❌":
                                colors.append('background-color: #fecaca')
                            else:
                                colors.append('background-color: #f3f4f6')
                        else:
                            colors.append('background-color: #f3f4f6')
                    return colors

                st.dataframe(
                    doc_list.style.apply(color_status, axis=1),
                    use_container_width=True
                )

                st.markdown("")

# ===== GAPS POR CATEGORIA =====
if st.session_state.view_mode == 'gaps':
    st.header("🎯 Gaps e Oportunidades por Categoria")

    if tirrell_name not in emp_sel:
        st.warning("Tirrell não encontrada nos dados filtrados")
        st.stop()

    st.subheader(f"Análise de Gaps - {tirrell_name}")

    for cat in cat_sel:
        st.markdown(f"### 📁 {cat}")

        cat_data = df_filtered[df_filtered["Categoria"] == cat]

        # Documentos que Tirrell NÃO faz
        tirrell_gaps = cat_data[
            (cat_data["Empresa"] == tirrell_name) &
            (cat_data["score"] == 0)
        ]["Tipo de Documento"].unique()

        # Documentos que Tirrell faz mas concorrentes não
        tirrell_vantagens = []
        for doc in cat_data[(cat_data["Empresa"] == tirrell_name) & (cat_data["score"] >= 1)]["Tipo de Documento"].unique():
            outros = cat_data[(cat_data["Tipo de Documento"] == doc) & (cat_data["Empresa"] != tirrell_name) & (cat_data["score"] >= 1)]
            if outros.empty:
                tirrell_vantagens.append(doc)

        col1, col2 = st.columns(2)

        with col1:
            st.error(f"#### ⚠️ Gaps ({len(tirrell_gaps)} documentos)")

            if len(tirrell_gaps) > 0:
                gaps_details = []
                for doc in tirrell_gaps:
                    concorrentes = cat_data[
                        (cat_data["Tipo de Documento"] == doc) &
                        (cat_data["Empresa"] != tirrell_name) &
                        (cat_data["score"] >= 1)
                    ]
                    n_conc = concorrentes["Empresa"].nunique()
                    gaps_details.append({
                        "Documento": doc,
                        "Concorrentes fazem": n_conc
                    })

                gaps_df = pd.DataFrame(gaps_details).sort_values("Concorrentes fazem", ascending=False)
                st.dataframe(gaps_df, use_container_width=True)
            else:
                st.success("✅ Tipificação completa nesta categoria!")

        with col2:
            st.success(f"#### 🏆 Vantagens ({len(tirrell_vantagens)} documentos)")

            if len(tirrell_vantagens) > 0:
                for doc in tirrell_vantagens:
                    st.write(f"• {doc}")
            else:
                st.info("Sem documentos exclusivos nesta categoria")

        st.markdown("---")

# ===== TABELA COMPLETA =====
if st.session_state.view_mode == 'tabela':
    st.header("📋 Tabela Completa")

    # Tabela por categoria
    for cat in cat_sel:
        with st.expander(f"📁 {cat}"):
            cat_data = df_filtered[df_filtered["Categoria"] == cat]
            st.dataframe(cat_data, use_container_width=True)

    st.markdown("---")

    # Estatísticas gerais
    st.subheader("📊 Estatísticas Gerais")

    comp_df = create_category_comparison(df_filtered, cat_sel, emp_sel)
    st.dataframe(comp_df, use_container_width=True)

st.markdown("---")
st.caption("💡 Análise baseada em categoria_doc.csv como referência de mercado | Categorias organizam os documentos por tipo de informação")
