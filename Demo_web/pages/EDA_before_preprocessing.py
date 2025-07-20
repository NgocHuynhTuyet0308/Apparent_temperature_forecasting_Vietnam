import streamlit as st
from utils.load_data import load_all_csv
import io
import pandas as pd

RAW_DATA_FOLDER_PATH = '../DATA_SENT SV/'
stations = [
        "Noi Bai", "Lang Son", "Lao Cai",
        "Vinh", "Phu Bai", "Quy Nhon",
        "TPHCM", "Ca Mau"
    ]
data_dict = load_all_csv(RAW_DATA_FOLDER_PATH, '_Final.csv')
available_stations = list(data_dict.keys())
station_order = [s for s in stations if s in available_stations]

# Description page
st.title('Exploratory Data Analysis – Before Preprocessing')
st.write('This section performs an Exploratory Data Analysis (EDA) ' \
'on the raw meteorological dataset before applying any preprocessing or cleaning steps. ' \
'The main purpose is to understand the initial structure of the data, identify potential quality issues, '
'and summarize key statistics.')

# Data range (date)
st.subheader('Date Range Overview of Each Station')
st.write('Most of the stations started recording data from January 1, ' \
'1990 or April 1, 1992, and nearly all of them ended on August 31, 2024. The data collection periods range from 32 to 34 years, ' \
'depending on the specific meteorological station. As a result, the number of recorded days varies between stations, ' \
'leading to inconsistencies in data length, ' \
'which can affect analysis, comparisons, or serve as input for modeling.')

date_data = []
duplicate_rows_data = []
missing_values_data = []
columns_check = ['TMP_2', 'DEW_2', 'RH', 'AT mean', 'AT max']

for station_name, station_df in data_dict.items():
    # Get date info
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

    # Check duplicate rows
    duplicate_rows_data.append({
        "Station": station_name,
        "Duplicate Rows": station_df.duplicated().sum()
    })

    # Check missing values
    row = {"Station": station_name}
    for col in columns_check:
        if col in station_df.columns:
            row[col] = station_df[col].isnull().sum()
        else:
            row[col] = "N/A"  # Cột không tồn tại
    missing_values_data.append(row)

        
date_df = pd.DataFrame(date_data)
st.dataframe(date_df)

# Check duplicate rows
st.subheader('Check duplicate rows')
st.write('The results show that there are no duplicate records present in the datasets.')
duplicate_rows_df = pd.DataFrame(duplicate_rows_data)
st.dataframe(duplicate_rows_df)

# Check missing values
st.subheader('Check missing values')
st.write('The results show that only the Vinh meteorological station has a single missing value across all features. ' \
'Since the amount of missing data is negligible, ' \
'we have completely removed this record during the preprocessing stage to ' \
'ensure the integrity and quality of the input data.')
df_missing = pd.DataFrame(missing_values_data)
st.dataframe(df_missing)

st.write("\n")

# Describe data
st.subheader('Statistical Summary of Raw Data')
option = st.selectbox("Choose stations", station_order)
df = data_dict[option]
st.dataframe(df.describe())






