import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analytics import publication_index as pi
from ui import render

render.init("Vue d'ensemble")

render.page_header(
    "Observatoire",
    "Transparence bancaire au Cameroun",
    "Qui publie quoi, et depuis quand ? Mesure factuelle de la disponibilité des informations publiques des 19 banques agréées.",
)

ranked, unranked = pi.compute_index()

tariffs_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "tariffs" / "tariffs_all_banks.csv"
n_tariff_rows = 0
n_tariff_banks = 0
if tariffs_path.exists():
    df_t = pd.read_csv(tariffs_path)
    n_tariff_rows = len(df_t)
    n_tariff_banks = df_t["bank_code"].nunique()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render.kpi("Banques agréées", "19", "Référentiel COBAC", "accent", "🏦")
with c2:
    render.kpi("Banques documentées", str(n_tariff_banks), "Grilles tarifaires publiques", "success", "📄")
with c3:
    render.kpi("Lignes tarifaires", str(n_tariff_rows), "Normalisées HT", "success", "🧾")
with c4:
    render.kpi("Évaluées (indice)", str(len(ranked)), "Couverture ≥ 4 critères", "warning", "🏆")

render.section("Indice de publication (0–100)")

if ranked:
    fig = go.Figure(go.Bar(
        x=[r["index"] for r in ranked],
        y=[r["bank_name"] for r in ranked],
        orientation="h",
        marker_color=["#059669" if r["index"] >= 75 else "#d97706" for r in ranked],
        marker_cornerradius=6,
        text=[f"{r['index']}" for r in ranked],
        textposition="outside",
    ))
    render.style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    detail = pd.DataFrame([
        {
            "Banque": r["bank_name"],
            "Indice": r["index"],
            "Couverture": f"{r['coverage']}/12",
            "Tarifs": r["pillars"].get("tarifs"),
            "Finance": r["pillars"].get("finance"),
            "Digital": r["pillars"].get("digital"),
            "Gouvernance": r["pillars"].get("gouvernance"),
        }
        for r in ranked
    ]).fillna("—")
    st.dataframe(detail, hide_index=True, use_container_width=True)
else:
    render.empty_state(
        "Pas encore de données",
        "Exécutez scripts/seed_publication_criteria.py puis complétez la collecte.",
    )

if unranked:
    render.callout(
        "warning",
        f"Non évaluées ({len(unranked)})",
        " - ".join(r["bank_name"] for r in unranked) + " : collecte en cours (couverture < 4 critères).",
    )

render.callout(
    "info",
    "Méthode",
    "Indice = moyenne pondérée des piliers renseignés (Tarifs 30 %, Finance 30 %, Digital 20 %, Gouvernance 20 %). "
    "Chaque critère est binaire et sourcé ; un pilier absent n'est pas compté 0 : il est exclu du calcul et signalé dans la couverture.",
)

render.disclaimer()