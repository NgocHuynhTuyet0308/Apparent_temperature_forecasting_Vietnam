import streamlit as st

st.set_page_config(page_title="Apparent Temperature Dashboard", layout="wide")

raw_data_page = st.Page("./pages/data_demo.py", title='About this project')
EDA_before_preprocessing_page = st.Page("./pages/EDA_before_preprocessing.py", title="EDA before preprocessing")
EDA_after_preprocessing_page = st.Page("./pages/EDA_after_preprocessing.py", title="EDA after preprocessing")
dashboard = st.Page("./pages/dashboard.py", title="Dashboard")
model_results = st.Page("./pages/model_results.py", title="Model performance")

pg = st.navigation([raw_data_page,
                    EDA_before_preprocessing_page,
                    EDA_after_preprocessing_page,
                    dashboard,
                    model_results])
pg.run()

