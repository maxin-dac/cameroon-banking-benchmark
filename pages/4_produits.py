import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from analytics import compare
from ui import render

render.init("Offre produits")
render.page_header(
    "Offre produits",
    "Matrice de présence des produits bancaires",
    "Liste des produits proposés par banque : présence/absence, pas d'évaluation de qualité. "
    "Conditions publiées quand elles existent.",
)

CATEGORY_LABELS = {
    "compte_courant": "Compte courant",
    "epargne": "Épargne",
    "credit_immobilier": "Crédit immobilier",
    "credit_consommation": "Crédit consommation",
    "credit_pme": "Crédit PME/TPE",
    "assurance": "Assurance (bancassurance)",
    "transfert_international": "Transfert international",
}

conn = compare.connect()
products = compare.get_product_matrix(conn)
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
conn.close()

if products:
    # Construire le tableau croisé banque × catégorie
    categories = list(CATEGORY_LABELS.keys())

    # Organiser par banque
    by_bank = {}
    for p in products:
        by_bank.setdefault(p["bank_code"], {})[p["product_category"]] = p

    # Tableau HTML
    head_cells = "<th>Banque</th>" + "".join(
        f"<th>{CATEGORY_LABELS.get(c, c)}</th>" for c in categories
    )
    head = f"<tr>{head_cells}</tr>"

    rows_html = []
    for bank_code in sorted(by_bank.keys(), key=lambda c: bank_names.get(c, c)):
        cells = [f'<td style="font-weight:600">{bank_names.get(bank_code, bank_code)}</td>']
        for cat in categories:
            p = by_bank[bank_code].get(cat)
            if p:
                badge = render.presence_badge(p["available"])
                if p.get("conditions_published") == "oui" and p.get("published_rate"):
                    badge += f' <small style="color:#64748b">{p["published_rate"]}</small>'
                cells.append(f"<td>{badge}</td>")
            else:
                cells.append(f'<td>{render.presence_badge("inconnu")}</td>')
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
    st.caption("✓ = produit proposé · ✗ = non proposé · ? = donnée non vérifiée. Sources : sites officiels.")

    # Détail des conditions publiées
    published = [p for p in products if p.get("conditions_published") == "oui" and p.get("published_rate")]
    if published:
        render.section("Conditions publiées")
        df = pd.DataFrame(published)
        cols = ["bank_name", "product_name", "published_rate", "published_duration", "source"]
        cols = [c for c in cols if c in df.columns]
        df = df[cols].rename(columns={
            "bank_name": "Banque", "product_name": "Produit",
            "published_rate": "Taux affiché", "published_duration": "Durée",
            "source": "Source",
        })
        st.dataframe(df, hide_index=True, use_container_width=True)
else:
    render.empty_state(
        "Données en cours de collecte",
        "L'inventaire des produits bancaires n'est pas encore documenté. "
        "Collecte en cours depuis les sites officiels et brochures commerciales.",
    )

render.callout(
    "info",
    "Méthodologie",
    "Ce tableau documente la présence ou l'absence déclarée de chaque catégorie de produit. "
    "Il ne constitue pas une évaluation de la qualité ni de la compétitivité de ces produits.",
)

render.disclaimer()
