# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:38:39 2022

@author: Nathan Wu
"""

import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import os
import click 
import random
from quote import quote

@click.command()
@click.option('--data_file', required=True, help='Spectra file from NanoDrop in .TSV format.')

def Plot_NanoDrop(data_file):

    base_folder = os.path.dirname(data_file) # Sets the base file
    exp_name = data_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]

    df = pd.read_csv(data_file, sep="\t", skiprows=2) # Skips the top two rows in imported tsv file
    
    df.to_csv(os.path.join(base_folder, f'{exp_name}.csv'), encoding='utf-8', index=False) # Saves the tsv file as a csv file for future analysis

    ymax = df['Absorbance'].max()

    sns.lineplot(data=df, x="Wavelength (nm)", y="Absorbance", color='red')
    plt.ylim(ymin=0)
    plt.xlim(190, 840)
    plt.title('%s Nano Drop Analysis' % exp_name)
    plt.savefig(os.path.join(base_folder, '%s_NanoDropAnalysis.png' % exp_name))
    #plt.show()
    
    words = {"science", "music", "engineering"}
    choice = random.choice(tuple(words))
    res = quote(choice, limit = 100)
    random_number = random.randint(1,100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")
    
