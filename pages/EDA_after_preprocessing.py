import streamlit as st
from utils.load_data import load_all_csv
import pandas as pd
import plotly.graph_objects as go

PREPROCESSED_DATA_FOLDER_PATH = 'static/Data_AT_FilteredDate/'
RAW_DATA_FOLDER_PATH = 'static/DATA_SENT_SV/'
stations = [
        "Noi Bai", "Lang Son", "Lao Cai",
        "Vinh", "Phu Bai", "Quy Nhon",
        "TPHCM", "Ca Mau"
    ]
data_dict = load_all_csv(PREPROCESSED_DATA_FOLDER_PATH, '_FilteredDate.csv')
raw_data_dict = load_all_csv(RAW_DATA_FOLDER_PATH, '_Final.csv')
available_stations = list(data_dict.keys())
station_order = [s for s in stations if s in available_stations]

# Description page
st.title('Exploratory Data Analysis – After Preprocessing')
st.write('This section performs the data preprocessing steps before conducting any analysis or modeling:')
st.markdown("""
1. **Remove missing or invalid values:**  
   Ensure data integrity by eliminating records with missing or incorrect entries to avoid bias in subsequent analyses.

2. **Find the common dates across all stations and remove the non-overlapping ones:**  
   Find the overlapping time period shared by all meteorological stations and filter out any records outside of this range. This ensures that the dataset is fully aligned and comparable across stations.

These steps help standardize the dataset, ensuring consistency when comparing or modeling the data from different stations.
""")

date_data = []
missing_values_data = []
columns_check = ['TMP_2', 'DEW_2', 'RH', 'AT mean', 'AT max']
remain_data = dict()
for station_name, station_df in data_dict.items():
    ymd = pd.to_datetime(station_df[['YEAR', 'MONTH', 'DAY']])

    first_day = ymd.min().date()
    last_day = ymd.max().date()
    years = ymd.dt.year.max() - ymd.dt.year.min()
    total_dates = len(station_df)

    date_data.append({
        "Station": station_name,
        "First Day": first_day,
        "Last Day": last_day,
        "Years": years,
        "Total Records": total_dates
    })

    row = {"Station": station_name}
    for col in columns_check:
        if col in station_df.columns:
            row[col] = station_df[col].isnull().sum()
        else:
            row[col] = "N/A"  
    missing_values_data.append(row)

    preprocessed_length = len(station_df)
    raw_length = len(raw_data_dict[station_name])
    remain_data[station_name] = {
        'Raw': raw_length,
        'Preprocessed': preprocessed_length
    }

# Missing values
st.subheader('Remaining missing values after preprocessing')
st.dataframe(pd.DataFrame(missing_values_data))

# Data range after preprocessing
st.subheader('Data range after preprocessing')
st.dataframe(pd.DataFrame(date_data))

# Remaining data
st.subheader('Remaining data after preprocessing')
remain_df = pd.DataFrame(remain_data).T.reset_index()
remain_df.columns = ['Station', 'Raw', 'Preprocessed']
remain_df['Removed'] = remain_df['Raw'] - remain_df['Preprocessed']
remain_df['Preprocessed (%)'] = (remain_df['Preprocessed'] / remain_df['Raw'] * 100).round(1)
remain_df['Removed (%)'] = (remain_df['Removed'] / remain_df['Raw'] * 100).round(1)
fig = go.Figure()

fig.add_trace(go.Bar(
    x=remain_df['Station'],
    y=remain_df['Preprocessed'],
    name='Preprocessed Data',
    marker_color='#4C708C',
    textposition='inside'
))

fig.add_trace(go.Bar(
    x=remain_df['Station'],
    y=remain_df['Removed'],
    name='Removed Data',
    marker_color='#D9D9D9',
    text=[f"{v} ({p}%)" for v, p in zip(remain_df['Removed'], remain_df['Removed (%)'])],
    textposition='inside'
))

fig.update_layout(
    barmode='stack',
    title='Remaining Data After Preprocessing',
    yaxis_title='Number of Records',
    xaxis_title='Station',
    legend=dict(title='Data Type'),
    template='simple_white'
)

st.plotly_chart(fig, use_container_width=True)


# Describe data after preprocessing
st.subheader('Statistical summary of data after preprocessing')
option = st.selectbox("Choose stations", station_order)
df = data_dict[option]
st.dataframe(df.describe())