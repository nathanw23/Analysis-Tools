"""
Fluorimeter_3DScan_Analysis.py

Python script to format and plot fluorimeter scan data 

v1, Nathan Wu, 22-Sep-2021
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
import click
from tqdm import tqdm
import random
from quote import quote

@click.command()
@click.option('--data_file', required=True, help='Data file for analysis. Fluorimeter must be set to EXCITATION scan mode')
@click.option('--c_axis', type=click.IntRange(0, 1000), default=400, show_default=True, help='Set the maximum value of the colourbar')

def interpret_3d_scan(data_file, c_axis):

    base_folder = os.path.dirname(data_file)
    exp_name = data_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]

    f = open(data_file, "r")
    lines = f.readlines()

    unfiltered_lines = [sub.split(",") for sub in lines]

    data_end = 0
    for l_index, line in enumerate(unfiltered_lines):  # logs are separated from data by a single blank line - this will detect and remove all logs after this line
        if line == ['\n']:
            data_end = l_index
            break
            
    filtered_lines = unfiltered_lines[0:data_end]
    df = pd.DataFrame(filtered_lines)
    df.dropna(inplace=True)

    print('Formatted data saved as %s_Formatted_Data.csv' % exp_name)
    df.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False, header=False)

    raw_data = pd.read_csv(os.path.join(base_folder, "%s_Formatted_Data.csv" % exp_name), header=[0, 1])

    # excitation wavelengths are repeated throughout file, so can read in first column only and discard the rest
    excitation_wavelengths = raw_data.iloc[:, 0].to_list()

    raw_emission_wavelengths = raw_data.columns.to_list()  # emission wavelengths are given in strings in the header, so need to be extracted
    raw_emission_wavelengths = [e[0] for e in raw_emission_wavelengths]  # emission wavelengths are in the first header

    emission_wavelengths = []
    for i in range(0, len(raw_emission_wavelengths), 2):  # run through the header data, the emission wavelength is in every second cell
        for seg in raw_emission_wavelengths[i].split('_'):  # split header using underscores
            try:
                em_wavelength = float(seg) # hacky way to extract wavelength by checking if string can be converted into an integer.
            except:
                pass

        if em_wavelength != 0 and raw_emission_wavelengths[i] != '\n':  # discards any 0 wavelengths, these are artifacts produced by Pandas.
            emission_wavelengths.append(em_wavelength)

    emission_positions = defaultdict(list)
    for index, wav in enumerate(emission_wavelengths):  # extracting positions of any duplicates (for averaging down the line)
        emission_positions[wav].append(index)

    replicates = len(list(emission_positions.values())[0])  # extracts number of replicates used from data

    heatmap_data = np.zeros((len(emission_positions), (len(excitation_wavelengths))))  # emission on y-axis, excitation on x-axis

    for i, ex in tqdm(enumerate(excitation_wavelengths), total=len(excitation_wavelengths), desc='Excitation Wavelengths'):  # running through excitation wavelengths
        for j, (em, em_indices) in enumerate(emission_positions.items()):
            fixed_indices = [(ind*2) + 1 for ind in em_indices]  # offsetting index positions to match file (data repeated once every 2 columns)
            replicate_data = raw_data.iloc[i, fixed_indices]
            heatmap_data[j, i] = np.mean(replicate_data)  # averaging data according to number of replicates

    # Graph plotting and formatting
    fig, ax = plt.subplots(figsize=(35,25))
    hmap = sns.heatmap(heatmap_data, xticklabels=['%.2f' % e for e in excitation_wavelengths],  # changes the dp of the excitation wavelength
                       yticklabels=(emission_positions.keys()), vmin=0, vmax=c_axis,cmap='viridis',
                       cbar_kws={'label': 'Intensity', 'orientation': 'vertical'})
    # plt.pcolor(heatmap_data, vmin=0, vmax=1000)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=25)
    cbar.ax.set_ylabel('', rotation=270, fontsize=30)

    hmap.set_xticklabels(['%.3f' % e for e in excitation_wavelengths])  # converting floats to 3DP strings
    hmap.invert_yaxis()
    plt.locator_params(axis='x', nbins=50)
    plt.locator_params(axis='y', nbins=50)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(rotation=0, fontsize=20)

    # ax.set_yticklabels(list(emission_positions.keys()))

    plt.title('%s 3D Fluorescence Scan' % exp_name, fontsize=35)
    plt.xlabel('Excitation Wavelengths (nm)', fontsize=35)
    plt.ylabel('Emission Wavelengths (nm)', fontsize=35)

    plt.savefig(os.path.join(base_folder, '%s_3DScan.png' % exp_name),dpi=300)
    
    words = {"science", "music", "engineering"}
    choice = random.choice(tuple(words))
    res = quote(choice, limit = 100)
    random_number = random.randint(1,100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")