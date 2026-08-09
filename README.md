# 🏦 Cameroun Banking Benchmark — Observatoire de la Transparence Bancaire

> 🚧 **Projet en cours de développement.** Module tarifaire fonctionnel (10 banques documentées) ; l'indice de transparence sur les 19 banques agréées et les modules financier/digital sont en cours de construction.

**Problème :** l'information bancaire camerounaise est structurellement opaque : grilles tarifaires hétérogènes voire absentes, données financières publiées tardivement (ou jamais), et aucune vue comparative fiable du marché des 19 banques agréées.

**Solution :** un observatoire open source qui mesure ce qui est **vérifiable** : la transparence. Chaque banque agréée est évaluée sur quatre piliers objectifs (tarifs, finance, digital, gouvernance), à partir de sources publiques tracées et datées.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Marché-19_banques_agréées-00693E?style=for-the-badge" alt="19 banques" />
  <img src="https://img.shields.io/badge/Statut-Travail_en_cours-orange?style=for-the-badge" alt="Statut" />
  <img src="https://img.shields.io/badge/Bilingue-FR_|_EN-008080?style=for-the-badge" alt="Bilingue" />
  <img src="https://img.shields.io/badge/Licence-MIT-green?style=for-the-badge" alt="Licence" />
</p>

🇬🇧 Version anglaise : [README_EN.txt](README_EN.txt)

## En bref

- **Périmètre officiel** : les 19 banques agréées au Cameroun.
- **Module tarifs** : 10 banques documentées par collecte manuelle (175 lignes normalisées HT).
- **Indice de transparence** : 4 piliers pondérés, 100 % vérifiables, aucune estimation.
- **Décision méthodologique** : pas de score de compétitivité prix — on mesure la transparence, pas le prix.
- **Stack** : Python · Streamlit · Plotly · Pandas · SQLite · HTML · CSS.

## Pourquoi pas de « score de compétitivité tarifaire » ?

Décision documentée :

1. Les grilles tarifaires ne sont pas uniformes d'une banque à l'autre (segments, packages, canaux) ; plusieurs banques ne publient rien.
2. Les données financières sont difficilement accessibles et publiées avec des délais tardifs.
3. Comparer des prix sur une base hétérogène produirait un score trompeur.

→ Le projet mesure donc la **transparence** (ce qui est publié, vérifiable et à jour), une proxy de la qualité de gouvernance utile pour un client, un investisseur ou un régulateur.

## Indice de transparence (4 piliers)

| Pilier | Poids | Critères objectifs |
| --- | --- | --- |
| Tarifs | 30 % | Grille publique ? PDF téléchargeable ? À jour ? Granularité particuliers/pros ? |
| Finance | 30 % | Comptes publiés ? Délai de publication ? Auditeur (Big 4 / cabinet local) ? |
| Digital | 20 % | Site fonctionnel ? App mobile notée ? Réseaux sociaux actifs ? |
| Gouvernance | 20 % | Actionnariat public ? Dirigeants identifiés ? Rapport annuel narratif ? |

Chaque critère est binaire ou ordinal et **sourcé** ; aucun critère n'est estimé.

## Périmètre : les 19 banques agréées

| Code | Banque | Siège | Tarifs publics |
| --- | --- | --- | --- |
| ACCESS | Access Bank | Douala | ✅ documentés |
| AGB | Africa Golden Bank | Douala | ✅ documentés |
| AFRILAND | Afriland First Bank | Douala | ✅ documentés |
| AFG | AFG Bank Cameroun | Douala | ✅ documentés |
| BICEC | BICEC | Douala | ✅ documentés |
| CBC | Commercial Bank | Douala | ✅ documentés |
| CCA | CCA-BANK | Douala | ✅ documentés |
| SCB | SCB Cameroun | Douala | ✅ documentés |
| SGC | Société Générale Cameroun | Douala | ✅ documentés |
| UBA | UBA Cameroun | Douala | ✅ documentés |
| BANGE | BANGE Bank Cameroun | Yaoundé | ⬜ à collecter |
| BCPME | BC-PME | Douala | ⬜ à collecter |
| BGFI | BGFIBANK Cameroun | Douala | ⬜ à collecter |
| CITI | Citibank Cameroun | Douala | ⬜ à collecter |
| ECOBANK | Ecobank Cameroun | Douala | ⬜ à collecter |
| REGIONALE | La Régionale Bank | Yaoundé | ⬜ à collecter |
| NFC | NFC-Bank | Yaoundé | ⬜ à collecter |
| SCBC | Standard Chartered Bank Cameroon | Douala | ⬜ à collecter |
| UBC | Union Bank of Cameroon | Douala | ⬜ à collecter |

## Fonctionnalités

- 🏆 Classement de transparence des 19 banques.
- 🔎 Comparateur tarifaire (10 banques documentées), meilleur/pire en couleur.
- 🏛️ Profil banque : identité, grille, sources, statut de publication.
- 📊 Benchmark tarifaire par service (SYSTAC, cartes, retraits GAB…).
- 🗺️ Carte du marché : sièges, actionnariat, statut de transparence.
- 📚 Méthodologie et limites en toute transparence.

## Sources des données (module tarifs)

Collecte **100 % manuelle** sur les brochures publiques officielles (aucun scraping). Observation : **2026-06-22**.

| Banque | Source officielle | Période |
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

## Éthique & conformité

- ✅ Collecte manuelle depuis des sources publiques officielles — **aucun scraping**, respect des CGU et de la loi n°2010/012 sur la cybersécurité.
- ✅ Aucune donnée personnelle, aucun secret bancaire : uniquement des tarifs publics.
- ✅ Traçabilité : chaque ligne de la base porte sa source et sa date de consultation.
- ⚠️ Outil d'aide à la décision : ne remplace pas une étude approfondie ni les conditions officielles des banques.

## Limites

- Observation ponctuelle (2026-06-22) : les tarifs peuvent évoluer.
- En zone CEMAC, la culture du reporting public est faible : certaines banques ne publient rien → leur indice de transparence sera faible, ce qui est un résultat en soi, pas un bug.
- L'indice mesure la transparence, pas la qualité ou la solidité de la banque.

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
python scripts/load_banks.py              # charge le référentiel des 19 banques
python scripts/import_tariffs.py          # importe les tarifs
```

## Structure du projet

```text
cameroon-banking-benchmark/
├── analytics/
│   ├── labels.py               # libellés FR des services et canaux
│   ├── scoring.py              # panier tarifaire et comparaisons
│   └── transparency.py         # indice de transparence (4 piliers)
├── data/
│   ├── db/                     # artefact local (gitignoré)
│   ├── reference/
│   │   └── banks_reference.csv # référentiel des 19 banques agréées
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
│   ├── pages/                  # comparateur, profil, benchmark, transparence, méthodo
│   ├── ui/render.py            # composants HTML injectés
│   └── assets/                 # theme.css + templates HTML
├── .gitignore
├── requirements.txt
├── LICENSE
├── README_FR.txt
└── README_EN.txt
```

## Feuille de route

- [x] Référentiel des 19 banques agréées (noms légaux, sièges, actionnariat)
- [x] Normalisation tarifaire de 10 banques (175 lignes HT)
- [x] Dashboard Streamlit v1 (comparateur, profil, benchmark)
- [ ] 🚧 Indice de transparence (4 piliers) + classement des 19 banques
- [ ] Collecte financière (comptes publiés, délais, auditeurs)
- [ ] Collecte digitale (site, app mobile, réseaux sociaux)
- [ ] Carte du marché (sièges, actionnariat, gouvernance)
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
