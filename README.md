# 🏆 Análise de Mercado - Comparativo de Tipificação de Documentos

Sistema de análise qualitativa para comparar capacidades de tipificação de documentos entre empresas.

## 📁 Estrutura do Projeto

```
dados/
├── app.py                                          # Aplicação Streamlit principal
├── data/
│   └── Pesquisa de mercado - Tipificação.xlsx    # Arquivo Excel com dados
├── INSTRUCOES_EXCEL.md                            # Instruções para o Excel
└── README.md                                       # Este arquivo
```

## 🚀 Como Usar

### 1. Preparar o Arquivo Excel

Edite o arquivo: `data/Pesquisa de mercado - Tipificação.xlsx`

**Estrutura:**
- **Aba 1 (Mercado):** Todos os documentos possíveis no mercado, organizados por categoria
- **Aba 2+ (Empresas):** Nome da aba = nome da empresa. Liste apenas os documentos que ela tipifica

### 2. Executar o App

```bash
streamlit run app.py
```

### 3. Usar os Filtros

Na barra lateral:
- ✅ **Categorias:** Marque/desmarque categorias para analisar
- ✅ **Empresas:** Selecione empresas para comparar
- 🎯 **Visualização:** Escolha o tipo de análise

## 📊 Visualizações Disponíveis

### 🎯 Tirrell vs Concorrentes (Principal)
**Análise qualitativa com tabelas comparativas**

Para cada concorrente e categoria:
- Tabela mostrando ✅/❌ para cada documento
- Cores:
  - 🟢 Verde: Vantagem TIRRELL (só ela faz)
  - 🔴 Vermelho: Lacuna TIRRELL (só concorrente faz)
  - 🔵 Azul: Empate (ambas fazem)

## 🎨 Lógica de Comparação

```
📌 Referência: Aba "Mercado" = TODOS os documentos possíveis

Para cada empresa:
  Se documento está na lista da empresa:
    ✅ TIPIFICA
  Caso contrário:
    ❌ NÃO TIPIFICA
```

## 📝 Como Adicionar Nova Empresa

1. Abra: `data/Pesquisa de mercado - Tipificação.xlsx`
2. Crie nova aba com o nome da empresa
3. Use as mesmas categorias da aba "Mercado"
4. Liste apenas os documentos que a empresa tipifica
5. Salve o arquivo
6. Recarregue o app (R no navegador)

## ⚙️ Requisitos

```bash
pip install streamlit pandas altair openpyxl
```

**Desenvolvido para análise competitiva de tipificação de documentos** 🚀
