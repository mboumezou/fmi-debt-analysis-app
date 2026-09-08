# IMF Sovereign Debt Visualizer

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Data%20App-FF4B4B?logo=streamlit&logoColor=white)
![Data](https://img.shields.io/badge/Data-IMF%20Sovereign%20Debt-1B365D)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive Streamlit application for analysing sovereign debt structures across advanced economies using data from the IMF Investor Base Sovereign Debt Database.

## Questions explored

- How is a country's sovereign debt split between domestic and foreign investor groups?
- How does investor composition evolve through time?
- How do countries compare at a selected quarter?
- What relationship appears between debt-to-GDP and the foreign-investor share?

## Features

- Country-level debt composition through stacked area charts.
- Cross-country comparison at a selected date.
- Debt-to-GDP versus foreign-investor-share scatter analysis.
- Consistent country labels and quarter selection across views.
- Interactive Plotly charts in a multi-page Streamlit interface.

## Data

The project uses the **IMF Investor Base Sovereign Debt Database**, compiled by the IMF Monetary and Capital Markets Department, with coverage from 1989Q4 to 2024Q2 in the included snapshot. Supporting files provide holdings, debt-to-GDP and exchange-rate inputs.

## Run locally

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Repository structure

```text
.
├── streamlit_app.py                    # Main English application
├── backup.py                           # French-language version
├── Database_For_Posting_AM_Frozen.xlsx # Consolidated data snapshot
├── Holdings.csv
├── DebtToGDP.csv
├── ExchangeRates.csv
├── requirements.txt
└── LICENSE
```

## Scope

The dashboard is intended for exploratory sovereign-risk analysis. Cross-country comparisons remain sensitive to definitions, reporting coverage, exchange-rate treatment and data availability.

## Author

Mohamed Boumezou — Finance student at Université Paris Dauphine–PSL  
[LinkedIn](https://www.linkedin.com/in/mohamed-boumezou-a8a0052ab/)
