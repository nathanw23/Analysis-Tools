import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import defaultdict


def cli_absorbance_plot(df, output_folder, exp_name):
    """
    Plots all nanodrop absorbances as a line plot.
    :param df: Nanodrop dataframe (with wavelength as index)
    :param output_folder: Output folder to save plots
    :param exp_name: Experiment filename
    :return: None
    """
    ax = sns.lineplot(data=df)
    ax.set(ylabel='Absorbance (AU)')
    plt.ylim(ymin=0)
    plt.xlim(190, 840)
    plt.title("%s Nano Drop Analysis" % exp_name)
    plt.savefig(os.path.join(output_folder, "%s_NanoDropAnalysis.pdf" % exp_name))


def absorbance_setup(data_file, **kwargs):
    """
    Reads in a nanodrop file and returns a dataframe with all absorbances.
    :param data_file: Input file location.
    :param kwargs: N/A.
    :return: Formatted dataframe.
    """
    name_location = 0
    data = defaultdict(list)
    name_incoming = True

    with open(data_file, 'r') as f:
        for index, line in enumerate(f):
            stripped_line = line.strip()
            if stripped_line == '':  # new datasets are always separated by a blank line
                name_incoming = True
                continue
            if name_incoming:  # gathers name from file
                name_location = index
                current_name = stripped_line
                name_incoming = False
            elif index > name_location + 2 and stripped_line != '':  # data starts 2 lines after the name
                if name_location == 0:  # only gathers wavelength data once
                    data['Wavelength (nm)'].append(float(stripped_line.split('\t')[0]))
                data[current_name].append(float(stripped_line.split('\t')[-1]))  # gathers absorbance data

    df = pd.DataFrame.from_dict(data)
    df.set_index('Wavelength (nm)', inplace=True)

    return df
