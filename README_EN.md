# 🏦 Cameroon Banking Benchmark

> 🚧 **Work in progress.** The tariff module is live; the **financial data** and **digital presence** modules are being collected and will ship in an upcoming release.

**Problem:** retail banking fees in Cameroon are scattered across heterogeneous PDF brochures, hard to compare, and rarely presented in a structured, comparable and educational way.

**Solution:** an open-source platform that normalizes retail fees from 10 Cameroonian banks using official public sources, structures them into comparable services (pre-tax amounts, annual or per-operation basis) and computes a transparent, reproducible tariff competitiveness score.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Status-Work_in_progress-orange?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Data-Public_sources-00693E?style=for-the-badge" alt="Data" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

🇫🇷 Version française : [README_FR.txt](README_FR.txt)

## At a glance

- **What it does**: compares 10 Cameroonian banks on normalized retail fees, visualizes gaps per service and ranks banks by tariff competitiveness.
- **Skills**: data engineering, manual data curation, fee normalization, scoring, data visualization, dashboard UX.
- **Demo**: coming soon (Streamlit Cloud).
- **Stack**: Python · Streamlit · Plotly · Pandas · SQLite · HTML · CSS.

## Key features

- 🏆 **Overall ranking**: 0–100 tariff competitiveness score with progress bars and basket coverage.
- 🔎 **Fee comparator**: bank × service selection, best fee in green, highest in red.
- 🏛️ **Bank profile**: identity card (legal name, headquarters, website, official source) and full fee grid with readable labels.
- 📊 **Tariff benchmark**: Plotly charts sorted from cheapest to most expensive per basket service.
- 📚 **Methodology**: normalization rules, standard scenario, limits and disclaimers, fully transparent.
- 🧱 **Market standards**: services free everywhere are automatically detected and reported outside the score.

### Coming soon (work in progress)

- 💰 Financial benchmark (total assets, net banking income, net income, ROE/ROA) — collection in progress.
- 🌐 Digital benchmark (social media, mobile apps, website) — manual collection planned.
- 🛰️ Streamlit Cloud deployment.

## Methodology

| Rule | Choice |
| --- | --- |
| Scope | Retail customers only (salaried, non-salaried, students) |
| Amounts | XAF pre-tax (HT) |
| Recurring fees | Annualized (monthly × 12, quarterly × 4) |
| Transactional fees | Per operation, **no annual projection** |
| Variable formulas | Stored as-is; evaluated only under the 50,000 XAF scenario (peer-bank ATM withdrawal) |
| Channel | Digital-first when available |

<details>
<summary>Tariff competitiveness score</summary>

| Step | Rule |
| --- | --- |
| Standard basket | 10 comparable services (account maintenance, initial deposit, SYSTAC, SYGMA, ATM withdrawals, cards, internet banking, banker's cheque) |
| Per-service score | Robust ranking: cheapest = 100, most expensive = 0 |
| Global score | Average of available services (0–100) |
| Minimum coverage | 5/10 documented services to be ranked |
| Market standards | Items free everywhere excluded from the score and displayed separately |

</details>

## Data sources

**100% manual** collection from official public fee brochures (no scraping). Observation date: **2026-06-22**. The full source list with links and periods is available in the [French README](README_FR.txt).

## Ethics & compliance

- ✅ Manual collection from official public sources — **no scraping**, respecting terms of service and Cameroon law n°2010/012 on cybersecurity.
- ✅ No personal data, no banking secrecy: public fees only.
- ✅ Traceability: every row carries its source and consultation date.
- ⚠️ Decision-support tool: does not replace an in-depth study or the banks' official conditions.

## Limits

- One-off observation (2026-06-22): fees may change.
- Public grids sometimes partial (e.g. SCB): reduced coverage, bank unranked when applicable.
- The score is a pre-screening tool; normalization choices are analyst choices, documented and reproducible.

## Quick start

```bash
git clone https://github.com/maxin-dac/cameroon-banking-benchmark.git
cd cameroon-banking-benchmark
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

Data pipeline:

```bash
python scripts/build_tariffs.py --clean
python scripts/init_database.py
python scripts/load_banks.py
python scripts/import_tariffs.py
```

## Project structure

```text
cameroon-banking-benchmark/
├── analytics/
│   ├── labels.py               # FR labels for services and channels
│   └── scoring.py              # basket, score, market standards
├── data/
│   ├── db/                     # local artifact (gitignored)
│   ├── reference/
│   │   └── banks_reference.csv # 10-bank reference
│   └── processed/
│       └── tariffs/
│           └── tariffs_all_banks.csv
├── scripts/
│   ├── build_tariffs.py        # source of truth for normalized fees
│   ├── init_database.py
│   ├── load_banks.py
│   └── import_tariffs.py
├── streamlit_app/
│   ├── app.py                  # overview
│   ├── pages/                  # comparator, profile, benchmark, methodology
│   ├── ui/render.py            # injected HTML components
│   └── assets/
│       ├── css/theme.css       # design system (Fluent sidebar, flat canvas)
│       └── html/               # HTML templates (KPI, callouts, header…)
├── .gitignore
├── requirements.txt
├── LICENSE
├── README_FR.txt
└── README_EN.txt
```

## Roadmap

- [x] 10-bank reference (legal name, headquarters, website, official source)
- [x] Normalization of 175 retail fees (pre-tax)
- [x] Tariff competitiveness score & ranking
- [x] Streamlit dashboard (5 pages, custom theme)
- [ ] 🚧 Financial data collection (in progress)
- [ ] Financial benchmark (soundness)
- [ ] Manual digital presence collection
- [ ] Digital benchmark & composite score
- [ ] Streamlit Cloud deployment

## Author

**Maxime NDACLEU** — Data Analyst & Business Intelligence Analyst

<p align="left">
  <a href="https://github.com/maxin-dac">
    <img src="https://img.shields.io/badge/GitHub-maxin--dac-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/maximendacleu">
    <img src="https://img.shields.io/badge/LinkedIn-maximendacleu-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

## License

MIT License (see `LICENSE` file). Data extracted from the cited banks' public fee brochures, provided for analysis and comparison purposes.
