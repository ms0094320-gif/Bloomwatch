# BloomWatch — Global Flowering Phenology from Space

**Tagline:** Detecting and mapping bloom onset using NASA satellite indices and AI time-series models.

## Overview
Flowering phenology is a sensitive indicator of ecosystem health, pollinator timing, and climate-driven shifts. BloomWatch uses NASA vegetation products (MODIS/VIIRS) to detect bloom onset across regions. We generate NDVI/EVI time series, apply an LSTM-based classifier with an XGBoost verifier, and visualize results in a Streamlit dashboard.

## Repository Contents
- `gee/bloomwatch_gee.js` — Google Earth Engine script to export NDVI/EVI time series.
- `src/train_model.py` — Train an LSTM + XGBoost ensemble on exported time series.
- `src/predict.py` — Predict bloom onset for new time series.
- `web/dashboard.py` — Streamlit dashboard (demo-ready with synthetic data).
- `docs/` — Submission checklist and video script.
- `assets/` — Logo and slide visuals.

## Quickstart
1. (Optional) Create a virtual environment
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard (synthetic demo data)
   ```bash
   streamlit run web/dashboard.py
   ```

## Data (NASA products)
- **MODIS MOD13Q1:** NDVI/EVI, 16-day, 250 m
- **VIIRS VNP13A1:** NDVI/EVI, 16-day, 500 m
- **MCD12Q2:** Annual land surface phenology metrics (validation)

## How to export time series with GEE
- Open the script in `gee/bloomwatch_gee.js` in the Earth Engine Code Editor.
- Set your region and date range; export a CSV to Google Drive.
- Download the CSV into `data/exports/` before training.

## Training and prediction
```bash
python src/train_model.py --data data/exports/ --out models/
python src/predict.py --input data/exports/sample.csv --out results/sample_bloom.json
```

## License
MIT — see `LICENSE`.