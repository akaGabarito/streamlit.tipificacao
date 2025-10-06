"""
Script para gerar PDF de apresentação do Benchmarking de Tipificação de Documentos
Com design profissional e fiel ao app Streamlit
"""

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import unicodedata
import re

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

class NumberedCanvas(canvas.Canvas):
    """Canvas customizado com rodapé e numeração"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor('#6b7280'))

        # Rodapé esquerdo
        self.drawString(30*mm, 15*mm, f"Benchmarking de Tipificação • {datetime.now().strftime('%d/%m/%Y')}")

        # Rodapé direito - numeração
        page_num = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 30*mm, 15*mm, page_num)

def gerar_pdf(output_path='Benchmarking_Tipificacao.pdf'):
    """Gera PDF de apresentação com design profissional"""

    # Criar documento
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=25*mm,
        bottomMargin=25*mm
    )

    # Estilos customizados baseados no app
    styles = getSampleStyleSheet()

    # Título principal (capa)
    title_cover = ParagraphStyle(
        'TitleCover',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#111827'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=38
    )

    # Subtítulo (capa)
    subtitle_cover = ParagraphStyle(
        'SubtitleCover',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=20
    )

    # Caption (capa)
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    # Título de seção (h2)
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=colors.HexColor('#374151'),
        spaceAfter=16,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        leading=24
    )

    # Subtítulo de seção (h3)
    subsection_title = ParagraphStyle(
        'SubsectionTitle',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=10,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    # Texto normal
    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=6,
        fontName='Helvetica',
        leading=14
    )

    # Carregar dados
    print("Carregando dados do Excel...")
    categorias_ref, empresas_docs = load_excel_data('data/Pesquisa de mercado - Tipificação.xlsx')

    # Elementos do PDF
    elements = []

    # === PÁGINA 1: CAPA ===
    elements.append(Spacer(1, 80*mm))
    elements.append(Paragraph("Benchmarking de Tipificação de Documentos", title_cover))
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph("Analisamos a tipificação de documentos ofertada no mercado de onboarding para entender o espaço de mercado da Tirrell.", subtitle_cover))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph("Separamos a tipificação por categorias para facilitar a comparação.", caption_style))
    elements.append(Spacer(1, 20*mm))
    elements.append(Paragraph(f"Gerado em {datetime.now().strftime('%d de %B de %Y')}", caption_style))
    elements.append(PageBreak())

    # === PÁGINA 2: UNIVERSO DE DOCUMENTOS DO MERCADO ===
    elements.append(Paragraph("Universo de Documentos do Mercado", section_title))
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph("Catálogo completo de tipos de documentos analisados no mercado de onboarding, organizados por categoria.", normal_text))
    elements.append(Spacer(1, 10*mm))

    # Estatísticas gerais
    total_docs_mercado = sum(len(docs) for docs in categorias_ref.values())
    total_categorias = len(categorias_ref)

    summary_text = f"<b>Total de Categorias:</b> {total_categorias} | <b>Total de Documentos:</b> {total_docs_mercado}"
    elements.append(Paragraph(summary_text, normal_text))
    elements.append(Spacer(1, 8*mm))

    # Tabela: Categoria e documentos
    data_universo = [['Categoria', 'Quantidade', 'Documentos']]

    for categoria, docs_lista in categorias_ref.items():
        docs_text = ', '.join(sorted(docs_lista))
        data_universo.append([
            categoria,
            str(len(docs_lista)),
            docs_text
        ])

    table_universo = Table(data_universo, colWidths=[35*mm, 25*mm, 100*mm])
    table_universo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
    ]))

    elements.append(table_universo)
    elements.append(Spacer(1, 10*mm))

    # Gráfico de distribuição (tabela visual)
    elements.append(Paragraph("Distribuição de Documentos por Categoria", subsection_title))
    elements.append(Spacer(1, 6*mm))

    data_dist = [['Categoria', 'Quantidade', '% do Total', 'Visualização']]

    for categoria, docs_lista in categorias_ref.items():
        qtd = len(docs_lista)
        pct = round((qtd / total_docs_mercado * 100), 1)
        # Criar barra visual proporcional
        bar_width = int((qtd / total_docs_mercado) * 100)  # Porcentagem para largura visual
        visual_bar = '█' * max(1, bar_width // 5)  # Cada █ representa ~5%

        data_dist.append([
            categoria,
            str(qtd),
            f"{pct}%",
            visual_bar
        ])

    table_dist = Table(data_dist, colWidths=[35*mm, 25*mm, 25*mm, 75*mm])
    table_dist.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor('#1e3a8a')),
    ]))

    elements.append(table_dist)
    elements.append(PageBreak())

    # === PÁGINA 3: VISÃO GERAL ===
    elements.append(Paragraph("Visão Geral - Desempenho por Categoria", section_title))
    elements.append(Spacer(1, 8*mm))

    # Preparar dados agregados por categoria
    total_mercado = sum(len(docs) for docs in categorias_ref.values())

    # Tabela: Empresa x Categoria
    empresas_list = sorted(empresas_docs.keys())
    categorias_list = list(categorias_ref.keys())

    # Criar tabela de comparação
    data_overview = [['Empresa'] + categorias_list + ['% Tipificação Total']]

    for empresa in empresas_list:
        row = [empresa]
        total_tipificados = 0
        for cat in categorias_list:
            cat_normalizada = normalize_header(cat)
            docs_mercado = categorias_ref[cat]
            docs_empresa = empresas_docs[empresa].get(cat_normalizada, set())
            tipificados = len(docs_empresa)
            total_docs_cat = len(docs_mercado)
            pct = round((tipificados / total_docs_cat * 100), 1) if total_docs_cat > 0 else 0
            row.append(f"{tipificados}/{total_docs_cat}\n({pct}%)")
            total_tipificados += tipificados

        pct_total = round((total_tipificados / total_mercado * 100), 1) if total_mercado > 0 else 0
        row.append(f"{pct_total}%")
        data_overview.append(row)

    # Calcular larguras das colunas
    col_widths = [35*mm] + [25*mm] * len(categorias_list) + [25*mm]

    table_overview = Table(data_overview, colWidths=col_widths)
    table_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))

    elements.append(table_overview)
    elements.append(PageBreak())

    # === RANKING POR CATEGORIA (SVGs) ===
    elements.append(Paragraph("Ranking por Categoria", section_title))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph("Visualização do desempenho das empresas em cada categoria, ordenadas por % de tipificação.", normal_text))
    elements.append(Spacer(1, 8*mm))

    # Importar SVGs gerados
    import os
    from pathlib import Path

    svg_dir = Path('svg')

    for categoria in categorias_ref.keys():
        # Nome do arquivo SVG
        filename = categoria.lower().replace(' ', '_').replace('í', 'i').replace('ó', 'o').replace('á', 'a')
        svg_path = svg_dir / f"ranking_{filename}.svg"

        if svg_path.exists():
            try:
                # Converter SVG para ReportLab Drawing
                drawing = svg2rlg(str(svg_path))

                if drawing:
                    # Escalar se necessário para caber na página
                    scale_factor = min(1.0, (A4[0] - 50*mm) / drawing.width)
                    drawing.width *= scale_factor
                    drawing.height *= scale_factor
                    drawing.scale(scale_factor, scale_factor)

                    elements.append(drawing)
                    elements.append(Spacer(1, 8*mm))
            except Exception as e:
                print(f"⚠️ Erro ao incluir SVG {svg_path}: {e}")
                # Fallback: adicionar texto
                elements.append(Paragraph(f"Ranking: {categoria} (gráfico não disponível)", subsection_title))
                elements.append(Spacer(1, 8*mm))

    elements.append(PageBreak())

    # === ANÁLISE QUALITATIVA: TIRRELL VS CONCORRENTES ===
    if 'TIRRELL' in empresas_docs:
        elements.append(Paragraph("Análise Qualitativa - Tirrell vs Concorrentes", section_title))
        elements.append(Spacer(1, 4*mm))
        elements.append(Paragraph("Comparação detalhada por categoria mostrando quais documentos cada empresa tipifica", normal_text))
        elements.append(Spacer(1, 8*mm))

        tirrell_name = 'TIRRELL'
        concorrentes = [e for e in sorted(empresas_docs.keys()) if e != tirrell_name]

        # Para cada concorrente
        for concorrente in concorrentes:
            elements.append(Paragraph(f"{tirrell_name} vs {concorrente}", subsection_title))
            elements.append(Spacer(1, 4*mm))

            # Para cada categoria
            for categoria, docs_mercado in categorias_ref.items():
                cat_normalizada = normalize_header(categoria)

                # Documentos das empresas nesta categoria
                docs_tirrell = empresas_docs[tirrell_name].get(cat_normalizada, set())
                docs_concorrente_set = empresas_docs[concorrente].get(cat_normalizada, set())

                # Documentos relevantes (união)
                docs_relevantes = sorted(docs_tirrell | docs_concorrente_set)

                if not docs_relevantes:
                    continue

                # Cabeçalho da categoria
                cat_header = Paragraph(f"<b>{categoria}</b>", normal_text)
                elements.append(cat_header)
                elements.append(Spacer(1, 2*mm))

                # Métricas
                total_docs_mercado = len(docs_mercado)
                tirrell_count = len(docs_tirrell)
                concorrente_count = len(docs_concorrente_set)
                vantagens_count = len(docs_tirrell - docs_concorrente_set)
                lacunas_count = len(docs_concorrente_set - docs_tirrell)

                metrics_data = [[
                    f"📊 Total Mercado\n{total_docs_mercado}",
                    f"✅ {tirrell_name}\n{tirrell_count}",
                    f"✅ {concorrente}\n{concorrente_count}",
                    f"🏆 Vantagens\n{vantagens_count}",
                    f"⚠️ Lacunas\n{lacunas_count}"
                ]]

                metrics_table = Table(metrics_data, colWidths=[30*mm]*5)
                metrics_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                ]))

                elements.append(metrics_table)
                elements.append(Spacer(1, 3*mm))

                # Tabela comparativa
                data_comp = [['Tipo de Documento', tirrell_name, concorrente]]

                for documento in docs_relevantes:
                    data_comp.append([
                        documento,
                        '✅' if documento in docs_tirrell else '❌',
                        '✅' if documento in docs_concorrente_set else '❌'
                    ])

                comp_table = Table(data_comp, colWidths=[70*mm, 30*mm, 30*mm])

                # Estilo base
                comp_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                    ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
                ]

                # Colorir células
                for i in range(1, len(data_comp)):
                    # Coluna TIRRELL
                    if data_comp[i][1] == '✅':
                        comp_style.append(('BACKGROUND', (1, i), (1, i), colors.HexColor('#bbf7d0')))
                    else:
                        comp_style.append(('BACKGROUND', (1, i), (1, i), colors.HexColor('#fecaca')))

                    # Coluna Concorrente
                    if data_comp[i][2] == '✅':
                        comp_style.append(('BACKGROUND', (2, i), (2, i), colors.HexColor('#bbf7d0')))
                    else:
                        comp_style.append(('BACKGROUND', (2, i), (2, i), colors.HexColor('#fecaca')))

                comp_table.setStyle(TableStyle(comp_style))
                elements.append(comp_table)
                elements.append(Spacer(1, 6*mm))

            elements.append(PageBreak())

    # Gerar PDF com canvas customizado
    print(f"Gerando PDF: {output_path}")
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"✅ PDF gerado com sucesso: {output_path}")

if __name__ == '__main__':
    gerar_pdf()
