# 🏦 Cameroun Banking Benchmark — Observatoire de la Transparence Bancaire

**Problème :** l'information bancaire camerounaise est structurellement opaque : grilles tarifaires hétérogènes voire absentes, données financières publiées tardivement (ou jamais), et aucune vue comparative fiable du marché des 19 banques agréées.

**Solution :** un observatoire open source et bilingue qui mesure ce qui est **vérifiable** — la publication des tarifs, des informations financières, de la présence digitale et de la gouvernance — pour les 19 banques agréées par la COBAC, à partir de sources publiques officielles, tracées et datées.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Data-Sources_publiques-00693E?style=for-the-badge" alt="Données publiques" />
  <img src="https://img.shields.io/badge/Bilingue-FR_|_EN-008080?style=for-the-badge" alt="Bilingue FR EN" />
  <img src="https://img.shields.io/badge/Statut-En_cours-orange?style=for-the-badge" alt="Statut" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

> 🚧 **Travail en cours** : module tarifaire opérationnel (10 banques) ; modules financier et digital en cours de collecte.

🇬🇧 English : [README_EN.md](README_EN.md)

## En bref

- **Ce que ça fait** : évalue et compare les 19 banques agréées du Cameroun sur leur transparence (indice de publication) et compare les tarifs particuliers des 10 banques documentées sur un panier normalisé HT.
- **Compétences mobilisées** : data engineering, collecte manuelle, normalisation tarifaire, construction d'indicateurs composites, data visualisation, UX bilingue, dashboarding.
- **Démo** : bientôt en ligne (Streamlit Cloud).
- **Stack** : Python · Streamlit · Plotly · Pandas · SQLite · HTML · CSS.

## Fonctionnalités principales

- 🏆 **Indice de publication** : score /100 sur 4 piliers pondérés, classement des 19 banques agréées.
- 🔎 **Comparateur tarifaire** : sélection banques × services, meilleur/pire tarif surligné (175 lignes normalisées HT).
- 🏛️ **Profil banque** : identité, actionnariat, grille tarifaire, statuts de publication, sources cliquables.
- 📊 **Benchmark tarifaire** : virements SYSTAC/SYGMA, cartes GIMAC/Visa, retraits GAB, banque à distance.
- 🗺️ **Carte du marché** : 19 banques, sièges, actionnariat, statut de couverture.
- 📚 **Méthodologie affichée** : pondérations, seuils, limites — rien n'est masqué.

## Pourquoi pas de « score de compétitivité prix » ?

- Les grilles tarifaires ne sont pas uniformes (segments, packages, canaux) ; plusieurs banques ne publient rien.
- Les données financières sont difficilement accessibles et publiées tardivement en zone CEMAC.
- Comparer des prix sur une base hétérogène produirait un score trompeur.

→ Le projet mesure donc la **transparence** (ce qui est publié, vérifiable, à jour) : une proxy de gouvernance utile à un client, un investisseur ou un régulateur.

## Indice de publication

<details>
<summary>Pondération des piliers</summary>

| Poids | Pilier | Critères objectifs |
| --- | --- | --- |
| 30% | Tarifs | Grille publique ? PDF téléchargeable ? À jour (< 12 mois) ? Granularité particuliers/pros ? |
| 30% | Finance | Comptes publiés ? Délai de publication ? Auditeur (Big 4 / cabinet local) ? |
| 20% | Digital | Site fonctionnel ? App mobile notée ? Réseaux sociaux actifs ? |
| 20% | Gouvernance | Actionnariat public ? Dirigeants identifiés ? Rapport annuel narratif ? |

</details>

<details>
<summary>Signaux de publication</summary>

| Signal | Sévérité |
| --- | --- |
| Aucune grille tarifaire publique | 🔴 |
| Aucune information financière publiée | 🔴 |
| Grille tarifaire > 12 mois | 🟡 |
| Aucune app mobile notée | 🟡 |
| Grille publique à jour + comptes publiés | 🟢 |

</details>

Chaque critère est binaire ou ordinal et **sourcé** ; un pilier absent n'est pas compté 0 : il est exclu du calcul et signalé dans la couverture.

## Démarrage rapide

```bash
git clone https://github.com/maxin-dac/cameroon-banking-benchmark.git
cd cameroon-banking-benchmark
pip install -r requirements.txt
python scripts/init_database.py
python scripts/load_banks.py
python scripts/build_tariffs.py --clean
python scripts/import_tariffs.py
python scripts/seed_publication_criteria.py
streamlit run streamlit_app/app.py
```

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

## La transparence par conception

- **Pas de scraping** : collecte manuelle depuis des sources publiques officielles, dans le respect des CGU et de la loi n°2010/012 sur la cybersécurité.
- **Traçabilité** : chaque ligne porte sa source et sa date de consultation.
- **Honnêteté** : une donnée manquante est affichée comme telle, jamais estimée ni comblée artificiellement.
- **Pas de données personnelles**, pas de secret bancaire : uniquement des tarifs publics.
- **Outil d'aide à la décision** : ne remplace pas une étude approfondie ni les conditions officielles des banques.

## Limites

- Observation ponctuelle (août 2026) : les tarifs peuvent évoluer.
- Culture du reporting public faible en zone CEMAC : certaines banques ne publient rien → un indice bas est un résultat, pas un bug.
- L'indice mesure la transparence, pas la qualité ou la solidité d'une banque.
- Comparaisons tarifaires limitées aux 10 banques documentées et au panier particuliers normalisé.

## Structure du projet

```text
cameroon-banking-benchmark/
├── analytics/
│   ├── labels.py               # libellés FR des services et canaux
│   ├── publication_index.py    # indice de publication (4 piliers)
│   └── scoring.py              # panier tarifaire et comparaisons
├── data/
│   ├── db/                     # SQLite locale (gitignorée)
│   ├── processed/tariffs/      # tariffs_all_banks.csv (175 lignes HT)
│   ├── raw/documents/          # PDF sources (gitignorés)
│   └── reference/              # banks_reference.csv (19 banques), publication_criteria.csv
├── scripts/
│   ├── build_tariffs.py        # source de vérité des tarifs normalisés
│   ├── import_tariffs.py       # import + contrôles de validité
│   ├── init_database.py        # schéma SQLite
│   ├── load_banks.py           # référentiel des 19 banques
│   └── seed_publication_criteria.py
├── streamlit_app/
│   ├── app.py                  # vue d'ensemble
│   ├── assets/                 # theme.css + templates HTML (design system)
│   ├── pages/                  # comparateur, profil, benchmark, indice, méthodologie
│   └── ui/render.py            # composants HTML injectés
├── .gitignore
├── requirements.txt
├── LICENSE
├── README.md
└── README_EN.md
```

## Feuille de route

- [x] Référentiel des 19 banques agréées (noms légaux, sièges, actionnariat)
- [x] Normalisation tarifaire de 10 banques (175 lignes HT)
- [x] Dashboard Streamlit v1 (5 pages, thème personnalisé)
- [x] Indice de publication (4 piliers) + classement
- [ ] 🚧 Collecte financière (comptes publiés, délais, auditeurs)
- [ ] Collecte digitale (site, app mobile, réseaux sociaux)
- [ ] Carte du marché (actionnariat, gouvernance)
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

Projet distribué sous licence MIT. Données extraites des brochures tarifaires publiques des banques citées, fournies à des fins d'analyse et de comparaison.
