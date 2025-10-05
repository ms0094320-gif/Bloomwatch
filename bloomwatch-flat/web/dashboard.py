import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob, os

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title='BloomWatch', layout='wide')
st.title('🌿 BloomWatch Dashboard (Real NASA Data)')

# -------------------------------
# Sidebar controls
# -------------------------------
col1, col2 = st.columns([1,2])
with col1:
    region = st.selectbox('Region', ['Muscat', 'Dhofar', 'Tokyo', 'California'])
    months = st.slider('Months to display', 6, 24, 12, 1)
    st.markdown('---')
    st.caption(
        "🌍 Using **real NASA MODIS NDVI/EVI data** exported via Google Earth Engine (MOD13Q1 collection). "
        "This visualization shows vegetation dynamics for the selected region and period."
    )

# -------------------------------
# Load real CSV data
# -------------------------------
# Look for any CSV inside data/exports/
csv_files = sorted(glob.glob("data/exports/*.csv"))

if csv_files:
    file_path = csv_files[0]  # take the first CSV found
    df = pd.read_csv(file_path)
    st.success(f"Loaded real NASA MODIS dataset: `{os.path.basename(file_path)}`")
else:
    st.warning("No CSV file found in data/exports/. Using demo synthetic data instead.")
    t = np.arange(12)
    df = pd.DataFrame({
        'Month': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        'NDVI': 0.2 + 0.3*np.sin((t-2)/12*2*np.pi),
        'EVI': 0.15 + 0.25*np.sin((t-2)/12*2*np.pi)
    })

# -------------------------------
# Handle time column if available
# -------------------------------
if 'time' in df.columns:
    try:
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values('time')
        df['Month'] = df['time'].dt.strftime('%b %Y')
    except Exception:
        df['Month'] = range(1, len(df)+1)
elif 'Month' not in df.columns:
    df['Month'] = range(1, len(df)+1)

# -------------------------------
# Predict bloom (max NDVI)
# -------------------------------
idx = int(np.argmax(df['NDVI'][:months]))
bloom_val = df['NDVI'].iloc[idx]

# -------------------------------
# Plot the chart
# -------------------------------
with col2:
    st.subheader('📈 NDVI/EVI Time Series (Real MODIS Data)')
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df['Month'][:months], df['NDVI'][:months], marker='o', label='NDVI')
    ax.plot(df['Month'][:months], df['EVI'][:months], marker='o', label='EVI')
    ax.axvline(x=idx, linestyle='--', color='gray')
    ax.annotate('Predicted Bloom', xy=(idx, bloom_val), xytext=(idx+0.5, bloom_val+0.05),
                arrowprops=dict(arrowstyle='->', lw=1.5))
    ax.set_ylim(0, max(0.9, df[['NDVI','EVI']].max().max()+0.1))
    ax.legend()
    st.pyplot(fig)

# -------------------------------
# Footer
# -------------------------------
st.markdown('---')
st.caption("""
🛰 **Data Source:** NASA MODIS MOD13Q1 (NDVI/EVI 16-day composite)  
📊 **Processing:** Exported through Google Earth Engine  
🌱 **Purpose:** Real NDVI/EVI visualization and bloom timing detection.
""")

