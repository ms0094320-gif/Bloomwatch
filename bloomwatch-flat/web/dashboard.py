import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------
st.set_page_config(page_title='BloomWatch: NASA MODIS', layout='wide')
st.title("🌿 BloomWatch: Real NASA MODIS Data (Last 12 Months)")
st.markdown("""
**BloomWatch** visualizes vegetation health using real satellite data from NASA’s **MODIS MOD13Q1** collection.  
Choose between **Muscat, Oman** and **Arizona, USA** to explore regional bloom trends from the past 12 months.
""")

# -------------------------------------------------------
# REGION SELECTION
# -------------------------------------------------------
st.sidebar.title("🌍 Select Region")
region = st.sidebar.selectbox("Choose a region", ["Muscat, Oman", "Arizona, USA"])

# Define folder paths for each region
region_paths = {
    "Muscat, Oman": "data/muscat/bloomwatch_muscat.csv",
    "Arizona, USA": "data/arizona/bloomwatch_arizona.csv"
}

# Get file path based on region
file_path = os.path.join(os.path.dirname(__file__), region_paths[region])

if not os.path.exists(file_path):
    st.error(f"🚨 Could not find data file for {region}. Expected at: {file_path}")
    st.stop()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = pd.read_csv(file_path)
st.success(f"✅ Loaded NASA MODIS dataset for **{region}**")

# Fix time format (Earth Engine timestamps are in milliseconds)
if 'time' not in df.columns:
    st.error("CSV must include a 'time' column with timestamps from Earth Engine.")
    st.stop()

if df['time'].dtype in ['int64', 'float64']:
    df['time'] = pd.to_datetime(df['time'], unit='ms', errors='coerce')
else:
    df['time'] = pd.to_datetime(df['time'], errors='coerce')

# Clean & prepare
df = df.sort_values('time').dropna(subset=['NDVI', 'EVI']).reset_index(drop=True)
df['Month'] = df['time'].dt.strftime('%b %Y')

# -------------------------------------------------------
# FILTER LAST 12 MONTHS
# -------------------------------------------------------
latest_date = df['time'].max()
start_date = latest_date - pd.DateOffset(months=12)
df_12 = df[df['time'] >= start_date]

if df_12.empty:
    st.warning("⚠️ No data found for the past 12 months.")
    st.stop()

# -------------------------------------------------------
# PREDICT BLOOM
# -------------------------------------------------------
idx = int(np.argmax(df_12['NDVI']))
bloom_date = df_12['Month'].iloc[idx]
bloom_value = df_12['NDVI'].iloc[idx]

# -------------------------------------------------------
# CHART
# -------------------------------------------------------
st.subheader(f"📈 NDVI / EVI Time Series — {region} (Last 12 Months)")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_12['Month'], df_12['NDVI'], marker='o', label='NDVI')
ax.plot(df_12['Month'], df_12['EVI'], marker='o', label='EVI')
ax.axvline(x=bloom_date, linestyle='--', color='gray')
ax.annotate(f'Predicted Bloom\n({bloom_date})',
            xy=(idx, bloom_value),
            xytext=(idx + 0.5, bloom_value + 0.02),
            arrowprops=dict(arrowstyle='->', lw=1.2),
            fontsize=9)
ax.set_ylim(0, max(0.9, float(df_12[['NDVI','EVI']].max().max()) + 0.1))
ax.set_xlabel("Time (Last 12 Months)")
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
📅 **Time Range:** Last 12 months (Oct 2024 – Oct 2025)  
⚙️ **Processed via:** Google Earth Engine  
🌱 **Purpose:** Analyze and compare vegetation bloom patterns using real NASA data.
""")
