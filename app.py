import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from ui import render

render.init("Vue d'ensemble")

from ui.version import get_version

st.sidebar.caption(f"Version {get_version()}")

render.page_header(
    "Observatoire",
    "Le secteur bancaire camerounais, en données publiques",
    "Tarifs particuliers normalisés, cadre réglementaire CEMAC et chiffres clés du marché. "
    "Aucun score, aucune notation : uniquement des faits sourcés et datés.",
)

ref_path = ROOT / "data" / "reference" / "banks_reference.csv"
tariffs_path = ROOT / "data" / "processed" / "tariffs" / "tariffs_all_banks.csv"

banks = pd.read_csv(ref_path) if ref_path.exists() else pd.DataFrame()
tariffs = pd.read_csv(tariffs_path) if tariffs_path.exists() else pd.DataFrame()

n_banks = len(banks) if not banks.empty else 19
n_documented = tariffs["bank_code"].nunique() if not tariffs.empty else 0
n_rows = len(tariffs)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render.kpi("Banques agréées", str(n_banks), "Référentiel COBAC", "accent", "🏦")
with c2:
    render.kpi("Banques documentées", str(n_documented), "Grilles particuliers publiques", "success", "📄")
with c3:
    render.kpi("Lignes tarifaires", str(n_rows), "Normalisées HT", "success", "🧾")
with c4:
    render.kpi("Observation", "08/2026", "Collecte manuelle", "warning", "🗓️")

render.section("Référentiel des banques agréées")

if not banks.empty:
    cols = [c for c in ["bank_code", "bank_name", "head_office", "group", "tariff_publication"] if c in banks.columns]
    st.dataframe(banks[cols], hide_index=True, use_container_width=True)
else:
    render.empty_state("Référentiel absent", "data/reference/banks_reference.csv introuvable.")

render.section("Modules de l'observatoire")

st.markdown(
    """
- **Comparateur** : tarifs particuliers comparés service par service (banques documentées).
- **Profil banque** : identité, gouvernance publiée et grille tarifaire de chaque banque.
- **Benchmark tarifaire** : visualisations par service du panier standard.
- **Cadre réglementaire** *(en construction)* : conventions, règlements COBAC/CEMAC, instructions et institutions de supervision.
- **Marché bancaire** *(en construction)* : total bilan, crédits, dépôts, créances en souffrance.
"""
)

render.callout(
    "info",
    "Positionnement",
    "L'observatoire ne note pas les banques : il donne à voir des faits publics, tracés et datés. "
    "Les modules financier et digital sont en cours de collecte.",
)

render.disclaimer()