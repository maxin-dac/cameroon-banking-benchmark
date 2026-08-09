import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analytics import publication_index as pi
from ui import render

render.init("Indice de publication")
render.page_header(
    "Indice de publication",
    "Qui publie quoi, et depuis quand ?",
    "Mesure factuelle de la disponibilité des informations publiques des 19 banques agréées. Aucun critère n'est estimé.",
)

ranked, unranked = pi.compute_index()

if not ranked:
    render.empty_state("Pas encore de données", "Exécutez scripts/seed_publication_criteria.py puis complétez la collecte.")
    st.stop()

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

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Détail par pilier")
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

with c2:
    st.markdown("##### Non évaluées (collecte en cours)")
    for r in unranked:
        st.markdown(f"- **{r['bank_name']}** — {r['coverage']}/12 critères")

render.callout(
    "info",
    "Méthode",
    "Indice = moyenne pondérée des piliers renseignés (Tarifs 30 %, Finance 30 %, Digital 20 %, Gouvernance 20 %). "
    "Chaque critère est binaire et sourcé. Un pilier absent n'est pas compté 0 : il est exclu du calcul et signalé dans la couverture.",
)
render.disclaimer()