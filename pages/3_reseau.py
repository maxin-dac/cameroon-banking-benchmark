import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from analytics import compare
from ui import render

render.init("Réseau & accessibilité")
render.page_header(
    "Réseau & accessibilité",
    "Présence physique et services mobiles",
    "Nombre d'agences par banque et par ville/région, services mobile banking et mobile money déclarés, "
    "horaires d'ouverture publiés. Données brutes côte à côte.",
)

conn = compare.connect()

# ── Section 1 : réseau d'agences ──
render.section("Nombre d'agences par banque et par ville")

network = compare.get_network_summary(conn)
if network:
    df = pd.DataFrame(network)
    cols = ["bank_name", "region", "city", "agency_count", "source", "observation_date"]
    cols = [c for c in cols if c in df.columns]
    df = df[cols].rename(columns={
        "bank_name": "Banque", "region": "Région", "city": "Ville",
        "agency_count": "Agences", "source": "Source", "observation_date": "Date obs.",
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    # Totaux par banque
    render.section("Total d'agences par banque")
    totals = compare.get_network_totals(conn)
    if totals:
        df_tot = pd.DataFrame(totals)
        df_tot = df_tot.rename(columns={
            "bank_name": "Banque", "total_agencies": "Total agences",
        })[["Banque", "Total agences"]]
        st.dataframe(df_tot, hide_index=True, use_container_width=True)
    else:
        render.empty_state("Données non disponibles", "Le total d'agences n'est pas encore renseigné.")
else:
    render.empty_state(
        "Données en cours de collecte",
        "Le réseau d'agences n'est pas encore documenté. "
        "Collecte manuelle depuis les localisateurs des sites officiels en cours.",
    )

# ── Section 2 : mobile banking & mobile money ──
render.section("Mobile banking et mobile money")

access_data = compare.get_accessibility_overview(conn)
if access_data:
    rows_html = []
    for b in access_data:
        cells = [
            f'<td>{b["bank_name"]}</td>',
            f'<td>{render.presence_badge(b.get("mobile_banking_app", "inconnu"))}</td>',
            f'<td>{render.presence_badge(b.get("orange_money_integration", "inconnu"))}</td>',
            f'<td>{render.presence_badge(b.get("mtn_momo_integration", "inconnu"))}</td>',
            f'<td>{b.get("opening_hours_published") or "—"}</td>',
        ]
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    head = (
        "<tr>"
        "<th>Banque</th>"
        "<th>App mobile</th>"
        "<th>Orange Money</th>"
        "<th>MTN MoMo</th>"
        "<th>Horaires publiés</th>"
        "</tr>"
    )
    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
    st.caption("oui / non / ? = donnée non vérifiée. Sources : sites officiels des banques.")
else:
    render.empty_state("Données non disponibles", "Les informations d'accessibilité ne sont pas encore renseignées.")

conn.close()

render.callout(
    "info",
    "Méthodologie",
    "Présence ou absence constatée sur les sites officiels et app stores. "
    "Aucune évaluation de la qualité du service.",
)

render.disclaimer()
