#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Fluorimeter_Scan_Analysis.py

Python script to format and plot fluorimeter scan data 

v1, Nathan Wu, 22-Sep-2021
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import click 
import random
from quote import quote

@click.command()
@click.option("--data_file", required=True, help='Specify location of input data file.')

def fluorimeter_scan_analysis(data_file):

    base_folder = os.path.dirname(data_file)
    exp_name = data_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]

    df = pd.read_csv(data_file)
    if df.shape[1] %2 != 0: df = df.iloc[: , :-1]
    df = df.dropna()   
    
    raw_sample_names = df.columns.to_list()    
    sample_names = raw_sample_names[::2]
    old_names = raw_sample_names[1::2]
    
    df2=df.drop([0, 0])
    df2 = pd.melt(df2, id_vars=raw_sample_names[0], value_vars=raw_sample_names[1::2], var_name='Sample', value_name='Intensity (A.U.)')
    df2 = df2.rename(columns={sample_names[0]: "Wavelength (nm)"})
    df2 = df2[["Sample", "Wavelength (nm)", "Intensity (A.U.)"]]
    df2['Sample'] = df2['Sample'].replace(old_names,sample_names)
    df2[["Wavelength (nm)", "Intensity (A.U.)"]] = df2[["Wavelength (nm)", "Intensity (A.U.)"]].apply(pd.to_numeric)
    
    df2.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False)
    
    sns.lineplot(data=df2, x="Wavelength (nm)", y="Intensity (A.U.)", hue="Sample")

    plt.ylim(ymin=0)
    plt.title('%s Fluorescence Scan' % exp_name)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (AU)')

    plt.savefig(os.path.join(base_folder, f'{exp_name} Fluorescence_Scan.png'), dpi=300)
    #plt.show()
    
    words = {"science", "music", "engineering"}
    choice = random.choice(tuple(words))
    res = quote(choice, limit = 100)
    random_number = random.randint(1,100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")
