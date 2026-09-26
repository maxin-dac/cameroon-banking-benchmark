# 🏦 Cameroun Banking Benchmark — Observatoire Factuel du Secteur Bancaire

> 🚧 ***Travail en cours***

> **Ce document présente des données publiques et déclaratives, sans jugement de qualité ou de performance.**

Observatoire comparatif du secteur bancaire camerounais. Pas de score, pas de classement, pas de notation : uniquement des faits sourcés, datés et vérifiables, présentés côte à côte.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Data-Sources_publiques-00693E?style=for-the-badge" alt="Données publiques" />
  <img src="https://img.shields.io/badge/Bilingue-FR_|_EN-008080?style=for-the-badge" alt="Bilingue FR EN" />
  <img src="https://img.shields.io/badge/Statut-En_cours-orange?style=for-the-badge" alt="Statut" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

🇬🇧 English : [README_EN.md](README_EN.md)

## Dimensions couvertes

| Dimension | Description | Statut |
| --- | --- | --- |
| **Tarifs** | Grilles tarifaires particuliers normalisées HT, comparées service par service | ✅ 10 banques |
| **Réseau & accessibilité** | Nombre d'agences par ville/région, mobile banking/money (oui/non), horaires publiés | 🔄 En cours |
| **Offre produits** | Matrice de présence/absence (crédit immo, conso, PME, épargne, assurance) | 🔄 En cours |
| **Digital** | Fonctionnalités app mobile listées objectivement (oui/non) | 🔄 En cours |
| **Solidité financière** | Ratios COBAC publiés, taille bilan, dépôts, crédits — présentés tels quels | 🔄 En cours |

## Sources des données (module tarifs)

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
| 9 autres banques agréées | Collecte manuelle (sites, COBAC, presse) | en cours |

## Principes

- **Pas de score, pas de classement** : tableaux comparatifs côte à côte, fiches par banque avec données brutes.
- **Pas de scraping** : collecte manuelle depuis des sources publiques officielles.
- **Traçabilité** : chaque ligne porte sa source et sa date de consultation.
- **Honnêteté** : une donnée manquante est affichée comme telle, jamais estimée ni comblée.
- **Pas d'interprétation** : les ratios financiers sont présentés tels que publiés par la COBAC, sans jugement de « bon » ou « mauvais ».
- **Pas de données personnelles**, pas de secret bancaire : uniquement des données publiques.

## Limites

- Observation ponctuelle (août 2026) : les données peuvent évoluer.
- Culture du reporting public faible en zone CEMAC : certaines banques ne publient rien.
- Comparaisons tarifaires limitées aux 10 banques documentées et au panier particuliers normalisé.
- Les dimensions réseau, produits, digital et financière sont en cours de collecte.

## Structure du projet

```text
cameroon-banking-benchmark/
├── analytics/
│   ├── __init__.py
│   ├── labels.py
│   └── compare.py              # comparaisons factuelles (0 score, 0 classement)
├── assets/                     # css + templates html
├── data/
│   ├── db/banking_benchmark.db
│   ├── processed/tariffs/tariffs_all_banks.csv
│   ├── raw/documents/          # PDF sources (gitignoré)
│   └── reference/
│       ├── banks_reference.csv     # 19 banques + colonnes accessibilité
│       ├── network.csv             # agences par ville/région
│       ├── products.csv            # matrice produits (présence/absence)
│       ├── digital_features.csv    # fonctionnalités app (oui/non)
│       └── financial_ratios.csv    # ratios COBAC publiés
├── pages/
│   ├── 1_comparateur.py        # tarifs côte à côte (neutre)
│   ├── 2_profil_banque.py      # fiche complète 4 dimensions
│   ├── 3_reseau.py             # agences, mobile banking/money, horaires
│   ├── 4_produits.py           # matrice présence/absence
│   ├── 5_digital.py            # fonctionnalités app (oui/non)
│   ├── 6_solidite.py           # ratios COBAC publiés
│   ├── 7_methodologie.py       # ce que fait / ne fait pas l'observatoire
│   └── 8_benchmark_tarifaire.py # visualisations neutres
├── scripts/
│   ├── build_tariffs.py
│   ├── import_tariffs.py
│   ├── init_database.py        # schéma étendu (7 tables)
│   └── load_banks.py
├── ui/
│   ├── __init__.py
│   ├── render.py               # + presence_badge()
│   └── version.py
├── app.py                      # vue d'ensemble factuelle
├── README.md / README_EN.md
├── requirements.txt
└── LICENSE
```

## Auteur

**Maxime NDACLEU** - Data Analyst & Business Intelligence Analyst

<p align="left">
  <a href="https://github.com/maxin-dac">
    <img src="https://img.shields.io/badge/GitHub-maxin--dac-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/maximendacleu">
    <img src="https://img.shields.io/badge/LinkedIn-maximendacleu-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

## Licence

Projet distribué sous licence MIT. Données extraites des brochures tarifaires publiques des banques citées, fournies à des fins d'analyse et de comparaison.
