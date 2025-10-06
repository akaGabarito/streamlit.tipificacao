import pandas as pd

SUPPORT_MAP = {"✅": 2, "⚙️ Parcial": 1, "❌": 0, "": 0, None: 0}
COLOR_SCALE = ["#fde2e2", "#ffe9b0", "#c7f0d8"]  # 0,1,2

def load_data(catalog_path: str, matrix_path: str):
    catalog = pd.read_csv(catalog_path)
    matrix = pd.read_csv(matrix_path)
    matrix["Suporte (✅/⚙️ Parcial/❌)"] = matrix["Suporte (✅/⚙️ Parcial/❌)"].fillna("")
    matrix["score"] = matrix["Suporte (✅/⚙️ Parcial/❌)"].map(SUPPORT_MAP).fillna(0).astype(int)
    catalog = catalog.sort_values(["Categoria", "Tipo de Documento"]).reset_index(drop=True)
    matrix = matrix.sort_values(["Empresa", "Categoria", "Tipo de Documento"]).reset_index(drop=True)
    return catalog, matrix

def pivot_matrix(df: pd.DataFrame):
    pivot = df.pivot_table(index="Empresa", columns="Tipo de Documento", values="score", aggfunc="max", fill_value=0)
    return pivot

def summarize_company(df: pd.DataFrame, empresa: str):
    sub = df[df["Empresa"] == empresa].copy()
    covered = sub[sub["score"] == 2]["Tipo de Documento"].tolist()
    partial = sub[sub["score"] == 1]["Tipo de Documento"].tolist()
    gaps = sub[sub["score"] == 0]["Tipo de Documento"].tolist()
    techs = sorted(set(";".join(sub["Tecnologia (tags)"].fillna("").tolist()).split(";")) - {""})
    return {"covered": covered, "partial": partial, "gaps": gaps, "techs": techs, "rows": sub}