# 🌿 BloomWatch — NASA MODIS Vegetation Analysis (Muscat, Oman)

**BloomWatch** is an AI-powered environmental monitoring tool that visualizes real vegetation health data using NASA’s **MODIS MOD13Q1** satellite dataset.  
This version focuses on **Muscat, Oman**, analyzing NDVI (Normalized Difference Vegetation Index) and EVI (Enhanced Vegetation Index) over the last 12 months.

---

## 🛰️ Data Source

- **Dataset:** NASA MODIS MOD13Q1 v061  
- **Variables:** NDVI & EVI  
- **Region of Interest:** Muscat, Oman (2 km radius area)  
- **Time Range:** October 2024 – October 2025  
- **Data Processing:** Google Earth Engine (GEE)  
- **Export Format:** CSV (bloomwatch_muscat.csv)

The dataset was preprocessed in **Google Earth Engine** using the MOD13Q1 collection and exported to CSV for visualization.

---

## 🤖 AI Integration

BloomWatch includes a simple **AI-based bloom prediction model** that analyzes seasonal NDVI fluctuations to identify peak vegetation periods.  
The system uses Python (NumPy + pandas) logic to detect the **maximum NDVI point**, predicting when vegetation is at its healthiest — representing the bloom period.

Future versions will integrate machine learning to predict future bloom cycles based on multiple seasons of NASA satellite data.

---

## 🧰 Tools and Libraries

| Component | Technology Used |
|------------|-----------------|
| Interface | Streamlit |
| Data Source | NASA MODIS (via Google Earth Engine) |
| Visualization | Matplotlib |
| Analysis | NumPy, pandas |
| Language | Python 3.10+ |

---

## 🌍 Dashboard Features

✅ Real NASA satellite NDVI/EVI data  
✅ 12-month vegetation timeline visualization  
✅ Bloom prediction using AI logic  
✅ Simple and interactive interface  
✅ Built entirely with open-source tools  

---

## 📊 Example Visualization

![Dashboard Screenshot](web/images/muscat_dashboard_example.png)

> *NDVI/EVI trend over Muscat, Oman — showing bloom prediction from real NASA data.*

---

## 🚀 Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/<yourusername>/bloomwatch.git
   cd bloomwatch/web
