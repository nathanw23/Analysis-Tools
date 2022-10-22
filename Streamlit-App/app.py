import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from shared_functions import csv_read_and_break_filter
from fluorimeter.standard_scan_analysis import fluorimeter_scan_analysis
from fluorimeter.kinetics_analysis import fluorimeter_kinetics_analysis
from platereader.kinetics import interpret_plate_kinetics
from nanodrop.nanodrop_analysis import absorbance_setup

# Settings
analysis_tools = ["Nanodrop", "Plate Kinetics", 'Fluorimeter Scan', 'Fluorimeter Kinetics']
page_title = "Analysis Tools"
page_header = 'Laboratory Analysis Tools - Web App'
page_icon = ":bar_chart:"  # https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# Layout
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)
st.header(page_header)

with st.expander('About this app'):
  st.write('This app plots data from a Clariostar plate reader and Cary Eclipse Fluorimeter.')

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
        df = fluorimeter_scan_analysis(data_file)
        fig = plt.figure()
        sns.lineplot(data=df, x="Wavelength (nm)", y="Intensity (A.U.)", hue="Sample")
        st.pyplot(fig)
    if selected_tool == "Fluorimeter Kinetics":
        df = fluorimeter_kinetics_analysis(data_file)
        fig = plt.figure()
        sns.lineplot(data=df, x="Time (min)", y="Intensity (A.U.)", hue="Group")
        st.pyplot(fig)
    if selected_tool == "Plate Kinetics":
        df = interpret_plate_kinetics(data_file, labels)
        fig = plt.figure()
        sns.lineplot(data=df, x='Converted_Time', y='Signal', hue='Group', ci='sd')
        st.pyplot(fig)
    if selected_tool == "Nanodrop":
        df = absorbance_setup(data_file)
        st.line_chart(data=df, x='Wavelength (nm)', y='Absorbance')
