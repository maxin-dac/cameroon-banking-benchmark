# 🏦 Cameroon Banking Benchmark - Banking Transparency Observatory

🚧 ***Work in progress***

Faced with financial opacity and the heterogeneity of pricing structures within the CEMAC zone in general and in Cameroon in particular, we are developing a standardized comparative analysis framework. This framework is based on the standardization of 175 pre-tax pricing lines collected from official sources. Still being finalized, this project will also incorporate a comprehensive consolidation of regional banking regulations.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Data-Public_sources-00693E?style=for-the-badge" alt="Public sources" />
  <img src="https://img.shields.io/badge/Bilingual-FR_|_EN-008080?style=for-the-badge" alt="Bilingual FR EN" />
  <img src="https://img.shields.io/badge/Status-Work_in_progress-orange?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

🇫🇷 Français : [README.md](README.md)

## Data sources (tariffs module)

100% manual collection, no scraping. Observation: August 2026.

| Bank | Source | Period |
| --- | --- | --- |
| Access Bank | [Quarterly Banking Conditions](https://cameroon.accessbankplc.com/access/media/Media-PDF-Attachment/Quarterly-Banking-Conditions.pdf) | Q3 2026 |
| Afriland First Bank | [Retail Fee Schedule 2026](https://www.afrilandfirstbank.com/wp-content/uploads/2026/07/Tarification_AFB_Particulier_2026-2.pdf) | 2026 |
| BICEC | [Retail Banking Conditions](https://www.bicec.com/pdf/BICEC_Conditions%20de%20banque_Particuliers_VA-VF_Mars2026.pdf) | March 2026 |
| CCA-BANK | [Fee Schedule Q2 2026](https://www.cca-bank.com/assets/tarifaires/cca-bank-tarifaire-2e-trimestre-2026-fr.pdf) | Q2 2026 |
| Commercial Bank | [CB Retail](https://commercialbank-cm.com/wp-content/uploads/2019/09/CB-PARTICULIERS-OCT-2025.pdf) | 01/10/2025 |
| SCB Cameroon | [Banking Conditions Q2 2026](https://www.scbcameroun.net/conditions-tarifaires-scbcameroun/29-les-conditions-de-banque-du-t2-2026/file) | Q2 2026 |
| Société Générale | [Fee Schedule Q3 2026](https://particuliers.societegenerale.cm/fileadmin/user_upload/Cameroun/PDF/2026/T3_-_2026/CLIPRI-T-3-2026-60X80-VF.pdf) | 01/07/2026 |
| UBA | [Banking Conditions](https://www.ubacameroon.com/wp-content/uploads/sites/8/2026/08/CONDITIONS-DE-BANQUE-APPLICABLES-A-LA-CLIENTELE-JUILLET-SEPTEMBRE-2026.pdf) | July–Sept. 2026 |
| Africa Golden Bank | [Banking Conditions Q2 2025](https://africagoldenbank.com/wp-content/uploads/2025/06/CONDITION-DE-BANQUE-2e-trimestre-2025.pdf) | Q2 2025 |
| AFG Bank | [Fee Schedule July 2026](https://afgbank.cm/files/2026/07/Press-Version-Press-CONDITION-FR-2026-Juillet.pdf) | 01/07/2026 |
| 9 other licensed banks | Manual collection (websites, COBAC, press) | in progress |

## Transparency by design

- No scraping: manual collection from official public sources, in compliance with terms of service and law n°2010/012 on cybersecurity.
- Traceability: each row carries its source and consultation date.
- Honesty: missing data is displayed as such, never estimated nor artificially filled.
- No personal data, no banking secrecy: only public fee schedules.
- Decision-support tool: does not replace an in-depth study nor the banks' official terms.

## Limitations

- One-off observation (August 2026): fees may change.
- Weak public reporting culture in the CEMAC zone: some banks do not publish their fee schedule.
- Tariff comparisons limited to the 10 documented banks and the normalized retail basket.

## Project structure

```text
cameroon-banking-benchmark/
 ├── analytics/
 │   ├── __init__.py
 │   ├── labels.py
 │   └── scoring.py              # tariff comparisons (no global score)
 ├── assets/                     # css + html templates
 ├── data/
 │   ├── db/banking_benchmark.db
 │   ├── processed/tariffs/tariffs_all_banks.csv
 │   ├── raw/documents/          # source PDFs (gitignored)
 │   └── reference/
 │       ├── banks_reference.csv
 │       ├── regulations_cemac.csv        # NEW (being collected)
 │       ├── institutions.csv             # NEW
 │       ├── market_indicators_template.csv   # NEW (being collected)
 │       └── bank_governance_template.csv     # NEW (org charts)
 ├── pages/
 │   ├── 1_comparateur.py
 │   ├── 2_profil_banque.py      # + org chart
 │   ├── 3_benchmark_tarifaire.py
 │   ├── 4_methodologie.py
 │   ├── 5_cadre_juridique.py    # NEW
 │   └── 6_marche_bancaire.py    # NEW
 ├── scripts/
 │   ├── build_tariffs.py
 │   ├── import_tariffs.py
 │   ├── init_database.py
 │   ├── load_banks.py
 │   ├── import_regulations.py   # NEW
 │   └── import_market.py        # NEW
 ├── ui/
 │   ├── __init__.py
 │   └── render.py
 ├── app.py                      # root
 ├── README.md / README_EN.md
 ├── requirements.txt
 └── LICENSE
```

## Author

**Maxime NDACLEU** - Data Analyst & Business Intelligence Analyst

<p align="left">
  <a href="https://github.com/maxin-dac">
    <img src="https://img.shields.io/badge/GitHub-maxin--dac-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/maximendacleu">
    <img src="https://img.shields.io/badge/LinkedIn-maximendacleu-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

## License

Project distributed under the MIT License. Data extracted from the public fee brochures of the cited banks, provided for analysis and comparison purposes.