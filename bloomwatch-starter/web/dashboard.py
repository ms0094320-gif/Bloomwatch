import streamlit as st, numpy as np, pandas as pd, matplotlib.pyplot as plt

st.set_page_config(page_title='BloomWatch', layout='wide')

st.title('BloomWatch Dashboard (Demo)')

# Controls
col1, col2 = st.columns([1,2])
with col1:
    region = st.selectbox('Region', ['Muscat', 'Dhofar', 'Tokyo', 'California'])
    months = st.slider('Months to display', 6, 12, 12, 1)
    st.markdown('---')
    st.caption('This demo uses synthetic NDVI/EVI. Replace with exports in data/exports/.')

# Synthetic NDVI/EVI seasonal curve
t = np.arange(12)
ndvi = 0.2 + 0.3*np.sin((t-2)/12*2*np.pi)
evi  = 0.15 + 0.25*np.sin((t-2)/12*2*np.pi)
df = pd.DataFrame({'Month': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                   'NDVI': ndvi, 'EVI': evi})

with col2:
    st.subheader('NDVI/EVI time series')
    fig, ax = plt.subplots(figsize=(7,3))
    ax.plot(df['Month'][:months], df['NDVI'][:months], marker='o', label='NDVI')
    ax.plot(df['Month'][:months], df['EVI'][:months], marker='o', label='EVI')
    # naive "bloom" at the max NDVI
    idx = int(np.argmax(df['NDVI'][:months]))
    ax.axvline(x=idx, linestyle='--')
    ax.annotate('Predicted bloom', xy=(idx, df['NDVI'][idx]), xytext=(idx+0.3, df['NDVI'][idx]+0.05),
                arrowprops=dict(arrowstyle='->'))
    ax.set_ylim(0, 0.8)
    ax.legend()
    st.pyplot(fig)

st.markdown('---')
st.caption('Next steps: swap synthetic series for real MODIS/VIIRS exports and model predictions.')