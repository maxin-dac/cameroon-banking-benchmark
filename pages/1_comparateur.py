import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from analytics import compare
from analytics.labels import service_label
from ui import render

render.init("Comparateur")
render.page_header(
    "Comparateur",
    "Comparaison tarifaire par service",
    "Montants HT : /an pour les récurrents, /opération pour les transactionnels. Canal digital prioritaire.",
)

conn = compare.connect()
banks = [b["bank_code"] for b in conn.execute("SELECT bank_code FROM banks ORDER BY bank_code")]
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
services = [r["service_key"] for r in conn.execute("SELECT DISTINCT service_key FROM tariffs ORDER BY service_key")]

col1, col2 = st.columns(2)
sel_banks = col1.multiselect("Banques", banks, default=banks, format_func=lambda c: bank_names.get(c, c))
sel_services = col2.multiselect(
    "Services",
    services,
    default=["account_maintenance", "local_transfer_systac", "card_visa_classic_annual", "atm_withdrawal_gimac"],
    format_func=service_label,
)

if not sel_banks or not sel_services:
    render.empty_state("Sélection vide", "Choisissez au moins une banque et un service.")
    st.stop()

rows_html = []
for key in sel_services:
    texts = {}
    for bank in sel_banks:
        row = compare.pick_row(conn, bank, [key])
        if row is None:
            texts[bank] = None
            continue
        texts[bank] = compare.format_tariff(row)

    cells = [f'<th scope="row">{service_label(key)}</th>']
    for bank in sel_banks:
        if texts[bank] is None:
            cells.append('<td><span class="pill muted">—</span></td>')
        else:
            cells.append(f'<td><span class="pill">{texts[bank]}</span></td>')
    rows_html.append("<tr>" + "".join(cells) + "</tr>")

conn.close()

head = "<tr><th>Service</th>" + "".join(f"<th>{bank_names.get(b, b)}</th>" for b in sel_banks) + "</tr>"
st.markdown(
    f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead><tbody>{"".join(rows_html)}</tbody></table></div>',
    unsafe_allow_html=True,
)
st.caption("Montants HT. Données publiques, collecte manuelle. Tri alphabétique par banque.")

render.disclaimer()