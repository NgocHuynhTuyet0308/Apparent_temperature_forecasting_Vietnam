import streamlit as st
import os
import glob
import pandas as pd



@st.cache_data
def load_all_csv(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    dfs = dict()
    for file in csv_files:
        name = os.path.basename(file).replace("_Final.csv", "")
        dfs[name] = pd.read_csv(file)

    return dfs


