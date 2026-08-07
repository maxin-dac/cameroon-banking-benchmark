import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from analytics import scoring
from analytics.labels import channel_label, service_label
from ui import render

render.init("Profil banque")

conn = scoring.connect()
banks = [b["bank_code"] for b in conn.execute("SELECT bank_code FROM banks ORDER BY bank_code")]
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
conn.close()

bank = st.selectbox("Banque", banks, format_func=lambda c: bank_names.get(c, c))

conn = scoring.connect()
info = conn.execute("SELECT * FROM banks WHERE bank_code = ?", (bank,)).fetchone()
rows = conn.execute(
    """
    SELECT service_category, service_key, channel, rate_pct, min_amount_ht, max_amount_ht,
           amount_per_operation_ht, amount_annual_ht, amount_one_time_ht, amount_condition_ht
    FROM tariffs
    WHERE bank_code = ?
    ORDER BY service_category, service_key, channel
    """,
    (bank,),
).fetchall()
conn.close()

ranking = {r["bank_code"]: r for r in scoring.compute_ranking()}
pos = ranking.get(bank)

render.page_header(
    "Profil banque",
    bank_names.get(bank, bank),
    f"{info['legal_name']} - Siege : {info['head_office']} - Tarifs applicables au {info['tariff_effective_date']}",
)

if pos:
    c1, c2, c3 = st.columns(3)
    with c1:
        render.kpi("Score de competitivite", f"{pos['score']}", "Panier standard particuliers", "accent", "S")
    with c2:
        render.kpi("Rang national", str(pos["rank"]) if pos["rank"] else "n.c.", "Sur les banques classees", "success", "R")
    with c3:
        render.kpi("Couverture du panier", f"{pos['coverage']}/10", "Services documentes", "warning", "C")
    if not pos["rank"]:
        render.callout(
            "warning",
            "Couverture insuffisante",
            "Trop de services du panier sont absents de la grille publique : banque non classee.",
        )
else:
    render.callout("warning", "Banque non classee", "Donnees insuffisantes pour calculer un score.")

render.section("Grille tarifaire particuliers")

body = "".join(
    "<tr>"
    f"<td>{r['service_category']}</td>"
    f"<td>{service_label(r['service_key'])}</td>"
    f"<td>{channel_label(r['channel'])}</td>"
    f'<td><span class="pill">{scoring.format_tariff(r)}</span></td>'
    "</tr>"
    for r in rows
)

st.markdown(
    '<div class="cb-table-wrap"><table class="cb-table">'
    "<thead><tr><th>Categorie</th><th>Service</th><th>Canal</th><th>Tarif HT</th></tr></thead>"
    f"<tbody>{body}</tbody></table></div>",
    unsafe_allow_html=True,
)

st.caption(f"Source : {info['tariff_source']}")

render.disclaimer()
