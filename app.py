import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from ui import render
from ui.version import get_version

render.init("Vue d'ensemble")

st.sidebar.caption(f"Version {get_version()}")

pages = {
    "Observatoire": [
        st.Page("pages/0_home.py", title="Vue d'ensemble", icon=":material/dashboard:", default=True),
        st.Page("pages/1_comparateur.py", title="Comparateur", icon=":material/compare_arrows:"),
        st.Page("pages/2_profil_banque.py", title="Profil Banque", icon=":material/account_balance:"),
        st.Page("pages/3_reseau.py", title="Réseau & Accès", icon=":material/map:"),
        st.Page("pages/4_produits.py", title="Offre Produits", icon=":material/category:"),
    ],
    "Analyses": [
        st.Page("pages/5_digital.py", title="Digital", icon=":material/smartphone:"),
        st.Page("pages/6_solidite.py", title="Solidité Financière", icon=":material/trending_up:"),
        st.Page("pages/8_benchmark_tarifaire.py", title="Benchmark Tarifaire", icon=":material/bar_chart:"),
    ],
    "Informations": [
        st.Page("pages/7_methodologie.py", title="Méthodologie", icon=":material/info:"),
    ]
}

pg = st.navigation(pages)
pg.run()