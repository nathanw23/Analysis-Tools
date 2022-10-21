import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Settings
analysis_tools = ["Plate Multiplex"]
page_title = "Analysis Tools Web App"
page_icon = ":microscope:"  # https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# Navigation Menu
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)

# Upload data file and select analysis tool
st.header("Select Data File & Select Tool")
with st.form("data_form", clear_on_submit=True):
    data_file = st.file_uploader("Select Data File", key="data_file")
    st.selectbox("Select the analysis tool", analysis_tools, key="tool")
    submitted = st.form_submit_button("Run Analysis")

# Data Clean Up and Visualisation
if submitted:
    df = pd.read_csv(data_file)
    # st.dataframe(df)
    if st.session_state['tool'] == 'Plate Multiplex':
        fig = plt.figure(figsize=(10, 4))
        sns.lineplot(data=df, x="Converted_Time", y="Signal", hue="Group", style="Fluorophore", ci='sd')
        st.pyplot(fig)