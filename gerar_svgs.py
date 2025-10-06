"""
Script para gerar gráficos SVG de ranking por categoria
EXATAMENTE como está no app Streamlit - estilo tabela com gradient Blues
"""

import pandas as pd
import unicodedata
import re
from pathlib import Path

def normalize_header(s: str) -> str:
    """Normaliza nomes de categorias"""
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode('ascii')
    s = re.sub(r'\s+', ' ', s.strip()).upper()

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
    """Carrega dados do Excel"""
    excel_file = pd.ExcelFile(excel_path)

    # Primeira aba = referência
    primeira_aba = excel_file.sheet_names[0]
    df_ref = pd.read_excel(excel_path, sheet_name=primeira_aba)

    categorias_ref = {}
    for col in df_ref.columns:
        docs = df_ref[col].dropna().tolist()
        docs = [d.strip() for d in docs if d and str(d).strip()]
        if docs:
            categorias_ref[col] = docs

    # Demais abas = empresas
    empresas_docs = {}

    for sheet_name in excel_file.sheet_names[1:]:
        empresa_name = sheet_name.strip()
        df_empresa = pd.read_excel(excel_path, sheet_name=sheet_name)

        empresas_docs[empresa_name] = {}

        for col in df_empresa.columns:
            categoria_normalizada = normalize_header(col)
            docs = df_empresa[col].dropna().tolist()
            docs = [d.strip() for d in docs if d and str(d).strip()]
            empresas_docs[empresa_name][categoria_normalizada] = set(docs)

    return categorias_ref, empresas_docs

def get_blues_gradient_color(pct):
    """
    Retorna cor do gradiente Blues (igual ao app Streamlit)
    Baseado no matplotlib colormap 'Blues'
    """
    if pct >= 90:
        return '#08519c'  # Azul muito escuro
    elif pct >= 80:
        return '#2171b5'  # Azul escuro
    elif pct >= 70:
        return '#4292c6'  # Azul médio-escuro
    elif pct >= 60:
        return '#6baed6'  # Azul médio
    elif pct >= 50:
        return '#9ecae1'  # Azul médio-claro
    elif pct >= 40:
        return '#c6dbef'  # Azul claro
    elif pct >= 30:
        return '#deebf7'  # Azul muito claro
    else:
        return '#f7fbff'  # Quase branco

def gerar_svg_ranking(categoria, categorias_ref, empresas_docs, output_path):
    """Gera SVG de ranking EXATAMENTE como a tabela do app"""

    cat_normalizada = normalize_header(categoria)
    docs_mercado = categorias_ref[categoria]
    total_docs = len(docs_mercado)

    # Calcular tipificação de cada empresa
    empresas_stats = []

    for empresa in sorted(empresas_docs.keys()):
        docs_empresa = empresas_docs[empresa].get(cat_normalizada, set())
        tipificados = len(docs_empresa)
        percentual = round((tipificados / total_docs * 100), 1) if total_docs > 0 else 0

        empresas_stats.append({
            'empresa': empresa,
            'tipificados': tipificados,
            'total': total_docs,
            'percentual': percentual
        })

    # Ordenar por percentual (decrescente) - igual ao app
    empresas_stats.sort(key=lambda x: x['percentual'], reverse=True)

    if not empresas_stats:
        return

    # Configurações do SVG - Tabela estilo dataframe
    row_height = 36
    header_height = 40
    width = 650
    height = header_height + (len(empresas_stats) * row_height) + 5

    # Larguras das colunas
    col_empresa = 200
    col_total = 120
    col_tipif = 120
    col_pct = 210

    # Cores EXATAS do app
    bg_header = '#374151'
    text_header = '#f9fafb'
    bg_tirrell = '#e0f2fe'  # Destaque TIRRELL
    bg_even = '#ffffff'
    bg_odd = '#f9fafb'
    border_color = '#e5e7eb'
    text_color = '#374151'

    # Iniciar SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">

    <!-- Background -->
    <rect width="{width}" height="{height}" fill="#ffffff"/>

    <!-- Título da Categoria -->
    <text x="{width/2}" y="25" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="{text_color}" text-anchor="middle">
        {categoria}
    </text>

    <!-- Header da Tabela -->
    <!-- Coluna: Empresa -->
    <rect x="0" y="{header_height}" width="{col_empresa}" height="{row_height}" fill="{bg_header}" stroke="{border_color}" stroke-width="1"/>
    <text x="{col_empresa/2}" y="{header_height + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="{text_header}" text-anchor="middle">Empresa</text>

    <!-- Coluna: Total Docs -->
    <rect x="{col_empresa}" y="{header_height}" width="{col_total}" height="{row_height}" fill="{bg_header}" stroke="{border_color}" stroke-width="1"/>
    <text x="{col_empresa + col_total/2}" y="{header_height + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="{text_header}" text-anchor="middle">Total Docs</text>

    <!-- Coluna: Tipificados -->
    <rect x="{col_empresa + col_total}" y="{header_height}" width="{col_tipif}" height="{row_height}" fill="{bg_header}" stroke="{border_color}" stroke-width="1"/>
    <text x="{col_empresa + col_total + col_tipif/2}" y="{header_height + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="{text_header}" text-anchor="middle">Tipificados</text>

    <!-- Coluna: % Tipificação -->
    <rect x="{col_empresa + col_total + col_tipif}" y="{header_height}" width="{col_pct}" height="{row_height}" fill="{bg_header}" stroke="{border_color}" stroke-width="1"/>
    <text x="{col_empresa + col_total + col_tipif + col_pct/2}" y="{header_height + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="{text_header}" text-anchor="middle">% Tipificação</text>

'''

    # Linhas de dados
    for idx, stats in enumerate(empresas_stats):
        y = header_height + row_height + (idx * row_height)

        # Determinar cor de fundo da linha
        is_tirrell = stats['empresa'] == 'TIRRELL'
        if is_tirrell:
            row_bg = bg_tirrell
        else:
            row_bg = bg_even if idx % 2 == 0 else bg_odd

        # Cor do gradiente para % Tipificação
        pct_bg = get_blues_gradient_color(stats['percentual'])
        # Texto branco se fundo escuro, senão texto normal
        pct_text = '#ffffff' if stats['percentual'] >= 50 else text_color

        # Coluna: Empresa
        svg += f'''    <!-- Linha {idx + 1}: {stats['empresa']} -->
    <rect x="0" y="{y}" width="{col_empresa}" height="{row_height}" fill="{row_bg}" stroke="{border_color}" stroke-width="0.5"/>
    <text x="8" y="{y + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="{text_color}" text-anchor="start">{stats['empresa']}</text>

'''

        # Coluna: Total Docs
        svg += f'''    <rect x="{col_empresa}" y="{y}" width="{col_total}" height="{row_height}" fill="{row_bg}" stroke="{border_color}" stroke-width="0.5"/>
    <text x="{col_empresa + col_total/2}" y="{y + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="{text_color}" text-anchor="middle">{stats['total']}</text>

'''

        # Coluna: Tipificados
        svg += f'''    <rect x="{col_empresa + col_total}" y="{y}" width="{col_tipif}" height="{row_height}" fill="{row_bg}" stroke="{border_color}" stroke-width="0.5"/>
    <text x="{col_empresa + col_total + col_tipif/2}" y="{y + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="{text_color}" text-anchor="middle">{stats['tipificados']}</text>

'''

        # Coluna: % Tipificação (com gradient Blues)
        svg += f'''    <rect x="{col_empresa + col_total + col_tipif}" y="{y}" width="{col_pct}" height="{row_height}" fill="{pct_bg}" stroke="{border_color}" stroke-width="0.5"/>
    <text x="{col_empresa + col_total + col_tipif + col_pct/2}" y="{y + row_height/2 + 5}" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="bold" fill="{pct_text}" text-anchor="middle">{stats['percentual']}%</text>

'''

    svg += '</svg>'

    # Salvar arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"✅ SVG gerado: {output_path}")

def gerar_todos_svgs():
    """Gera SVGs de ranking para todas as categorias"""

    print("Carregando dados do Excel...")
    categorias_ref, empresas_docs = load_excel_data('data/Pesquisa de mercado - Tipificação.xlsx')

    # Criar pasta svg se não existir
    svg_dir = Path('svg')
    svg_dir.mkdir(exist_ok=True)

    print(f"\nGerando SVGs de ranking (estilo app) para {len(categorias_ref)} categorias...\n")

    for categoria in categorias_ref.keys():
        # Nome do arquivo (normalizado)
        filename = categoria.lower().replace(' ', '_').replace('í', 'i').replace('ó', 'o').replace('á', 'a')
        output_path = svg_dir / f"ranking_{filename}.svg"

        gerar_svg_ranking(categoria, categorias_ref, empresas_docs, output_path)

    print(f"\n✅ {len(categorias_ref)} SVGs gerados com sucesso na pasta 'svg/'!")
    print("Os SVGs estão no formato de tabela EXATAMENTE como no app Streamlit")

if __name__ == '__main__':
    gerar_todos_svgs()
