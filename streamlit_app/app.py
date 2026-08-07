import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from analytics import scoring
from ui import render

render.init("Vue d'ensemble")
render.page_header(
    "Vue d'ensemble",
    "Compétitivité tarifaire des banques camerounaises",
    "Score 0-100 : plus le score est élevé, plus la banque est compétitive sur le panier standard particuliers.",
)

ranking = scoring.compute_ranking()
standards = scoring.market_standards()

conn = scoring.connect()
n_services = conn.execute("SELECT COUNT(DISTINCT service_key) FROM tariffs").fetchone()[0]
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
conn.close()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render.kpi("Banques couvertes", "10", "Référentiel particuliers", "accent", "🏦")
with c2:
    render.kpi("Services suivis", str(n_services), "Grilles tarifaires HT", "accent", "🧾")
with c3:
    render.kpi("Banque la plus compétitive", ranking[0]["bank_code"], f"Score {ranking[0]['score']}", "success", "🏆")
with c4:
    avg_cov = round(sum(r["coverage"] for r in ranking) / len(ranking), 1)
    render.kpi("Couverture moyenne", f"{avg_cov}/10", "Panier standard", "warning", "📊")

render.section("Classement général")

ranked = [r for r in ranking if r["rank"]]
rows = "".join(
    f'<div class="rank-row">'
    f'<span class="rank-pos">{r["rank"]}</span>'
    f'<span class="rank-bank">{bank_names.get(r["bank_code"], r["bank_code"])}</span>'
    f'<div class="rank-bar"><div class="rank-fill" style="width:{r["score"]}%"></div></div>'
    f'<span class="rank-score">{r["score"]}</span>'
    f'</div>'
    for r in ranked
)
st.markdown(f'<div class="rank-list">{rows}</div>', unsafe_allow_html=True)

excluded = [r for r in ranking if not r["rank"]]
if excluded:
    names = ", ".join(bank_names.get(r["bank_code"], r["bank_code"]) for r in excluded)
    render.callout("warning", "Non classées (couverture insuffisante)", names)

if standards:
    body = " - ".join(f"{label} : {v:,.0f} XAF partout" for label, v in standards)
    render.callout("info", "Standards du marché (exclus du score)", body)

render.disclaimer()