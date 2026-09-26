import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from analytics import compare
from ui import render

render.init("Solidité financière")
render.page_header(
    "Solidité financière",
    "Chiffres publiés par les autorités de supervision",
    "Ratios prudentiels publiés par la COBAC et taille du bilan quand disponible publiquement. "
    "Données présentées telles quelles, sans interprétation de « bon » ou « mauvais ».",
)

METRIC_LABELS = {
    "total_bilan": "Total bilan",
    "total_depots": "Total dépôts",
    "total_credits": "Total crédits bruts",
    "fonds_propres_nets": "Fonds propres nets",
    "ratio_solvabilite": "Ratio de solvabilité",
}

conn = compare.connect()

# Déterminer les années disponibles
years_rows = conn.execute(
    "SELECT DISTINCT year FROM financial_data WHERE value IS NOT NULL ORDER BY year DESC"
).fetchall()
available_years = [r["year"] for r in years_rows] if years_rows else []

bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}

if available_years:
    sel_year = st.selectbox("Année", available_years)
    financial = compare.get_financial_overview(conn, year=sel_year)
else:
    financial = []

conn.close()

if financial:
    metrics = list(METRIC_LABELS.keys())

    # Organiser par banque
    by_bank = {}
    for f in financial:
        by_bank.setdefault(f["bank_code"], {})[f["metric_key"]] = f

    # Tableau HTML
    head_cells = "<th>Banque</th>" + "".join(
        f"<th>{METRIC_LABELS.get(m, m)}</th>" for m in metrics
    )
    head = f"<tr>{head_cells}</tr>"

    rows_html = []
    for bank_code in sorted(by_bank.keys(), key=lambda c: bank_names.get(c, c)):
        cells = [f'<td style="font-weight:600">{bank_names.get(bank_code, bank_code)}</td>']
        for metric in metrics:
            f = by_bank[bank_code].get(metric)
            if f and f.get("value") is not None:
                val = f["value"]
                unit = f.get("unit", "")
                if unit == "XAF" and val >= 1_000_000:
                    display = f"{val / 1_000_000_000:,.1f} Mds XAF"
                elif unit == "%":
                    display = f"{val:,.1f} %"
                else:
                    display = f"{val:,.0f} {unit}"
                cells.append(f'<td><span class="pill">{display}</span></td>')
            else:
                cells.append('<td><span class="pill muted">—</span></td>')
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
    st.caption("Données publiées par la COBAC. Pas de classement, pas de jugement.")

    # Source
    sources = set()
    for f in financial:
        if f.get("source"):
            sources.add(f["source"])
    if sources:
        render.section("Sources")
        for s in sorted(sources):
            st.markdown(f"- {s}")
else:
    render.empty_state(
        "Données en cours de collecte",
        "Les ratios financiers ne sont pas encore renseignés. "
        "Collecte en cours depuis les rapports COBAC et les publications officielles. "
        "La culture du reporting public reste limitée en zone CEMAC.",
    )

render.callout(
    "warning",
    "Avertissement",
    "Les ratios financiers sont présentés tels que publiés par la COBAC. "
    "L'observatoire ne porte aucun jugement sur la solidité, la performance ou le risque des établissements. "
    "Une donnée absente signifie qu'elle n'a pas été trouvée dans les publications publiques.",
)

render.disclaimer()
