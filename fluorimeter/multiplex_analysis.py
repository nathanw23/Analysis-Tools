import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from shared_functions import csv_read_and_break_filter

def cli_multiplex_plot(df, output_folder, exp_name):
    grid = sns.FacetGrid(df, col='Group', row='Fluorophore', margin_titles=True)
    grid.map(sns.lineplot, "Time (min)", "Intensity (A.U.)", ci="sd", palette="colorblind")
    grid.savefig(os.path.join(output_folder, f"{exp_name}_MultiplexFacet.pdf"), dpi=300)

def fluorimeter_multiplex_analysis(data_file):

    filtered_lines = csv_read_and_break_filter(data_file)  # reads in data and filters any logs

    df = pd.DataFrame(filtered_lines)

    if df.shape[1] % 2 != 0:
        df = df.iloc[:, :-1]  # Removes the empty column at the end of the dataframe if dataframe has odd number of columns
    df = df.dropna()

    sample_names = [sname for sname in df.iloc[0].to_list() if sname]
    df = df.iloc[2:, :]  # Removes the first/second row from the dataframe, as these do not contain data

    sample_number = len(sample_names)  # Gets the number of samples

    appended_data1 = []  # Initialises appended data list
    appended_data2 = []  # Initialises appended data list

    for y in range(0, len(df.columns), 2):  # Loop to concat the timepoints to one column
        appended_data1.append(df[y])
    df_concat1 = pd.concat(appended_data1)

    for x in range(1, len(df.columns), 2):  # Loop to concat the signals to one column
        appended_data2.append(df[x])
    df_concat2 = pd.concat(appended_data2)

    df_combined = pd.concat([df_concat1, df_concat2], axis=1)  # Combines the time and signal columns into one dataframe
    df_combined = df_combined.reset_index(drop=True)  # Resets the index
    dataframe_length = len(df_combined.index)  # Gets the length of the dataframe

    round = dataframe_length / sample_number  # Calculates the number of datapoints for each group
    names = sample_names * int(round)  # Creates a list of each of the group names for each sample
    sorted_list = sorted(names,
                         key=sample_names.index)  # Orders the list in the order they first appeated in the original dataframe
    df_combined['Group'] = sorted_list  # Adds a list of groups to the dataframe

    # Renames the columns
    df_combined = df_combined.rename(columns={df_combined.columns[0]: 'Time (min)', df_combined.columns[1]: 'Intensity (A.U.)'})

    df_combined = df_combined[['Group', 'Time (min)', 'Intensity (A.U.)']]  # Reorders the columns

    df_combined['Time (min)'] = pd.to_numeric(df_combined['Time (min)'])  # Converts the time column from object type to float
    df_combined['Intensity (A.U.)'] = pd.to_numeric(df_combined['Intensity (A.U.)'])  # # Converts the signal column from object type to float

    df_combined[['Group', 'Wavelengths']] = df_combined['Group'].str.split('_', 1, expand=True) # Splits the wavelengths from the sample names

    wavelengths = df_combined['Wavelengths'].unique() # Gets the unique wavelengths

    fluorophores = [] # Initialises list to store fluorophores

    for i in wavelengths:
        fluor = input(f"{i} = ")
        fluorophores.append(fluor)

    res = {wavelengths[i]: fluorophores[i] for i in range(len(wavelengths))} # Creates a dictionary

    df_combined['Fluorophore'] = df_combined['Wavelengths'].replace(res) # Creates a new column with the name of the fluorophores for easier reference

    return df_combined