import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------
st.set_page_config(page_title="BloomWatch", layout="wide")
st.title("🌿 BloomWatch — Compare Real NASA MODIS Data (12-Month View)")

st.markdown("""
Use the selector below to explore vegetation health trends from NASA's **MODIS MOD13Q1** dataset.  
Choose between **Muscat, Oman** and **Arizona, USA** to visualize real NDVI/EVI satellite data.
""")

# -------------------------------------------------------
# INTERFACE — SELECT REGION
# -------------------------------------------------------
st.sidebar.header("🌍 Choose Region")
region = st.sidebar.radio(
    "Select region to visualize:",
    ["Muscat, Oman", "Arizona, USA"],
    captions=["Middle East region", "North America region"]
)

# -------------------------------------------------------
# DEFINE FILE PATHS
# -------------------------------------------------------
region_paths = {
    "Muscat, Oman": "data/muscat/bloomwatch_muscat.csv",
    "Arizona, USA": "data/arizona/bloomwatch_arizona.csv"
}

file_path = os.path.join(os.path.dirname(__file__), region_paths[region])

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
if not os.path.exists(file_path):
    st.error(f"🚨 Missing data file for {region}. Expected at: {file_path}")
    st.stop()

df = pd.read_csv(file_path)

# Handle timestamps correctly
if "time" not in df.columns:
    st.error("CSV must include a 'time' column exported from Google Earth Engine.")
    st.stop()

if df["time"].dtype in ["int64", "float64"]:
    df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
else:
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

# Clean data
df = df.sort_values("time").dropna(subset=["NDVI", "EVI"]).reset_index(drop=True)
df["Month"] = df["time"].dt.strftime("%b %Y")

# -------------------------------------------------------
# FILTER TO LAST 12 MONTHS
# -------------------------------------------------------
latest_date = df["time"].max()
start_date = latest_date - pd.DateOffset(months=12)
df_12 = df[df["time"] >= start_date]

if df_12.empty:
    st.warning("⚠️ No valid data found in the past 12 months.")
    st.stop()

# -------------------------------------------------------
# BLOOM ANALYSIS
# -------------------------------------------------------
idx = int(np.argmax(df_12["NDVI"]))
bloom_date = df_12["Month"].iloc[idx]
bloom_value = df_12["NDVI"].iloc[idx]

# -------------------------------------------------------
# VISUALIZATION
# -------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"📈 NDVI / EVI — {region} (Last 12 Months)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_12["Month"], df_12["NDVI"], marker="o", label="NDVI")
    ax.plot(df_12["Month"], df_12["EVI"], marker="o", label="EVI")
    ax.axvline(x=bloom_date, linestyle="--", color="gray")
    ax.annotate(f"Predicted Bloom\n({bloom_date})",
                xy=(idx, bloom_value),
                xytext=(idx + 0.5, bloom_value + 0.02),
                arrowprops=dict(arrowstyle="->", lw=1.2),
                fontsize=9)
    ax.set_ylim(0, max(0.9, float(df_12[["NDVI", "EVI"]].max().max()) + 0.1))
    ax.set_xlabel("Time (Last 12 Months)")
    ax.set_ylabel("Vegetation Index Value")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.metric("Predicted Bloom Month", bloom_date)
    st.metric("Max NDVI Value", f"{bloom_value:.3f}")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.markdown("---")
st.caption(f"""
🛰 **Data Source:** NASA MODIS MOD13Q1 (NDVI/EVI, 16-day composite, 250m resolution)  
📍 **Region:** {region}  
📅 **Time Range:** Last 12 months (Oct 2024 – Oct 2025)  
⚙️ **Processed via:** Google Earth Engine  
🌱 **Purpose:** Detect and visualize vegetation bloom cycles from real NASA data.
""")
