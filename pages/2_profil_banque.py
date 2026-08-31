import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from analytics import labels
from ui import render

render.init("Profil banque")

ref_path = ROOT / "data" / "reference" / "banks_reference.csv"
tariffs_path = ROOT / "data" / "processed" / "tariffs" / "tariffs_all_banks.csv"

banks = pd.read_csv(ref_path, dtype=str)
tariffs = pd.read_csv(tariffs_path) if tariffs_path.exists() else pd.DataFrame()

names = dict(zip(banks["bank_code"], banks["bank_name"]))
code = st.selectbox("Banque", banks["bank_code"], format_func=lambda c: names.get(c, c))

info = banks[banks["bank_code"] == code].iloc[0]
bt = tariffs[tariffs["bank_code"] == code] if not tariffs.empty else pd.DataFrame()

render.page_header(
    "Profil banque",
    str(info["bank_name"]),
    "Identité, actionnariat publié et grille tarifaire particuliers. Uniquement des faits publiés et sourcés.",
)

c1, c2, c3 = st.columns(3)
with c1:
    render.kpi("Services documentés", str(len(bt)), "Lignes tarifaires normalisées HT", "success")
with c2:
    render.kpi("Grille applicable au", str(info.get("tariff_effective_date") or "—"), "Date d'effet de la grille", "accent")
with c3:
    render.kpi("Publication de la grille", str(info.get("tariff_publication") or "unknown"), "Statut constaté sur le site officiel", "warning")

st.markdown(
    f"**Nom légal** : {info.get('legal_name') or '—'} · "
    f"**Siège** : {info.get('head_office') or '—'} · "
    f"**Actionnariat** : {info.get('group') or '—'} · "
    f"**Site** : {info.get('website') or '—'} · "
    f"**Téléphone** : {info.get('phone') or '—'}"
)

render.section("Grille tarifaire particuliers (HT)")

if bt.empty:
    render.empty_state(
        "Pas encore de grille normalisée",
        "Les tarifs de cette banque ne sont pas encore documentés dans la base. Collecte en cours.",
    )
else:
    def fmt(r):
        if pd.notna(r.get("rate_pct")):
            s = f"{float(r['rate_pct']):g} %"
            if pd.notna(r.get("min_amount_ht")):
                s += f" min {float(r['min_amount_ht']):,.0f}"
            if pd.notna(r.get("max_amount_ht")):
                s += f" max {float(r['max_amount_ht']):,.0f}"
            return s
        for col, suf in [
            ("amount_per_operation_ht", " / opération"),
            ("amount_annual_ht", " / an"),
            ("amount_one_time_ht", " une fois"),
            ("amount_condition_ht", " (condition)"),
        ]:
            if pd.notna(r.get(col)):
                return f"{float(r[col]):,.0f}{suf}"
        return "—"

    view = pd.DataFrame(
        {
            "Service": [labels.service_label(k) for k in bt["service_key"]],
            "Canal": [labels.channel_label(c) for c in bt["channel"]],
            "Tarif HT": [fmt(r) for _, r in bt.iterrows()],
        }
    )
    st.dataframe(view, hide_index=True, width="stretch")

render.disclaimer()