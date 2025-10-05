# BloomWatch — Global Flowering Phenology from Space

**Tagline:** Detecting and mapping bloom onset using NASA satellite indices and AI time-series models.

## Overview
BloomWatch uses NASA vegetation products (MODIS/VIIRS) to detect bloom onset across regions. We generate NDVI/EVI time series, apply an LSTM-based classifier with an XGBoost verifier, and visualize results in a Streamlit dashboard.

## Repo Contents
- `gee/bloomwatch_gee.js` — Google Earth Engine script to export NDVI/EVI time series.
- `src/train_model.py` — Train an LSTM + XGBoost ensemble on exported time series.
- `src/predict.py` — Predict bloom onset for new time series.
- `web/dashboard.py` — Streamlit dashboard (demo uses synthetic data).
- `docs/` — Submission checklist and (optional) video script.
- `assets/` — (place logos/figures here).

## Quickstart (dashboard)
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run web/dashboard.py
```

## Data (NASA products)
- MODIS MOD13Q1: NDVI/EVI, 16-day, 250 m
- VIIRS VNP13A1: NDVI/EVI, 16-day, 500 m
- MCD12Q2: Land surface phenology metrics (validation)

## Export time series with GEE
Open `gee/bloomwatch_gee.js` in the Earth Engine Code Editor, set your region/date, and export a CSV to Drive. Download into `data/exports/` before training.

## Train & Predict (optional)
```bash
pip install -r requirements-train.txt
python src/train_model.py --data data/exports/ --out models/
python src/predict.py --input data/exports/<file>.csv --out results/bloom.json
```

## License
MIT — see `LICENSE`.