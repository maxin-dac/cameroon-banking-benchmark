# 🏦 Cameroon Banking Benchmark - Banking Transparency Observatory

**Problem:** banking information in Cameroon is structurally opaque: heterogeneous or missing fee schedules, financial data published late (or never), and no reliable comparative view of the 19 licensed banks.

**Solution:** an open-source, bilingual observatory that measures what is **verifiable** - publication of fees, financial information, digital presence and governance - for the 19 COBAC-licensed banks, using traced and dated official public sources.

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

> 🚧 **Work in progress**: tariff module live (10 banks); financial and digital modules under collection.

🇫🇷 Français : [README.md](README.md)

## At a glance

- **What it does**: assesses and compares the 19 licensed banks of Cameroon on transparency (publication index) and compares retail fees of the 10 documented banks on a normalized pre-tax basket.
- **Skills**: data engineering, manual collection, fee normalization, composite indicator design, data visualization, bilingual UX, dashboarding.
- **Demo**: coming soon (Streamlit Cloud).
- **Stack**: Python · Streamlit · Plotly · Pandas · SQLite · HTML · CSS.

## Key features

- 🏆 **Publication index**: /100 score over 4 weighted pillars, ranking of the 19 licensed banks.
- 🔎 **Fee comparator**: bank × service selection, best/worst highlighted (175 normalized pre-tax rows).
- 🏛️ **Bank profile**: identity, ownership, fee grid, publication status, clickable sources.
- 📊 **Tariff benchmark**: SYSTAC/SYGMA transfers, GIMAC/Visa cards, ATM withdrawals, remote banking.
- 🗺️ **Market map**: 19 banks, headquarters, ownership, coverage status.
- 📚 **Displayed methodology**: weights, thresholds, limits - nothing hidden.

## Why no "price competitiveness score"?

- Fee schedules are not uniform (segments, packages, channels); several banks publish nothing.
- Financial data is hard to access and published late in the CEMAC zone.
- Comparing prices on a heterogeneous basis would produce a misleading score.

→ The project therefore measures **transparency** (what is published, verifiable, up to date): a governance proxy useful to a customer, an investor or a regulator.

## Publication index

<details>
<summary>Pillar weighting</summary>

| Weight | Pillar | Objective criteria |
| --- | --- | --- |
| 30% | Tariffs | Public schedule? Downloadable PDF? Up to date (< 12 months)? Retail/corporate granularity? |
| 30% | Finance | Accounts published? Publication delay? Auditor (Big 4 / local firm)? |
| 20% | Digital | Working website? Rated mobile app? Active social media? |
| 20% | Governance | Public ownership? Identified executives? Narrative annual report? |

</details>

<details>
<summary>Publication signals</summary>

| Signal | Severity |
| --- | --- |
| No public fee schedule | 🔴 |
| No published financial information | 🔴 |
| Fee schedule older than 12 months | 🟡 |
| No rated mobile app | 🟡 |
| Up-to-date public schedule + published accounts | 🟢 |

</details>

Every criterion is binary or ordinal and **sourced**; a missing pillar is not counted as 0: it is excluded from the computation and reported in the coverage.

## Quick start

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

## Data sources (tariff module)

**100% manual** collection, no scraping. Observation: **August 2026**. Full per-bank table with links and periods in the [French README](README.md#sources-des-données-module-tarifs).

## Transparency by design

- **No scraping**: manual collection from official public sources, respecting terms of service and Cameroon law n°2010/012 on cybersecurity.
- **Traceability**: every row carries its source and consultation date.
- **Honesty**: missing data is displayed as such, never estimated or artificially filled.
- **No personal data**, no banking secrecy: public fees only.
- **Decision-support tool**: does not replace an in-depth study or the banks' official conditions.

## Limits

- One-off observation (August 2026): fees may change.
- Weak public reporting culture in the CEMAC zone: some banks publish nothing → a low index is a result, not a bug.
- The index measures transparency, not the quality or soundness of a bank.
- Fee comparisons limited to the 10 documented banks and the normalized retail basket.

## Roadmap

- [x] Reference of the 19 licensed banks (legal names, HQ, ownership)
- [x] Tariff normalization for 10 banks (175 pre-tax rows)
- [x] Streamlit dashboard v1 (5 pages, custom theme)
- [x] Publication index (4 pillars) + ranking
- [ ] 🚧 Financial collection (published accounts, delays, auditors)
- [ ] Digital collection (website, mobile app, social media)
- [ ] Market map (ownership, governance)
- [ ] Streamlit Cloud deployment

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

MIT License. Data extracted from the cited banks' public fee brochures, provided for analysis and comparison purposes.
