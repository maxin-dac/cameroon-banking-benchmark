import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.graph_objects as go
import streamlit as st

from analytics import compare
from ui import render

render.init("Benchmark tarifaire")
render.page_header(
    "Benchmark tarifaire",
    "Comparaison visuelle par service du panier",
    "Montants affichés côte à côte. Formules variables évaluées au scénario indiqué.",
)

conn = compare.connect()
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
detail = compare.get_tariff_comparison(conn)
conn.close()

labels = {item_id: label for item_id, (label, vals, std) in detail.items()}
choice = st.selectbox("Service du panier", list(labels.keys()), format_func=lambda x: labels[x])

label, vals, std = detail[choice]

if len(vals) < 2:
    render.empty_state("Données insuffisantes", "Moins de deux banques documentées sur ce service.")
    st.stop()

# Tri alphabétique par nom de banque (pas par prix)
items = sorted(vals.items(), key=lambda kv: bank_names.get(kv[0], kv[0]))
codes = [b for b, v in items]
values = [v for b, v in items]
names = [bank_names.get(b, b) for b in codes]

# Couleur neutre uniforme — pas de vert/rouge
fig = go.Figure(go.Bar(
    x=values,
    y=names,
    orientation="h",
    marker_color="#2563eb",
    marker_cornerradius=6,
    text=[f"{v:,.0f}" for v in values],
    textposition="outside",
))
render.style_fig(fig)
fig.update_layout(xaxis_title="XAF HT", yaxis_title="", height=max(340, 48 * len(values)))
st.plotly_chart(fig, use_container_width=True)

if std:
    render.callout("info", "Scénario appliqué", f"Formules variables évaluées pour un montant de {std:,.0f} XAF.")

render.callout(
    "info",
    "Lecture",
    "Montants HT affichés côte à côte. Tri alphabétique. Données publiques et déclaratives.",
)

render.disclaimer()
