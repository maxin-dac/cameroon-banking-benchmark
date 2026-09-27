import sys
from pathlib import Path
import pandas as pd
import streamlit as st
from analytics import compare
from ui import render

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

render.page_header(
    "Observatoire",
    "Le secteur bancaire camerounais, en données publiques",
    "Tarifs, réseau, produits, digital et ratios financiers : "
    "des faits sourcés et datés, sans score ni classement.",
)

ref_path = ROOT / "data" / "reference" / "banks_reference.csv"
tariffs_path = ROOT / "data" / "processed" / "tariffs" / "tariffs_all_banks.csv"

banks = pd.read_csv(ref_path) if ref_path.exists() else pd.DataFrame()
tariffs = pd.read_csv(tariffs_path) if tariffs_path.exists() else pd.DataFrame()

n_banks = len(banks) if not banks.empty else 19
n_documented = tariffs["bank_code"].nunique() if not tariffs.empty else 0
n_rows = len(tariffs)

# Compter les dimensions avec des données
conn = compare.connect()
n_network = conn.execute("SELECT COUNT(*) c FROM network WHERE agency_count IS NOT NULL").fetchone()["c"]
n_products = conn.execute("SELECT COUNT(*) c FROM products WHERE available != 'inconnu'").fetchone()["c"]
n_digital = conn.execute("SELECT COUNT(*) c FROM digital_features WHERE available != 'inconnu'").fetchone()["c"]
n_financial = conn.execute("SELECT COUNT(*) c FROM financial_data WHERE value IS NOT NULL").fetchone()["c"]
conn.close()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render.kpi("Banques agréées", str(n_banks), "Référentiel COBAC", "accent", "account_balance")
with c2:
    render.kpi("Banques documentées", str(n_documented), "Grilles particuliers publiques", "success", "description")
with c3:
    render.kpi("Lignes tarifaires", str(n_rows), "Normalisées HT", "success", "receipt_long")
with c4:
    render.kpi("Observation", "09/2026", "Collecte manuelle", "warning", "calendar_month")

render.section("Référentiel des banques agréées")

if not banks.empty:
    cols = [c for c in ["bank_code", "bank_name", "head_office", "group", "tariff_publication"] if c in banks.columns]
    st.dataframe(
        banks[cols], 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "bank_code": "Code",
            "bank_name": "Banque",
            "head_office": "Siège Social",
            "group": "Groupe",
            "tariff_publication": "Publication Tarifs"
        }
    )
else:
    render.empty_state("Référentiel absent", "data/reference/banks_reference.csv introuvable.")

render.section("Dimensions de l'observatoire")

st.markdown(
    f"""
| Dimension | Statut | Données |
| --- | --- | --- |
| **Tarifs** | <span class="material-symbols-rounded" style="color:var(--success-color);font-size:1.2em;vertical-align:middle;">check_circle</span> {n_documented} banques documentées | {n_rows} lignes normalisées |
| **Réseau & accessibilité** | {'<span class="material-symbols-rounded" style="color:var(--success-color);font-size:1.2em;vertical-align:middle;">check_circle</span>' if n_network > 0 else '<span class="material-symbols-rounded" style="color:var(--warning-color);font-size:1.2em;vertical-align:middle;">sync</span>'} En cours | {n_network} points de données |
| **Offre produits** | {'<span class="material-symbols-rounded" style="color:var(--success-color);font-size:1.2em;vertical-align:middle;">check_circle</span>' if n_products > 0 else '<span class="material-symbols-rounded" style="color:var(--warning-color);font-size:1.2em;vertical-align:middle;">sync</span>'} En cours | {n_products} produits vérifiés |
| **Digital** | {'<span class="material-symbols-rounded" style="color:var(--success-color);font-size:1.2em;vertical-align:middle;">check_circle</span>' if n_digital > 0 else '<span class="material-symbols-rounded" style="color:var(--warning-color);font-size:1.2em;vertical-align:middle;">sync</span>'} En cours | {n_digital} fonctionnalités vérifiées |
| **Solidité financière** | {'<span class="material-symbols-rounded" style="color:var(--success-color);font-size:1.2em;vertical-align:middle;">check_circle</span>' if n_financial > 0 else '<span class="material-symbols-rounded" style="color:var(--warning-color);font-size:1.2em;vertical-align:middle;">sync</span>'} En cours | {n_financial} ratios publiés |
""", unsafe_allow_html=True
)

render.section("Pages de l'observatoire")

st.markdown(
    """
- **Comparateur** : tarifs particuliers comparés service par service (banques documentées).
- **Profil banque** : fiche factuelle complète — identité, réseau, produits, digital et tarifs.
- **Réseau & accessibilité** : nombre d'agences par ville, mobile banking/money, horaires publiés.
- **Offre produits** : matrice de présence/absence par catégorie de produit.
- **Digital** : fonctionnalités app mobile listées objectivement (oui/non).
- **Solidité financière** : ratios COBAC publiés, taille du bilan, dépôts, crédits.
- **Méthodologie** : ce que fait l'observatoire et ce qu'il ne fait pas.
- **Benchmark tarifaire** : visualisations par service du panier standard.
"""
)

render.callout(
    "info",
    "Positionnement",
    "Ce document présente des données publiques et déclaratives, "
    "sans jugement de qualité ou de performance. "
    "Aucun score, aucune notation, aucun classement.",
)

render.disclaimer()
