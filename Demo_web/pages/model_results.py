import streamlit as st
from utils.load_data import load_excel, load_csv, load_all_csv
import pandas as pd
import plotly.graph_objects as go

PREPROCESSED_DATA_FOLDER_PATH = '../DATA_AT_FilteredDate/'
data_dict = load_all_csv(PREPROCESSED_DATA_FOLDER_PATH, '_FilteredDate.csv')
data = {
    'AT mean': {
        'LSTM': {
            'R2': [91.287, 90.588, 90.549, 93.74, 89.855, 94.264, 68.725, 56.462],
            'MSE': [2.415, 3.26, 2.597, 1.655, 1.771, 0.415, 0.593, 0.837],
            'RMSE': [1.554, 1.805, 1.612, 1.286, 1.331, 0.644, 0.77, 0.915],
            'MAE': [1.144, 1.317, 1.256, 0.947, 0.963, 0.486, 0.598, 0.696]
        },
        'BiLSTM': {
            'R2': [90.832, 90.14, 90.18, 93.216, 89.103, 92.766, 66.074, 55.085],
            'MSE': [2.541, 3.414, 2.698, 1.794, 1.902, 0.522, 0.643, 0.864],
            'RMSE': [1.594, 1.848, 1.643, 1.339, 1.379, 0.722, 0.802, 0.929],
            'MAE': [1.217, 1.356, 1.282, 0.995, 1.006, 0.559, 0.648, 0.721]
        },
        'GCN - LSTM': {
            'R2': [91.5232, 89.2053, 91.3655, 94.3617, 92.7648, 94.5469, 68.0806, 58.4931],
            'MSE': [2.3493, 3.7385, 2.3728, 1.4908, 1.2629, 0.3932, 0.6054, 0.7980],
            'RMSE': [1.5327, 1.9335, 1.5404, 1.2210, 1.1238, 0.6272, 0.7781, 0.8933],
            'MAE': [1.1526, 1.4053, 1.1827, 0.9065, 0.8417, 0.4772, 0.6119, 0.6862]
        },
        'GCN - BiLSTM': {
            'R2': [91.3447, 89.1781, 90.8855, 93.8819, 92.4564, 94.1561, 68.1283, 58.3186],
            'MSE': [2.3988, 3.7479, 2.5047, 1.6176, 1.3167, 0.4216, 0.6045, 0.8014],
            'RMSE': [1.5488, 1.9360, 1.5826, 1.2719, 1.1475, 0.6493, 0.7775, 0.8952],
            'MAE': [1.1543, 1.4023, 1.1869, 0.9315, 0.8561, 0.4961, 0.6088, 0.6840]
        },
        'The proposed model with LSTM': {
            'R2': [98.4013, 97.8732, 98.6501, 99.0797, 98.8128, 99.1371, 94.2309, 93.0102],
            'MSE': [0.4431, 0.7366, 0.3710, 0.2433, 0.2072, 0.0623, 0.1094, 0.1344],
            'RMSE': [0.6656, 0.8582, 0.6091, 0.4933, 0.4552, 0.2495, 0.3308, 0.3666],
            'MAE': [0.3715, 0.4356, 0.3431, 0.3027, 0.2702, 0.1540, 0.1734, 0.1940]
        },
        'The proposed model with BiLSTM': {
            'R2': [98.4616, 97.9224, 98.5506, 99.0471, 98.6891, 99.1049, 94.2284, 92.7179],
            'MSE': [0.4264, 0.7195, 0.3983, 0.2520, 0.2288, 0.0646, 0.1095, 0.1400],
            'RMSE': [0.6530, 0.8482, 0.6311, 0.5020, 0.4783, 0.2541, 0.3309, 0.3742],
            'MAE': [0.3789, 0.4456, 0.3607, 0.3184, 0.2846, 0.1568, 0.1852, 0.1996]
        }
    },
    'AT max':{
        'LSTM': {
            'R2': [84.758, 81.806, 81.725, 84.865, 78.98, 67.307, 51.482, 45.517],
            'MSE': [5.493, 7.785, 6.534, 5.403, 6.172, 3.804, 1.559, 1.71],
            'RMSE': [2.344, 2.79, 2.556, 2.325, 2.484, 1.95, 1.249, 1.308],
            'MAE': [1.867, 2.179, 2.038, 1.815, 1.864, 1.681, 0.986, 0.973]
        },
        'BiLSTM': {
            'R2': [84.265, 81.477, 81.025, 84.107, 78.652, 61.894, 50.516, 43.297],
            'MSE': [5.671, 7.926, 6.785, 5.674, 6.268, 4.434, 1.59, 1.78],
            'RMSE': [2.344, 2.79, 2.556, 2.325, 2.484, 1.95, 1.249, 1.308],
            'MAE': [1.896, 2.19, 2.069, 1.859, 1.872, 1.821, 1.021, 0.981]
        },
        'GCN - LSTM': {
            'R2': [84.4389, 80.9042, 83.6896, 87.3539, 85.9621, 86.9442, 50.7896, 44.5720],
            'MSE': [5.6086, 8.1707, 5.8320, 4.5148, 4.1219, 1.5192, 1.5817, 1.7397],
            'RMSE': [2.3683, 2.8584, 2.4150, 2.1248, 2.0302, 1.2325, 1.2576, 1.3190],
            'MAE': [1.8495, 2.1385, 1.8905, 1.5686, 1.5334, 0.9331, 1.0039, 1.0118]
        },
        'GCN - BiLSTM': {
            'R2': [84.439, 80.6087, 83.7770, 87.3646, 86.1197, 86.7334, 50.4370, 44.5633],
            'MSE': [5.6086, 8.2971, 5.8008, 4.5110, 4.0756, 1.5437, 1.5930, 1.7400],
            'RMSE': [2.3683, 2.8805, 2.4085, 2.1239, 2.0188, 1.2425, 1.2621, 1.3191],
            'MAE': [1.8495, 2.1506, 1.8796, 1.5748, 1.5241, 0.9470, 1.0107, 0.9993]
        },
        'The proposed model with LSTM': {
            'R2': [97.1083, 96.6071, 97.5423, 98.1874, 98.1451, 98.2442, 90.2718, 90.4516],
            'MSE': [1.0422, 1.4517, 0.8788, 0.6471, 0.5446, 0.2043, 0.3127, 0.2997],
            'RMSE': [1.0209, 1.2049, 0.9374, 0.8044, 0.7380, 0.4520, 0.5592, 0.5474],
            'MAE': [0.5419, 0.6127, 0.5084, 0.4680, 0.4265, 0.2582, 0.2750, 0.2550]
        },
        'The proposed model with BiLSTM': {
            'R2': [97.1634, 96.7582, 97.5141, 98.2382, 98.1803, 97.8917, 90.2103, 90.2259],
            'MSE': [1.0224, 1.3871, 0.8889, 0.6290, 0.5343, 0.2453, 0.3147, 0.3068],
            'RMSE': [1.0111, 1.1778, 0.9428, 0.7931, 0.7310, 0.4953, 0.5609, 0.5539],
            'MAE': [0.5437, 0.5994, 0.5104, 0.4737, 0.4235, 0.3025, 0.2745, 0.2732]
        }
    }
}
color_dict = {
    'LSTM': '#dbae58',
    'BiLSTM': '#2ca02c',
    'GCN - LSTM': '#d62728',
    'GCN - BiLSTM': '#9467bd',
    'The proposed model with LSTM': '#ff7f0e',
    'The proposed model with BiLSTM': '#1f77b4'
}
marker_dict = {
    'LSTM': 'circle',
    'BiLSTM': 'triangle-up',
    'GCN - LSTM': 'pentagon',
    'GCN - BiLSTM': 'star',
    'The proposed model with LSTM': 'square',
    'The proposed model with BiLSTM': 'diamond'
}

compare_data = {
    'AT mean': {
        'LSTM': load_excel('../Result_csv/LSTM/Result_LSTM_ATmean.xlxs'),
        'BiLSTM': load_excel('../Result_csv/BiLSTM/Result_BiLSTM_ATmean.xlsx'),
        'GCN - LSTM': load_csv('../Result_csv/GCN_LSTM_baseline/Result_GCN_LSTM_baseline_1_ATmean_new.csv'),
        'GCN - BiLSTM': load_csv('../Result_csv/GCN_BiLSTM_baseline/Result_GCN_BiLSTM_baseline_1_ATmean_new.csv'),
        'The proposed model with LSTM': load_csv('../Result_csv/GCN_LSTM_Attention/Result_GCN_LSTM_Attention_1_ATmean_new.csv'),
        'The proposed model with BiLSTM': load_csv('../Result_csv/GCN_BiLSTM_Attention/Result_GCN_BiLSTM_Attention_1_ATmean_new.csv'),
    },
    'AT max': {
        'LSTM': load_excel('../Result_csv/LSTM/Result_LSTM_ATmax.xlxs'),
        'BiLSTM': load_excel('../Result_csv/BiLSTM/Result_BiLSTM_ATmax.xlsx'),
        'GCN - LSTM': load_csv('../Result_csv/GCN_LSTM_baseline/Result_GCN_LSTM_baseline_1_ATmax_new.csv'),
        'GCN - BiLSTM': load_csv('../Result_csv/GCN_BiLSTM_baseline/Result_GCN_BiLSTM_baseline_1_ATmax_new.csv'),
        'The proposed model with LSTM': load_csv('../Result_csv/GCN_LSTM_Attention/Result_GCN_LSTM_Attention_1_ATmax_new.csv'),
        'The proposed model with BiLSTM': load_csv('../Result_csv/GCN_BiLSTM_Attention/Result_GCN_BiLSTM_Attention_1_ATmax_new.csv'),
    }
}

stations = ['Noi Bai', 'Lang Son', 'Lao Cai',
            'Vinh', 'Phu Bai', 'Quy Nhon',
            'TPHCM', 'Ca Mau']


if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'LSTM'

if 'selected_station' not in st.session_state:
    st.session_state.selected_station = 'Noi Bai'

if 'feature' not in st.session_state:
    st.session_state.feature = 'AT mean'

# Description page
st.title("Model performance results")
st.write("This section performs the performance comparision between the proposed model and several baseline models," \
"including LSTM, BiLSTM, GCN - LSTM and GCN - BiLSTM proposed by other authors. " \
"The comparison is conducted using multiple evaluation metrics such as R² score, MAE, MSE, and RMSE, providing a comprehensive analysis of the forecasting capabilities of each model.")
st.write("**Note:** The architectures of the models are described in the [README](https://github.com/NgocHuynhTuyet0308/Apparent_temperature_forecasting_Vietnam) on GitHub.")


# Button
st.subheader("Evaluate model performance across metrics")
button_left, button_right = st.columns(2)
if button_left.button("Mean apparent temperature", use_container_width=True):
    st.session_state.feature = "AT mean"
if button_right.button("Max apparent temperature", use_container_width=True):
    st.session_state.feature = 'AT max'

def lineplot_result(data, feature, metric, color_dict, marker_dict):
    data_dict = data[feature]
    stations = ['Noi Bai', 'Lang Son', 'Lao Cai',
                'Vinh', 'Phu Bai', 'Quy Nhon',
                'TPHCM', 'Ca Mau']
    models = [model for model in data_dict.keys()]
    model_results = dict()
    
    for model in models:
        model_results[model] = data_dict[model][metric]
    
    fig = go.Figure()

    for model in models:
        fig.add_trace(go.Scatter(
            x=stations,
            y=model_results[model],
            mode='lines+markers',
            name=model if 'R2' in metric else None,
            showlegend=True if 'R2' in metric else False,
            line=dict(
                color=color_dict.get(model, 'gray'),
                width=2,
                dash='dot'),
            marker=dict(
                color=color_dict.get(model, 'gray'),
                size=8,
                symbol=marker_dict.get(model, 'circle') 
            )
        ))
    new_feature = feature.replace('AT', 'apparent temperature')
    fig.update_layout(
        title = f'{metric}',
        xaxis_title='Station',
        yaxis_title=f'{metric}',
        xaxis_tickangle=45
    )

    st.plotly_chart(fig, use_container_width=True)



    
# R2 plot
lineplot_result(data, st.session_state.feature, 'R2', color_dict, marker_dict)

# MAE, MSE, RMSE plot
col1, col2, col3 = st.columns(3)
with col1:
    lineplot_result(data, st.session_state.feature, 'MSE', color_dict, marker_dict)
with col2:
    lineplot_result(data, st.session_state.feature, 'RMSE', color_dict, marker_dict)
with col3:
    lineplot_result(data, st.session_state.feature, 'MAE', color_dict, marker_dict)




st.write("\n")
st.subheader('Comparion of model predictions and actual values')
# Option
col4, col5 = st.columns(2)
with col4:
    st.session_state.selected_model = st.selectbox(
        "Choose model:",
        ['LSTM', 'BiLSTM', 
         'GCN - LSTM', 'GCN - BiLSTM',
         'The proposed model with LSTM',
         'The proposed model with BiLSTM']
    )
with col5:
    st.session_state.selected_station = st.selectbox(
        "Choose station:",
        ['Noi Bai', 'Lang Son', 'Lao Cai', 'Vinh', 'Phu Bai', 'Quy Nhon', 'TPHCM', 'Ca Mau']
    )


def lineplot_compare_data(compare_data, feature, forecast_horizon, selected_model, selected_station):
    df_NoiBai = data_dict['Noi Bai']
    df_last_1177 = df_NoiBai.tail(1177)
    date_array = df_last_1177.apply(
        lambda row: f"{int(row['DAY']):02d}/{int(row['MONTH']):02d}/{int(row['YEAR'])}",
        axis=1
    ).tolist()
    
    forecast_start_index = 31 + forecast_horizon - 1
    date_forecast_array = date_array[forecast_start_index:]

    df_results = compare_data[feature][selected_model]
    station = selected_station.replace(' ', '')
    real_col = f'Real_AT_{station}'
    predicted_col = f'Predicted_AT_{station}'

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=date_forecast_array,
            y=df_results[real_col],
            mode='lines',
            name='Actual values',
            line=dict(color='#1f77b4')
        ))
    
    fig.add_trace(go.Scatter(
            x=date_forecast_array,
            y=df_results[predicted_col],
            mode='lines',
            name='Predicted values',
            line=dict(color='#ff7f0e')
        ))
    
    step = max(1, len(date_forecast_array) // 10)
    tickvals = [date_forecast_array[i] for i in range(0, len(date_forecast_array), step)]
    fig.update_xaxes(
        tickvals=tickvals,    
        ticktext=tickvals,   
        tickangle=45,         
        tickfont=dict(
            family="Times New Roman",
            size=12
        )
    )
    feature = feature.replace('AT', 'Apparent temperature')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=feature,
    )

    st.plotly_chart(fig, use_container_width=True)


lineplot_compare_data(compare_data, st.session_state.feature, 1, st.session_state.selected_model, st.session_state.selected_station)