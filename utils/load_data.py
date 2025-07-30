import streamlit as st
import os
import glob
import pandas as pd



@st.cache_data
def load_all_csv(folder_path, replace_text):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    dfs = dict()
    for file in csv_files:
        name = os.path.basename(file).replace(replace_text, "")
        dfs[name] = pd.read_csv(file)

    return dfs

@st.cache_data
def load_excel(excel_file_path):
    df = pd.read_excel(excel_file_path)
    return df

@st.cache_data
def load_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df


