# inv_unidad02 — AGENTS.md

## Stack

- Python 3.13, managed with **uv** (`uv sync`, `uv add <pkg>`, `uv run <cmd>`)
- venv in `.venv/`
- Key deps: `statsmodels`, `linearmodels`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `openpyxl`, `scikit-learn`, `yfinance`, `pmdarima`, `lightgbm`, `xgboost`

## Entrypoints

| Script | Purpose |
|---|---|
| `src/main.py` | ENAHO data processing pipeline → `panel_ingreso_real_huanuco.xlsx` |
| `src/credito_real.py` | MCO with full diagnostics (time series, monthly) |
| `src/reporte.py` | ADL(1,2) model → `reporte_final.txt` + `panel_completo_modelo5.png` |
| `src/conectividad_vial.py` | Generates Excel workbook (Tema 1, distrital cross-section) |
| `src/credicorp.py` | OLS for Credicorp returns |
| `src/Obtener_bbdd.py` | Downloads financial data via yfinance → `data/processed/` |
| `src/econometria_basica.py` | Quick OLS from Google Sheets CSV |
| `main.py` (root) | **Empty** — use `src/main.py` instead |

## Commands

```sh
uv sync                          # install deps
uv add <pkg>                     # add dep
uv run python src/main.py        # ENAHO pipeline
uv run python src/credito_real.py
uv run python src/reporte.py
uv run python src/conectividad_vial.py
uv run jupyter lab               # launch notebooks
```

## Data

- Raw ENAHO CSVs go in `data/raw/` (**gitignored** — only `.gitkeep` or committed manually)
- `data/processed/` has pre-built datasets: `Base_datos.xlsx`, `base_datos_econometria.csv`, `BaseDatos_Vial_Huanuco.xlsx`, `bonos_verdes.csv`
- `.env` defines `RUTA_ABSOLUTA` for project root path

## Architecture notes

- Contains **multiple research topics** in one repo: Tema 1 (child malnutrition, cross-section), Tema 8 (road infrastructure & income, panel), credit analysis (time series ADL), Credicorp returns (financial OLS), climate/agriculture
- Two `main.py` files; the root one is **empty** — the real pipeline is `src/main.py`
- `src/config.py` holds province codes, ENAHO variable names
- `src/reporte.py` generates outputs in root (`reporte_final.txt`, `panel_completo_modelo5.png`)
- `reporte_final.txt` at root is a static copy of the full ADL model report
- Notebooks in `notebooks/` by topic: `datospanel/`, `investigaciones/`, `model/`, `RendimientosCredicorp/`
- R file at `R-files/init.R` is a stub

## Quirks

- ENAHO raw CSVs expected in `data/raw/` are not committed (gitignored pattern `data/raw/*.csv`)
- `.gitignoreecho` in root is a stray file (was created by accident)
- Root `main.py` is intentionally empty; never run it expecting the ENAHO pipeline
