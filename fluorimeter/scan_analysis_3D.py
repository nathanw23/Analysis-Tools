import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
from tqdm.rich import tqdm
import sys
from shared_functions import generate_quote, csv_read_and_break_filter


def cli_plot_heatmap(heatmap_data, excitation_wavelengths, emission_wavelengths, c_axis, base_folder, exp_name,
                     sample_info=''):
    # Graph plotting and formatting

    fig, ax = plt.subplots(figsize=(35, 25))
    hmap = sns.heatmap(heatmap_data, xticklabels=['%.2f' % e for e in excitation_wavelengths],
                       # changes the dp of the excitation wavelength
                       yticklabels=emission_wavelengths, vmin=0, vmax=c_axis, cmap='viridis',
                       cbar_kws={'label': 'Intensity', 'orientation': 'vertical'})

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=25)
    cbar.ax.set_ylabel('', rotation=270, fontsize=30)

    hmap.set_xticklabels(['%.3f' % e for e in excitation_wavelengths])  # converting floats to 3DP strings
    hmap.set_yticklabels(['%.3f' % e for e in emission_wavelengths])  # converting floats to 3DP strings

    hmap.invert_yaxis()
    plt.locator_params(axis='x', nbins=50)
    plt.locator_params(axis='y', nbins=50)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(rotation=0, fontsize=20)

    plt.title('%s %s 3D Fluorescence Scan' % (exp_name, sample_info), fontsize=35)
    plt.xlabel('Excitation Wavelengths (nm)', fontsize=35)
    plt.ylabel('Emission Wavelengths (nm)', fontsize=35)

    if sample_info != '':
        sample_info = '_' + sample_info

    plt.savefig(os.path.join(base_folder, '%s_3DScan%s.png' % (exp_name, sample_info)), dpi=300)


def interpret_3d_scan(data_file, plot_separately, preformatted_data=False, save_formatted_data=False, **kwargs):
    print("Starting Programme")

    base_folder = os.path.dirname(data_file)
    exp_name = data_file.split(os.sep)[-1].rsplit('.', 1)[0]

    if not preformatted_data:
        print("Importing & Formatting Data")
        filtered_lines = csv_read_and_break_filter(data_file)
        df = pd.DataFrame(filtered_lines)
        df.dropna(inplace=True)

        if save_formatted_data:
            print('Formatted data saved as %s_Formatted_Data.csv' % exp_name)
            df.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False, header=False)

        header = df.iloc[0]
        raw_data = df[2:]
        raw_data.columns = header
        raw_data = raw_data.drop(columns=['\n'])  # drops any incorrect formatting

        raw_data = raw_data.loc[:, ~(raw_data == '').any()]  # if scan stopped before fully complete, removes any unfinished columns

        raw_data = raw_data.astype(float)

    else:
        raw_data = pd.read_csv(os.path.join(base_folder, "%s_Formatted_Data.csv" % exp_name), header=[0, 1])
        raw_data = raw_data.droplevel(1, axis=1).drop(columns=['\n'])

    print('Preparing Heatmap data')

    wavelengths = defaultdict(list)

    if '_EX_' in raw_data.columns.to_list()[0]:  # defines which type of wavelength is in the header/columns
        wavelengths['emission'] = raw_data.iloc[:, 0].to_list()  # column wavelengths repeated throughout file
        header_type = 'excitation'
        header_sep = '_EX_'
        column_type = 'emission'
    elif '_EM_' in raw_data.columns.to_list()[0]:
        wavelengths['excitation'] = raw_data.iloc[:, 0].to_list()
        header_type = 'emission'
        header_sep = '_EM_'
        column_type = 'excitation'
    else:
        raise RuntimeError('Something is wrong in the data header - add either emission or excitation data only.')

    header_wavelengths = raw_data.columns.to_list()
    header_wavelengths_reps = []
    sample_names = []
    for i in range(0, len(header_wavelengths), 2):  # run through the header data, the wavelength is in every second cell
        split_header = header_wavelengths[i].split(header_sep)
        if '\n' in split_header:
            continue
        sname, h_wavelength = split_header[0], split_header[-1]
        if sname not in sample_names and sname != '\n':
            sample_names.append(sname)
        h_wavelength = float(h_wavelength)
        if h_wavelength != 0 and header_wavelengths[i] != '\n':
            # discards any 0 wavelengths, these are artifacts produced by Pandas.
            header_wavelengths_reps.append(h_wavelength)

    header_wavelength_positions = defaultdict(list)
    for index, wav in enumerate(header_wavelengths_reps):  # extracting positions of any duplicates (for averaging down the line)
        header_wavelength_positions[wav].append(index)

    wavelengths[header_type] = list(header_wavelength_positions.keys())

    replicates = len(list(header_wavelength_positions.values())[0])  # extracts number of replicates used from data

    if not plot_separately:
        print('Averaging samples')
        heatmap_data = np.zeros((len(wavelengths['emission']), (len(wavelengths['excitation']))))  # emission on y-axis, excitation on x-axis
        for i, ex in tqdm(enumerate(wavelengths[column_type]), total=len(wavelengths[column_type]), desc='%s wavelengths' % header_type):
            for j, (wav, wav_indices) in enumerate(header_wavelength_positions.items()):
                if header_type == 'emission':
                    heatmap_ordering = (j, i)
                else:
                    heatmap_ordering = (i, j)
                fixed_indices = [(ind * 2) + 1 for ind in wav_indices]
                # offsetting index positions to match file (data repeated once every 2 columns)
                replicate_data = raw_data.iloc[i, fixed_indices]
                heatmap_data[heatmap_ordering] = np.mean(replicate_data)  # averaging data according to number of replicates

        return heatmap_data, wavelengths, sample_names
    else:
        multi_heatmaps = []
        for s_index, sample in enumerate(sample_names):
            print('Preparing sample %s' % sample)
            heatmap_data = np.zeros((len(wavelengths['emission']), (len(wavelengths['excitation']))))  # emission on y-axis, excitation on x-axis
            for i, ex in tqdm(enumerate(wavelengths[column_type]), total=len(wavelengths[column_type]),
                              desc='%s wavelengths' % header_type):
                for j, (wav, wav_indices) in enumerate(header_wavelength_positions.items()):
                    if header_type == 'emission':
                        heatmap_ordering = (j, i)
                    else:
                        heatmap_ordering = (i, j)

                    if s_index >= len(wav_indices):  # sometimes not all wavelengths produced for every sample
                        heatmap_data[heatmap_ordering] = 0
                    else:
                        fixed_indices = [(ind * 2) + 1 for ind in wav_indices][s_index]
                        # offsetting index positions to match file (data repeated once every 2 columns)
                        replicate_data = raw_data.iloc[i, fixed_indices]
                        heatmap_data[heatmap_ordering] = replicate_data
            multi_heatmaps.append(heatmap_data)

        return multi_heatmaps, wavelengths, sample_names

