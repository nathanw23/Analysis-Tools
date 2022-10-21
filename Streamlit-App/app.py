import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Test Data
data = np.random.randn(10,1) # Used to generate data for graph placeholder

# Settings
analysis_tools = ["Plate Multiplex", "Plate Kinetics", 'Fluorimeter Scan', 'Fluorimeter Kinetics', '3D Scan' ]
page_title = "Analysis Tools Web App"
page_icon = ":bar_chart:"  # https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# Navigation Menu
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)

data_file = st.file_uploader("Select data file", key="data_file")

selected_tool = st.selectbox("Select an analysis tool", options=analysis_tools)

if selected_tool in ['Plate Kinetics', 'Plate Multiplex']:
    labels = st.text_input("Labels", placeholder="Enter Labels", key="labels", help="Separated by commas with no spaces") # Needed for plate kinetics and plate multiplex

if 'Plate Multiplex' in selected_tool:
    fluorophores = st.text_input("Fluorophores", placeholder="Enter Fluorophores", key="fluorophores", help="Separated by commas with no spaces") # Needed for plate multiplex

if '3D Scan' in selected_tool:
    c_axis = st.slider("Select C axis range", min_value=100, max_value=1000, step=100) # Only needed for 3D scan


run = st.button("Run Analysis")

if run:
    if selected_tool == "Fluorimeter Scan":
        st.line_chart(data) # Graph place holder