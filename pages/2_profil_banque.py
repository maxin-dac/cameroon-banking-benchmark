import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from analytics import compare, labels
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
    "Fiche factuelle : identité, réseau, produits, digital et tarifs. "
    "Uniquement des données publiées et sourcées, sans note finale.",
)

# ── KPIs factuels ──
c1, c2, c3 = st.columns(3)
with c1:
    render.kpi("Services documentés", str(len(bt)), "Lignes tarifaires normalisées HT", "success")
with c2:
    render.kpi("Grille applicable au", str(info.get("tariff_effective_date") or "—"), "Date d'effet de la grille", "accent")
with c3:
    render.kpi("Publication de la grille", str(info.get("tariff_publication") or "unknown"), "Statut constaté sur le site officiel", "warning")

# ── Identité ──
st.markdown(
    f"**Nom légal** : {info.get('legal_name') or '—'} · "
    f"**Siège** : {info.get('head_office') or '—'} · "
    f"**Actionnariat** : {info.get('group') or '—'} · "
    f"**Site** : {info.get('website') or '—'} · "
    f"**Téléphone** : {info.get('phone') or '—'}"
)

# ── Accessibilité ──
render.section("Accessibilité & services mobiles")

mobile_app = info.get("mobile_banking_app") or "inconnu"
orange = info.get("orange_money_integration") or "inconnu"
mtn = info.get("mtn_momo_integration") or "inconnu"
hours = info.get("opening_hours_published") or "—"

st.markdown(
    f"App mobile : {render.presence_badge(mobile_app)} · "
    f"Orange Money : {render.presence_badge(orange)} · "
    f"MTN MoMo : {render.presence_badge(mtn)} · "
    f"Horaires : {hours}",
    unsafe_allow_html=True,
)

# ── Produits ──
render.section("Offre produits")

conn = compare.connect()
products = conn.execute(
    "SELECT product_category, product_name, available, conditions_published, published_rate "
    "FROM products WHERE bank_code = ? ORDER BY product_category",
    (code,),
).fetchall()

if products:
    rows_html = []
    for p in products:
        cells = [
            f'<td>{p["product_name"]}</td>',
            f'<td>{render.presence_badge(p["available"])}</td>',
            f'<td>{render.presence_badge(p["conditions_published"])}</td>',
            f'<td>{p["published_rate"] or "—"}</td>',
        ]
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    head = "<tr><th>Produit</th><th>Proposé</th><th>Conditions publiées</th><th>Taux affiché</th></tr>"
    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
else:
    render.empty_state("Données en cours de collecte", "Les produits de cette banque ne sont pas encore documentés.")

# ── Digital ──
render.section("Fonctionnalités digitales")

digital = conn.execute(
    "SELECT feature_name, available FROM digital_features WHERE bank_code = ? ORDER BY feature_key",
    (code,),
).fetchall()

if digital:
    rows_html = []
    for d in digital:
        cells = [
            f'<td>{d["feature_name"]}</td>',
            f'<td>{render.presence_badge(d["available"])}</td>',
        ]
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    head = "<tr><th>Fonctionnalité</th><th>Disponible</th></tr>"
    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
else:
    render.empty_state("Données en cours de collecte", "Les fonctionnalités digitales ne sont pas encore documentées.")

conn.close()

# ── Grille tarifaire ──
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