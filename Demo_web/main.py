import streamlit as st

st.set_page_config(page_title="Apparent Temperature Dashboard", layout="wide")

main_page = st.Page("./pages/main_page.py", title="Main Page", icon="🎈")
raw_data_page = st.Page("./pages/data_demo.py", title="Raw data")
EDA_before_preprocessing_page = st.Page("./pages/EDA_before_preprocessing.py", title="EDA before preprocessing")
EDA_after_preprocessing_page = st.Page("./pages/EDA_after_preprocessing.py", title="EDA after preprocessing")
dashboard = st.Page("./pages/dashboard.py", title="Dashboard")

pg = st.navigation([main_page, 
                    raw_data_page,
                    EDA_before_preprocessing_page,
                    EDA_after_preprocessing_page,
                    dashboard])
pg.run()

