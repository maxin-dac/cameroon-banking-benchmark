import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from ui import render

render.init("Méthodologie")

render.page_header(
    "Méthodologie",
    "Ce que fait l'observatoire — et ce qu'il ne fait pas",
    "Ce document présente des données publiques et déclaratives, "
    "sans jugement de qualité ou de performance.",
)

render.section("Positionnement")
st.markdown(
    """
**Ce que fait l'observatoire :**
- Collecte des données publiques : tarifs, réseau d'agences, produits proposés,
  fonctionnalités digitales déclarées, ratios financiers publiés par la COBAC.
- Les présente **côte à côte** dans des tableaux comparatifs factuels.
- Trace chaque donnée à **sa source et sa date de consultation**.

**Ce que l'observatoire ne fait PAS :**
- ❌ Aucun classement, aucune note, aucun score.
- ❌ Aucune interprétation de type « bon » ou « mauvais ».
- ❌ Aucune estimation : une donnée absente est affichée comme telle, jamais comblée.
- ❌ Aucune évaluation subjective de la « qualité de service ».
"""
)

render.section("Dimensions couvertes")
st.markdown(
    """
| Dimension | Données collectées | Type |
| --- | --- | --- |
| **Tarifs** | Grilles tarifaires particuliers normalisées HT | Montants chiffrés |
| **Réseau & accessibilité** | Nombre d'agences par ville/région, mobile banking, mobile money, horaires | Chiffres + binaire (oui/non) |
| **Offre produits** | Crédit immo, conso, PME, épargne, assurance, transfert international | Présence/absence |
| **Digital** | Fonctionnalités app mobile (virement instantané, paiement marchand, etc.) | Binaire (oui/non) |
| **Solidité financière** | Ratios COBAC publiés, taille bilan, dépôts, crédits | Chiffres publiés |
"""
)

render.section("Règles de normalisation tarifaire")
st.markdown(
    """
- **Montants HT** uniquement ; les grilles TTC sont écartées.
- **Frais récurrents** annualisés (mensuel × 12, trimestriel × 4).
- **Frais transactionnels** conservés **par opération**, sans projection annuelle.
- **Formules variables** (ex. 1 % min 500 max 1 000) stockées telles quelles ; évaluées uniquement au
  scénario standard de 50 000 XAF pour le retrait GAB confrère.
- **Canal digital prioritaire** quand il existe (ex. virement SYSTAC en ligne vs agence).
- **Aucune estimation** : une donnée manquante est affichée comme telle, jamais comblée.
"""
)

render.section("Sources des données (module tarifs)")
st.markdown(
    """
Collecte **100 % manuelle**, aucun scraping. Observation : **août 2026**.

| Banque | Source | Période |
| --- | --- | --- |
| Access Bank | [Quarterly Banking Conditions](https://cameroon.accessbankplc.com/access/media/Media-PDF-Attachment/Quarterly-Banking-Conditions.pdf) | T3 2026 |
| Afriland First Bank | [Tarification Particuliers 2026](https://www.afrilandfirstbank.com/wp-content/uploads/2026/07/Tarification_AFB_Particulier_2026-2.pdf) | 2026 |
| BICEC | [Conditions de banque Particuliers](https://www.bicec.com/pdf/BICEC_Conditions%20de%20banque_Particuliers_VA-VF_Mars2026.pdf) | Mars 2026 |
| CCA-BANK | [Tarifaire T2 2026](https://www.cca-bank.com/assets/tarifaires/cca-bank-tarifaire-2e-trimestre-2026-fr.pdf) | T2 2026 |
| Commercial Bank | [CB Particuliers](https://commercialbank-cm.com/wp-content/uploads/2019/09/CB-PARTICULIERS-OCT-2025.pdf) | 01/10/2025 |
| SCB Cameroun | [Conditions de banque T2 2026](https://www.scbcameroun.net/conditions-tarifaires-scbcameroun/29-les-conditions-de-banque-du-t2-2026/file) | T2 2026 |
| Société Générale | [Conditions tarifaires T3 2026](https://particuliers.societegenerale.cm/fileadmin/user_upload/Cameroun/PDF/2026/T3_-_2026/CLIPRI-T-3-2026-60X80-VF.pdf) | 01/07/2026 |
| UBA | [Conditions de banque](https://www.ubacameroon.com/wp-content/uploads/sites/8/2026/08/CONDITIONS-DE-BANQUE-APPLICABLES-A-LA-CLIENTELE-JUILLET-SEPTEMBRE-2026.pdf) | Juil.–Sept. 2026 |
| Africa Golden Bank | [Condition de banque T2 2025](https://africagoldenbank.com/wp-content/uploads/2025/06/CONDITION-DE-BANQUE-2e-trimestre-2025.pdf) | T2 2025 |
| AFG Bank | [Grille tarifaire Juillet 2026](https://afgbank.cm/files/2026/07/Press-Version-Press-CONDITION-FR-2026-Juillet.pdf) | 01/07/2026 |
"""
)

render.section("Éthique & conformité")
st.markdown(
    """
- Pas de scraping : collecte manuelle depuis des sources publiques officielles, dans le respect des CGU
  et de la loi n°2010/012 sur la cybersécurité.
- Traçabilité : chaque ligne porte sa source et sa date de consultation.
- Pas de données personnelles, pas de secret bancaire : uniquement des données publiques.
"""
)

render.section("Limites")
st.markdown(
    """
- Observation ponctuelle (août 2026) : les tarifs et données peuvent évoluer.
- Culture du reporting public faible en zone CEMAC : certaines banques ne publient rien
  → une donnée absente est un résultat, pas un bug.
- Comparaisons tarifaires limitées aux 10 banques documentées et au panier particuliers normalisé.
- Les dimensions réseau, produits, digital et financière sont en cours de collecte.
"""
)

render.callout(
    "warning",
    "Avertissement",
    "Outil d'aide à la décision. Ne remplace pas une étude approfondie ni les conditions officielles des banques.",
)

render.disclaimer()
