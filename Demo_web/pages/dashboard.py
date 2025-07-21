import streamlit as st
from utils.load_data import load_all_csv
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import base64
from PIL import Image
import io

PREPROCESSED_DATA_FOLDER_PATH = '../DATA_AT_FilteredDate/'
stations = [
        "Noi Bai", "Lang Son", "Lao Cai",
        "Vinh", "Phu Bai", "Quy Nhon",
        "TPHCM", "Ca Mau"
    ]
data_dict = load_all_csv(PREPROCESSED_DATA_FOLDER_PATH, '_FilteredDate.csv')
available_stations = list(data_dict.keys())
station_order = [s for s in stations if s in available_stations]


# Option
option = st.selectbox("Choose stations", station_order)
df = data_dict[option]
feature = 'AT mean'

# Button
AT_mean_button, AT_max_button = st.columns(2)
if AT_mean_button.button("Mean apparent temperature", use_container_width=True):
    feature = "AT mean"
if AT_max_button.button("Maximum apparent temperature", use_container_width=True):
    feature = "AT max"

def plot_annual_AT_variation(option, station_df, feature):
    years = np.arange(1992, 2025)
    at = station_df.groupby('YEAR')[feature].mean()

    coef_mean = np.polyfit(years, at, 1)
    trend_mean = coef_mean[0]*years + coef_mean[1]

    fig = go.Figure()

    if feature == 'AT mean':
        line_label = "Mean apparent temperature (°C)"
    else:
        line_label = "Max apparent temperature (°C)"

    fig.add_trace(go.Scatter(
        x=years, y=at,
        mode='lines+markers',
        name=line_label,
        line=dict(color="#4C708C")
    ))

    fig.add_trace(go.Scatter(
        x=years, y=trend_mean,
        mode='lines',
        name="Trend (mean)",
        line=dict(color="#D9D9D9", dash="dash")
    ))
        
    fig.update_layout(
        title=f"Annual variation of apparent temperature at {option} station",
        xaxis_title="Year",
        yaxis_title="Apparent Temperature (°C)",
        template="simple_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_AT_variation(option, station_df, feature):
    df = station_df.copy()

    # Xác định giai đoạn
    conditions = [
        (df['YEAR'] >= 1992) & (df['YEAR'] <= 2002),
        (df['YEAR'] >= 2003) & (df['YEAR'] <= 2013),
        (df['YEAR'] >= 2014) & (df['YEAR'] <= 2018),
        (df['YEAR'] >= 2019) & (df['YEAR'] <= 2024),
    ]
    choices = ['1992 - 2002', '2003 - 2013', '2014 - 2018', '2019 - 2024']
    df['period'] = np.select(conditions, choices, default='Other')

    # Tính giá trị trung bình
    mean_at = df.groupby(['period', 'MONTH'])[feature].mean().unstack('MONTH')

    # Tổng hợp toàn bộ giai đoạn
    total_df = df[(df['YEAR'] >= 1992) & (df['YEAR'] <= 2024)]
    mean_total = total_df.groupby('MONTH')[feature].mean()
    mean_at.loc['1992 - 2024'] = mean_total

    # Reorder
    choices.append('1992 - 2024')
    mean_at = mean_at.reindex(choices)
    choices = ['1992 - 2024'] + choices[:-1]
    mean_at = mean_at.reindex(choices)

    # Xây dựng heatmap
    fig = go.Figure(data=go.Heatmap(
        z=mean_at.values,
        x=[i for i in range(1, 13)],
        y=choices,
        colorscale='RdBu_r',
        colorbar=dict(title='°C')
    ))

    # Thêm annotation từng ô
    annotations = []
    for i in range(mean_at.shape[0]):
        for j in range(mean_at.shape[1]):
            annotations.append(
                go.layout.Annotation(
                    text=f"{mean_at.values[i, j]:.1f}",
                    x=mean_at.columns[j],
                    y=mean_at.index[i],
                    showarrow=False,
                    font=dict(color="black", size=12, family="Times New Roman")
                )
            )

    fig.update_layout(
        annotations=annotations,
        xaxis_title="Month",
        yaxis_title="Period",
        font=dict(family="Times New Roman", size=14),
        template="simple_white",
        xaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(1, 13)],  
            ticktext=[str(i) for i in range(1, 13)]
        ),
        yaxis=dict(autorange="reversed"),
        title=f"Monthly variation of apparent temperature at {option} station"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def get_corr(data_dict, feature):
    data = {
        'Noi Bai': list(data_dict['Noi Bai'][feature]),
        'Lang Son': list(data_dict['Lang Son'][feature]),
        'Lao Cai': list(data_dict['Lao Cai'][feature]),
        'Vinh': list(data_dict['Vinh'][feature]),
        'Phu Bai': list(data_dict['Phu Bai'][feature]),
        'Quy Nhon': list(data_dict['Quy Nhon'][feature]),
        'TPHCM': list(data_dict['TPHCM'][feature]),
        'Ca Mau': list(data_dict['Ca Mau'][feature]),
    }
    data = pd.DataFrame(data)
    corr = data.corr(method='pearson')

    return round(corr, 2)

def plot_heatmap(data_dict, feature):
    corr_feature = get_corr(data_dict, feature)
    stations = corr_feature.columns.tolist()

    fig = go.Figure(data=go.Heatmap(
        z=corr_feature,
        x=stations,
        y=stations,
        colorscale='Blues',
    
    ))

    annotations = []
    for i in range(len(stations)):
        for j in range(len(stations)):
            annotations.append(
                go.layout.Annotation(
                    text=str(corr_feature.values[i][j]),
                    x=stations[j],
                    y=stations[i],
                    xref='x1',
                    yref='y1',
                    showarrow=False,
                    font=dict(color="black", size=12, family="Times New Roman")
                )
            )

    fig.update_layout(
        annotations=annotations,
        xaxis_title="Station",
        font=dict(family="Times New Roman", size=14),
        template="simple_white",
        yaxis=dict(autorange="reversed"),
        title=f"Correlation of apparent temperature among stations"
    )

    st.plotly_chart(fig, use_container_width=True)


# Dashboard spatial
col1, col2 = st.columns(2)
with col1:
    st.write('\n')
    st.write('\n')
    st.markdown('**Effect of latitude on apparent temperature among stations**')
    if feature == 'AT mean':
        st.image('static/ATmean_map.png', use_container_width=True)
    elif feature == 'AT max':
        st.image('static/ATmax_map.png', use_container_width=True)
    
with col2:
    plot_heatmap(data_dict, feature)

# Dashboard temporal
col3, col4 = st.columns(2)
with col3:
    plot_annual_AT_variation(option, df, feature)
with col4:
    plot_monthly_AT_variation(option, df, feature)
    

    