import streamlit as st
from utils.load_data import load_all_csv
import pandas as pd
import pydeck as pdk


RAW_DATA_FOLDER_PATH = '../DATA_SENT SV/'
stations = [
        "Noi Bai", "Lang Son", "Lao Cai",
        "Vinh", "Phu Bai", "Quy Nhon",
        "TPHCM", "Ca Mau"
    ]


data_dict = load_all_csv(RAW_DATA_FOLDER_PATH)
available_stations = list(data_dict.keys())
station_order = [s for s in stations if s in available_stations]

# Description of raw data page
st.title('Raw Data of Apparent Temperature Across Stations')

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

# Raw dataframe
st.subheader('Meteorological Raw Data')
option = st.selectbox("Choose stations", station_order)
df = data_dict[option]
st.dataframe(df)