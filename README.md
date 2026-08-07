# 🏦 Cameroun Banking Benchmark

> 🚧 **Projet en cours de développement.** Le module tarifaire est fonctionnel ; les modules **données financières** et **présence digitale** sont en cours de collecte et arriveront dans une prochaine version.

**Problème :** les conditions tarifaires des banques camerounaises sont dispersées dans des brochures PDF hétérogènes, difficiles à comparer, et rarement présentées de manière structurée, comparable et pédagogique.

**Solution :** une plateforme open source qui normalise les tarifs particuliers de 10 banques camerounaises à partir de sources publiques officielles, les structure en services comparables (montants HT, base annuelle ou par opération) et calcule un score de compétitivité tarifaire transparent et reproductible.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Statut-Travail_en_cours-orange?style=for-the-badge" alt="Statut" />
  <img src="https://img.shields.io/badge/Données-Sources_publiques-00693E?style=for-the-badge" alt="Données" />
  <img src="https://img.shields.io/badge/Licence-MIT-green?style=for-the-badge" alt="Licence" />
</p>

🇬🇧 Version anglaise : [README_EN.md](README_EN.md)

## En bref

- **Ce que ça fait** : comparer 10 banques camerounaises sur leurs tarifs particuliers normalisés, visualiser les écarts par service et classer les banques selon un score de compétitivité tarifaire.
- **Compétences mobilisées** : data engineering, curation manuelle de données, normalisation tarifaire, scoring, data visualisation, UX dashboard.
- **Démo** : bientôt en ligne (Streamlit Cloud).
- **Stack** : Python · Streamlit · Plotly · Pandas · SQLite · HTML · CSS.

## Fonctionnalités principales

- 🏆 **Classement général** : score de compétitivité tarifaire 0–100 avec barres de progression et couverture du panier.
- 🔎 **Comparateur tarifaire** : sélection banques × services, meilleur tarif en vert, plus élevé en rouge.
- 🏛️ **Profil banque** : fiche d'identité (nom légal, siège, site, source officielle) et grille tarifaire complète en libellés lisibles.
- 📊 **Benchmark tarifaire** : graphiques Plotly triés du moins cher au plus cher par service du panier.
- 📚 **Méthodologie** : règles de normalisation, scénario standard, limites et avertissements, en toute transparence.
- 🧱 **Standards du marché** : services gratuits partout détectés automatiquement et reportés hors score.

### À venir (travail en cours)

- 💰 Benchmark financier (total bilan, PNB, résultat net, ROE/ROA) — collecte en cours.
- 🌐 Benchmark digital (réseaux sociaux, applications mobiles, site web) — collecte manuelle planifiée.
- 🛰️ Déploiement Streamlit Cloud.

## Méthodologie

| Règle | Choix |
| --- | --- |
| Périmètre | Particuliers uniquement (salariés, non salariés, étudiants) |
| Montants | XAF hors taxes (HT) |
| Frais récurrents | Annualisés (mensuel × 12, trimestriel × 4) |
| Frais transactionnels | Par opération, **sans projection annuelle** |
| Formules variables | Stockées telles quelles ; évaluées uniquement au scénario 50 000 XAF (retrait GAB confrère) |
| Canal | Digital prioritaire quand il existe |

<details>
<summary>Score de compétitivité tarifaire</summary>

| Étape | Règle |
| --- | --- |
| Panier standard | 10 services comparables (tenue de compte, dépôt initial, SYSTAC, SYGMA, retraits GAB, cartes, internet banking, chèque de banque) |
| Score par service | Classement robuste : le moins cher = 100, le plus cher = 0 |
| Score global | Moyenne des services disponibles (0–100) |
| Couverture minimale | 5/10 services documentés pour être classé |
| Standards du marché | Items gratuits partout exclus du score et affichés séparément |

</details>

## Sources des données

Collecte **100 % manuelle** sur les brochures tarifaires publiques officielles (aucun scraping). Observation : **2026-06-22**.

| Banque | Source officielle | Période |
| --- | --- | --- |
| Access Bank Cameroon | [Quarterly Banking Conditions](https://cameroon.accessbankplc.com/access/media/Media-PDF-Attachment/Quarterly-Banking-Conditions.pdf) | T3 2026 |
| Afriland First Bank | [Tarification Particuliers 2026](https://www.afrilandfirstbank.com/wp-content/uploads/2026/07/Tarification_AFB_Particulier_2026-2.pdf) | 2026 |
| BICEC | [Conditions de banque Particuliers](https://www.bicec.com/pdf/BICEC_Conditions%20de%20banque_Particuliers_VA-VF_Mars2026.pdf) | Mars 2026 |
| CCA-BANK | [Tarifaire T2 2026](https://www.cca-bank.com/assets/tarifaires/cca-bank-tarifaire-2e-trimestre-2026-fr.pdf) | T2 2026 |
| Commercial Bank Cameroon | [CB Particuliers](https://commercialbank-cm.com/wp-content/uploads/2019/09/CB-PARTICULIERS-OCT-2025.pdf) | 01/10/2025 |
| SCB Cameroun | [Conditions de banque T2 2026](https://www.scbcameroun.net/conditions-tarifaires-scbcameroun/29-les-conditions-de-banque-du-t2-2026/file) | T2 2026 |
| Société Générale Cameroun | [Conditions tarifaires T3 2026](https://particuliers.societegenerale.cm/fileadmin/user_upload/Cameroun/PDF/2026/T3_-_2026/CLIPRI-T-3-2026-60X80-VF.pdf) | 01/07/2026 |
| UBA Cameroun | [Conditions de banque](https://www.ubacameroon.com/wp-content/uploads/sites/8/2026/08/CONDITIONS-DE-BANQUE-APPLICABLES-A-LA-CLIENTELE-JUILLET-SEPTEMBRE-2026.pdf) | Juil.–Sept. 2026 |
| Africa Golden Bank | [Condition de banque T2 2025](https://africagoldenbank.com/wp-content/uploads/2025/06/CONDITION-DE-BANQUE-2e-trimestre-2025.pdf) | T2 2025 |
| AFG Bank Cameroon | [Grille tarifaire Juillet 2026](https://afgbank.cm/files/2026/07/Press-Version-Press-CONDITION-FR-2026-Juillet.pdf) | 01/07/2026 |

## Éthique & conformité

- ✅ Collecte manuelle depuis des sources publiques officielles — **aucun scraping**, respect des CGU et de la loi n°2010/012 sur la cybersécurité.
- ✅ Aucune donnée personnelle, aucun secret bancaire : uniquement des tarifs publics.
- ✅ Traçabilité : chaque ligne de la base porte sa source et sa date de consultation.
- ⚠️ Outil d'aide à la décision : ne remplace pas une étude approfondie ni les conditions officielles des banques.

## Limites

- Observation ponctuelle (2026-06-22) : les tarifs peuvent évoluer.
- Grilles publiques parfois partielles (ex. SCB) → couverture réduite, banque non classée le cas échéant.
- Le score est un outil de pré-criblage ; les choix de normalisation sont des choix d'analyste, documentés et reproductibles.

## Démarrage rapide

```bash
git clone https://github.com/maxin-dac/cameroon-banking-benchmark.git
cd cameroon-banking-benchmark
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

Pipeline de données :

```bash
python scripts/build_tariffs.py --clean   # reconstruit le CSV normalisé (175 lignes)
python scripts/init_database.py           # crée la base SQLite
python scripts/load_banks.py              # charge le référentiel des 10 banques
python scripts/import_tariffs.py          # importe les tarifs
```

## Structure du projet

```text
cameroon-banking-benchmark/
├── analytics/
│   ├── labels.py               # libellés FR des services et canaux
│   └── scoring.py              # panier, score, standards du marché
├── data/
│   ├── db/                     # artefact local (gitignoré)
│   ├── reference/
│   │   └── banks_reference.csv # référentiel des 10 banques
│   └── processed/
│       └── tariffs/
│           └── tariffs_all_banks.csv
├── scripts/
│   ├── build_tariffs.py        # source de vérité des tarifs normalisés
│   ├── init_database.py
│   ├── load_banks.py
│   └── import_tariffs.py
├── streamlit_app/
│   ├── app.py                  # vue d'ensemble
│   ├── pages/                  # comparateur, profil, benchmark, méthodologie
│   ├── ui/render.py            # composants HTML injectés
│   └── assets/
│       ├── css/theme.css       # design system (sidebar Fluent, canvas flat)
│       └── html/               # templates HTML (KPI, callouts, header…)
├── .gitignore
├── requirements.txt
├── LICENSE
├── README_FR.txt
└── README_EN.txt
```

## Feuille de route

- [x] Référentiel des 10 banques (nom légal, siège, site, source officielle)
- [x] Normalisation de 175 tarifs particuliers HT
- [x] Score de compétitivité tarifaire & classement
- [x] Dashboard Streamlit (5 pages, thème personnalisé)
- [ ] 🚧 Collecte des données financières (en cours)
- [ ] Benchmark financier (solidité)
- [ ] Collecte manuelle de la présence digitale
- [ ] Benchmark digital & score composite
- [ ] Déploiement Streamlit Cloud

## Auteur

**Maxime NDACLEU** — Data Analyst & Business Intelligence Analyst

<p align="left">
  <a href="https://github.com/maxin-dac">
    <img src="https://img.shields.io/badge/GitHub-maxin--dac-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/maximendacleu">
    <img src="https://img.shields.io/badge/LinkedIn-maximendacleu-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

## Licence

Projet distribué sous licence MIT (voir fichier `LICENSE`). Données issues des brochures tarifaires publiques des banques citées, fournies à des fins d'analyse et de comparaison.
