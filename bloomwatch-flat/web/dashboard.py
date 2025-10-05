import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os

# -------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------
st.set_page_config(page_title='BloomWatch: NASA MODIS', layout='wide')
st.title("🌿 BloomWatch: Real NASA MODIS Vegetation Data")
st.markdown("""
**BloomWatch** visualizes real vegetation health data from NASA’s MODIS MOD13Q1 collection.  
This dashboard analyzes **NDVI** (Normalized Difference Vegetation Index) and **EVI** (Enhanced Vegetation Index)
exported from **Google Earth Engine** for a 2 km radius area near **Muscat, Oman (2021–2024)**.
""")

# -------------------------------------------------------
# LOAD REAL CSV DATA
# -------------------------------------------------------
csv_files = sorted(glob.glob("data/exports/*.csv"))

if csv_files:
    file_path = csv_files[0]  # use first CSV found
    df = pd.read_csv(file_path)
    st.success(f"✅ Loaded real NASA MODIS dataset: `{os.path.basename(file_path)}`")
else:
    st.error("🚨 No CSV file found in `data/exports/`. Please add your exported file.")
    st.stop()

# -------------------------------------------------------
# CLEAN AND PREPARE DATA
# -------------------------------------------------------
# Convert time to datetime
if 'time' in df.columns:
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
else:
    st.error("CSV must include a 'time' column with timestamps from Earth Engine.")
    st.stop()

# Sort and clean
df = df.sort_values('time')
df = df.dropna(subset=['NDVI', 'EVI'])
df = df.reset_index(drop=True)

# Extract month for labeling
df['Month'] = df['time'].dt.strftime('%b %Y')

# -------------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------------
st.sidebar.title("🌱 Display Options")

unique_years = sorted(df['time'].dt.year.unique())

# Handle one-year datasets safely
if len(unique_years) > 1:
    year_range = st.sidebar.slider(
        "Select year range",
        int(unique_years[0]),
        int(unique_years[-1]),
        (int(unique_years[0]), int(unique_years[-1]))
    )
    df = df[(df['time'].dt.year >= year_range[0]) & (df['time'].dt.year <= year_range[1])]
else:
    st.sidebar.info(f"Data covers only one year: {unique_years[0]}")

months = st.sidebar.slider("Months to display", 6, len(df), 24, 1)

# -------------------------------------------------------
# PREDICT BLOOM
# -------------------------------------------------------
idx = int(np.argmax(df['NDVI'][:months]))
bloom_date = df['Month'].iloc[idx]
bloom_value = df['NDVI'].iloc[idx]

# -------------------------------------------------------
# PLOT CHART
# -------------------------------------------------------
st.subheader("📈 NDVI / EVI Time Series — Muscat, Oman")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Month'][:months], df['NDVI'][:months], marker='o', label='NDVI')
ax.plot(df['Month'][:months], df['EVI'][:months], marker='o', label='EVI')
ax.axvline(x=bloom_date, linestyle='--', color='gray')
ax.annotate(f'Predicted Bloom\n({bloom_date})',
            xy=(idx, bloom_value),
            xytext=(idx + 0.5, bloom_value + 0.02),
            arrowprops=dict(arrowstyle='->', lw=1.2),
            fontsize=9)
ax.set_ylim(0, max(0.9, float(df[['NDVI','EVI']].max().max()) + 0.1))
ax.set_xlabel("Time (2021–2024)")
ax.set_ylabel("Vegetation Index Value")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.markdown("---")
st.caption("""
🛰 **Data Source:** NASA MODIS MOD13Q1 (NDVI/EVI, 16-day composite, 250m resolution)  
📍 **Region:** Muscat, Oman (2 km radius)  
📅 **Time range:** 2021–2024  
⚙️ **Processed via:** Google Earth Engine  
🌱 **Purpose:** Analyze real vegetation patterns and detect bloom timing.
""")
