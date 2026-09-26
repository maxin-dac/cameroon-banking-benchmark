import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from analytics import compare
from ui import render

render.init("Digital")
render.page_header(
    "Digital",
    "Fonctionnalités digitales déclarées",
    "Fonctionnalités de l'app mobile listées objectivement : oui/non par banque. "
    "Pas de score de maturité digitale.",
)

FEATURE_LABELS = {
    "consultation_solde": "Consultation solde",
    "virement_interne": "Virement interne",
    "virement_instantane": "Virement instantané",
    "paiement_marchand": "Paiement marchand",
    "paiement_factures": "Paiement de factures",
    "gestion_carte": "Gestion de carte",
    "ouverture_compte_en_ligne": "Ouverture compte en ligne",
    "demande_credit_en_ligne": "Demande crédit en ligne",
    "notifications_push": "Notifications push",
}

conn = compare.connect()
digital = compare.get_digital_matrix(conn)
bank_names = {r["bank_code"]: r["bank_name"] for r in conn.execute("SELECT bank_code, bank_name FROM banks")}
conn.close()

if digital:
    features = list(FEATURE_LABELS.keys())

    # Organiser par banque
    by_bank = {}
    for d in digital:
        by_bank.setdefault(d["bank_code"], {})[d["feature_key"]] = d

    # Tableau HTML
    head_cells = "<th>Banque</th>" + "".join(
        f"<th>{FEATURE_LABELS.get(f, f)}</th>" for f in features
    )
    head = f"<tr>{head_cells}</tr>"

    rows_html = []
    for bank_code in sorted(by_bank.keys(), key=lambda c: bank_names.get(c, c)):
        cells = [f'<td style="font-weight:600">{bank_names.get(bank_code, bank_code)}</td>']
        for feat in features:
            d = by_bank[bank_code].get(feat)
            if d:
                cells.append(f"<td>{render.presence_badge(d['available'])}</td>")
            else:
                cells.append(f'<td>{render.presence_badge("inconnu")}</td>')
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    st.markdown(
        f'<div class="cb-table-wrap"><table class="cb-table"><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>',
        unsafe_allow_html=True,
    )
    st.caption("✓ = fonctionnalité déclarée · ✗ = non disponible · ? = donnée non vérifiée. Sources : app stores, sites officiels.")
else:
    render.empty_state(
        "Données en cours de collecte",
        "Les fonctionnalités digitales ne sont pas encore documentées. "
        "Vérification en cours depuis les app stores et les sites officiels.",
    )

render.callout(
    "info",
    "Méthodologie",
    "Ce tableau liste les fonctionnalités déclarées par les banques dans leurs apps et sites. "
    "Il ne constitue pas une évaluation de la qualité, de la performance ou de l'expérience utilisateur.",
)

render.disclaimer()
