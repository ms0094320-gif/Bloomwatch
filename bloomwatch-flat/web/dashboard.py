import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os

# -------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------
st.set_page_config(page_title='BloomWatch: NASA MODIS', layout='wide')
st.title("🌿 BloomWatch: Multi-Region Vegetation Analysis")
st.markdown("""
**BloomWatch** visualizes vegetation health using **real NASA MODIS MOD13Q1 data**  
exported from **Google Earth Engine**. Select a region to analyze bloom trends based on NDVI and EVI indices.
""")

# -------------------------------------------------------
# REGION SELECTION
# -------------------------------------------------------
st.sidebar.title("🌍 Select Region")
region = st.sidebar.selectbox("Choose a region", ["Muscat, Oman", "Arizona, USA"])

region_file_map = {
    "Muscat, Oman": "bloomwatch_muscat.csv",
    "Arizona, USA": "bloomwatch_arizona.csv"
}

file_path = None
for path in glob.glob("data/exports/*.csv"):
    if region_file_map[region] in path:
        file_path = path
        break

if not file_path:
    st.error(f"🚨 Could not find CSV for {region}. Expected `{region_file_map[region]}` in data/exports/")
    st.stop()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = pd.read_csv(file_path)
st.success(f"✅ Loaded NASA MODIS dataset for **{region}**")

if 'time' not in df.columns:
    st.error("CSV must include a 'time' column with timestamps.")
    st.stop()

df['time'] = pd.to_datetime(df['time'], errors='coerce')
df = df.sort_values('time')
df = df.dropna(subset=['NDVI', 'EVI'])
df = df.reset_index(drop=True)
df['Month'] = df['time'].dt.strftime('%b %Y')

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------
unique_years = sorted(df['time'].dt.year.unique())

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
# BLOOM PREDICTION
# -------------------------------------------------------
idx = int(np.argmax(df['NDVI'][:months]))
bloom_date = df['Month'].iloc[idx]
bloom_value = df['NDVI'].iloc[idx]

# -------------------------------------------------------
# PLOT
# -------------------------------------------------------
st.subheader(f"📈 NDVI / EVI Time Series — {region}")

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
ax.set_xlabel("Time")
ax.set_ylabel("Vegetation Index Value")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.markdown("---")
st.caption(f"""
🛰 **Data Source:** NASA MODIS MOD13Q1 (NDVI/EVI, 16-day composite, 250 m resolution)  
📍 **Region:** {region}  
⚙️ **Processed via:** Google Earth Engine  
🌱 **Purpose:** Compare vegetation bloom cycles across regions.
""")
