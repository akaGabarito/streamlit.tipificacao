# 📋 Como Usar o Arquivo Excel - Pesquisa de Mercado

## 📂 Localização
`data/Pesquisa de mercado - Tipificação.xlsx`

## 🏗️ Estrutura do Arquivo

### Aba 1: **Mercado** (Referência)
- **Função:** Define TODOS os tipos de documentos possíveis no mercado
- **Formato:** Cada coluna = uma categoria (IDENTIFICATÓRIO, FINANCEIRO, VEICULAR, JURÍDICO, FUNCIONAL)
- **Conteúdo:** Lista de documentos em cada categoria
- ⚠️ Esta aba é a REFERÊNCIA para comparação

**Exemplo:**
| IDENTIFICATÓRIO | FINANCEIRO | VEICULAR | JURÍDICO | FUNCIONAL |
|-----------------|------------|----------|----------|-----------|
| RG              | Comprovante de renda | CRLV | Contrato social | OAB |
| CNH             | Boletos | IPVA | Cartão CNPJ | CRM |
| CPF             | Extratos bancários | | Histórico Escolar | CREA |

### Aba 2+: **Nome da Empresa** (ex: TIRRELL, FLEXDOC, CREDIFY)
- **Função:** Lista os documentos que ESTA EMPRESA tipifica
- **Nome da aba:** Nome da empresa (ex: TIRRELL, FLEXDOC)
- **Formato:** Mesmas categorias da aba Mercado
- **Conteúdo:** Apenas os documentos que a empresa OFERECE

**Exemplo (TIRRELL):**
| IDENTIFICATÓRIO | FINANCEIRO | VEICULAR | JURÍDICO | FUNCIONAL |
|-----------------|------------|----------|----------|-----------|
| RG              | Comprovante de renda | | | |
| CNH             | Boletos | | | |
| CPF             | Extratos bancários | | | |

## 🔄 Lógica de Comparação

1. O sistema lê a aba **Mercado** para saber TODOS os documentos possíveis
2. Para cada empresa (abas seguintes), compara:
   - ✅ Se o documento está na lista da empresa = TIPIFICA
   - ❌ Se o documento NÃO está na lista da empresa = NÃO TIPIFICA

3. Gera tabelas comparativas mostrando:
   - **Vantagens TIRRELL:** Documentos que só a TIRRELL faz
   - **Lacunas TIRRELL:** Documentos que só o concorrente faz
   - **Empates:** Documentos que ambas fazem

## 📝 Como Adicionar Nova Empresa

1. Crie uma nova aba no Excel
2. Nome da aba = Nome da empresa (ex: "EMPRESA_X")
3. Use as MESMAS categorias da aba Mercado
4. Liste apenas os documentos que a empresa tipifica
5. Salve o arquivo

## ⚙️ Identificação da Empresa Principal

O sistema identifica automaticamente **TIRRELL** como empresa principal para comparações.

Se quiser mudar, altere o nome da aba ou ajuste nos filtros do app.

## 🎯 Exemplo Completo

```
📊 Pesquisa de mercado - Tipificação.xlsx
│
├── 📄 Aba 1: Mercado (Referência - TODOS os documentos)
├── 📄 Aba 2: TIRRELL (Sua empresa)
├── 📄 Aba 3: FLEXDOC (Concorrente 1)
├── 📄 Aba 4: CREDIFY (Concorrente 2)
└── 📄 Aba 5: EMPRESA_X (Concorrente 3)
```

## 🚀 Executar o App

```bash
streamlit run app.py
```

O app carregará automaticamente o Excel e gerará todas as análises!
