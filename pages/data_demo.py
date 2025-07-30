import streamlit as st
from utils.load_data import load_all_csv
import pandas as pd
import pydeck as pdk


RAW_DATA_FOLDER_PATH = 'static\DATA_SENT_SV'
stations = [
        "Noi Bai", "Lang Son", "Lao Cai",
        "Vinh", "Phu Bai", "Quy Nhon",
        "TPHCM", "Ca Mau"
    ]


data_dict = load_all_csv(RAW_DATA_FOLDER_PATH, '_Final.csv')
available_stations = list(data_dict.keys())
station_order = [s for s in stations if s in available_stations]

# Description of raw data page
st.title('Project: Apparent temperature forecasting in Vietnam across 8 stations')
st.write('**Source code is available on [GitHub](https://github.com/NgocHuynhTuyet0308/Apparent_temperature_forecasting_Vietnam).**')

st.subheader('Introduction')
st.write('In recent years, Vietnam has been experiencing an alarming increase in heatwaves and severe cold spells that persist for several consecutive days. These extreme events are matters of concern as they affect human health through apparent temperature – an indication that reflects the degree to which the human body actually feels hot or cold, under the combined influence of factors such as air temperature, dew point and wind speed. This project focuses on improving accuracy in apparent temperature forecasting in Vietnam by exploiting spatio – temporal relationships in meteorological dataset. Specifically, we propose a hybrid model which combines customized Graph Convolutional Network (GCN) with variants of Long short – term memory (LSTM), along with the Attention mechanism. This proposed method includes two phases: data preprocessing as input to the model and model development. In the data preprocessing phase, the datasets are normalized, transformed into a time series format using the sliding window technique. The model development phase primarily focuses on the model architecture and its training process, along with the optimization of its hyperparameters. This study trains and evaluates the proposed model based on apparent temperature dataset which was collected from 8 meteorological stations representing different regions across Vietnam between 1992 and 2024. The efficiency of the proposed model is compared with traditional methods, such as LSTM variants that focus on temporal features, as well as simple models that capture spatio-temporal relationships. Experimental results demonstrate that the proposed method significantly outperforms baseline models in forecasting apparent temperature across all stations in the three main regions of Vietnam, achieving a coefficient of determination (R²) of approximately 93 – 99% for forecasting the mean apparent temperature and 90 – 98% for forecasting the maximum apparent temperature at a single time step.')

st.subheader('Dataset of this project')
st.write('The dataset used in this study was collected from the Meteostat Developers API '
'(https://dev.meteostat.net/), which compiles datasets from worldwide meteorological stations, ' \
'mostly derived from trustworthy governmental agencies like the National Oceanic and Atmospheric Administration (NOAA), ' \
'with the following geographical distribution:')

st.markdown("""
| Region           | Stations |
|-----------------|----------|
| **Northern Vietnam** | Noi Bai (Red River Delta), Lang Son (Northeastern), Lao Cai (Northwestern) |
| **Central Vietnam**  | Vinh, Phu Bai (North Central Coast), Quy Nhon (South Central Coast) |
| **Southern Vietnam** | Ho Chi Minh City (Southeast), Ca Mau (Mekong Delta) |
""")

# Vietnam map
Vietnam_map = pd.DataFrame({
    'lat': [21.2142, 21.8457, 22.4853, 18.6756, 16.4015, 13.782, 10.7626, 9.1769],
    'lon': [105.8048, 106.7615, 103.9639, 105.6932, 107.7038, 109.219, 106.6829, 104.9046],
    'Station': ["Noi Bai", "Lang Son", "Lao Cai", "Vinh", "Phu Bai", "Quy Nhon", "TPHCM", "Ca Mau"],
    'Location': [
        "Red River Delta", "Northeastern", "Northwestern",
        "North Central Coast", "North Central Coast", "South Central Coast",
        "Southeast", "Mekong Delta"
    ]
})
layer = pdk.Layer(
    "ScatterplotLayer",
    Vietnam_map,
    get_position='[lon, lat]',  
    get_radius=50000,           
    get_fill_color='[255, 0, 0, 160]',  
    pickable=True  
)
view_state = pdk.ViewState(
    latitude=16,    
    longitude=107,  
    zoom=4.5    
)
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Station: {Station} ({Location})"}
))


# Feature description
st.subheader('Feature Description')
st.markdown("""
- **YEAR, MONTH, DAY**: Time indicators for each observation  
- **LATITUDE**: North–South geographic position (degrees)  
- **LONGITUDE**: East–West geographic position (degrees)
- **TMP_2**: Air temperature at 2 meters height (°C)  
- **DEW_2**: Dew point temperature at 2 meters height (°C)  
- **RH**: Relative humidity (%)  
- **AT_mean**: Daily mean apparent temperature (°C)  
- **AT_max**: Daily maximum apparent temperature (°C)
""")



# Raw dataframe
st.subheader('Meteorological Raw Data')
option = st.selectbox("Choose stations", station_order, index=0)
df = data_dict[option]
st.dataframe(df)