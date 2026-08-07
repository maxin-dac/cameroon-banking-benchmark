import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from ui import render

render.init("Méthodologie")
render.page_header(
    "Méthodologie",
    "Comment les données et le score sont produits",
    "Transparence complète sur les sources, les règles de normalisation et les limites.",
)

st.markdown(
    """
**Sources** : brochures tarifaires publiques des 10 banques, collectées manuellement (aucun scraping).
Chaque ligne de la base porte sa source et sa date de consultation (2026-06-22).

**Périmètre** : particuliers uniquement (salariés, non salariés, étudiants). Montants HT.

**Normalisation** :
- Services récurrents convertis en base annuelle (mensuel x 12, trimestriel x 4).
- Services transactionnels conservés en montant par opération, sans projection annuelle.
- Formules variables (ex. 1% min 500 max 1 000) stockées telles quelles ; évaluées uniquement
  dans le benchmark avec un scénario standard de 50 000 XAF pour le retrait GAB confrère.

**Score de compétitivité (0-100)** :
- Panier de 10 services comparables ; canal digital prioritaire quand il existe.
- Score par service = classement robuste (le moins cher = 100, le plus cher = 0).
- Items à variance nulle (gratuit partout) exclus et reportés comme standards du marché.
- Score global = moyenne des services disponibles ; couverture minimale de 5/10 pour être classé.

**Limites** : observations ponctuelles, grilles publiques parfois partielles (ex. SCB),
absence de données digitales et financières dans cette version.
"""
)

render.callout("warning", "Avertissement",
               "Outil d'aide à la décision. Ne remplace pas les conditions officielles des banques ni une étude approfondie.")

render.disclaimer()