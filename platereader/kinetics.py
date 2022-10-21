import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os


def cli_lineplot(df, output_folder, exp_name, labels):
    legend_labels = labels.split(",")
    sns.color_palette("colorblind")
    n_number = df.query('Group == "A" and Converted_Time == 0').Group.count()  # Calculates the replicate number

    ax = sns.lineplot(data=df, x='Converted_Time', y='Signal', hue='Group', ci="sd",
                      palette="colorblind")  # Plots a line graph of the average for each group at each time point
    if n_number == 1:
        ax.set_title('%s Kinetics Scan' % (exp_name), wrap=True)
    else:
        ax.set_title('%s Kinetics Scan (N = %s, Band = Standard Deviation)' % (exp_name, n_number),
                     wrap=True)  # Adds a title to the graph with the correct n number
    ax.set(xlabel='Time (min)', ylabel='Signal (A.U.)')  # Labels the axis
    plt.legend(labels=legend_labels)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    ax.set_xlim(0, df['Converted_Time'].max())

    plt.savefig(os.path.join(output_folder, '%s_Plate_Kinetics' % exp_name), bbox_inches='tight',
                dpi=300)  # Saves the graph with an appropiate file name


def interpret_plate_kinetics(data_file, labels, **kwargs):
    legend_labels = labels.split(",")  # Places the lables provided in a list

    df = pd.read_csv(data_file, skiprows=6)  # Reads in the csv file and removes the extra rows

    df.drop(['Time'], axis=1, inplace=True)  # Removes the unnecesary column

    df2 = pd.melt(df, id_vars=['Unnamed: 0', 'Unnamed: 2'], var_name='Timepoint',
                  value_name='Signal')  # Converts the data from wide format to long format for plotting

    df2.rename({'Unnamed: 0': 'Well', 'Unnamed: 2': 'Group'}, axis=1,
               inplace=True)  # Renames the first column to 'Group' to be more descriptive

    df2['Extracted_Minute'] = df2['Timepoint'].str.split('min').str[0].astype(int)  # Extracts minute value

    df2['Extracted_Second'] = df2['Timepoint'].str.split('min').str[1]
    df2['Extracted_Second'] = df2['Extracted_Second'].str.split('s').str[0]
    df2['Extracted_Second'] = df2['Extracted_Second'].replace(r'^\s*$', np.NaN, regex=True).astype(float)
    df2['Extracted_Second'] = df2['Extracted_Second'].fillna(0)  # Code  extracts  the second value and sets NaNs to 0

    df2['Converted_Time'] = (((df2['Extracted_Minute'] * 60) + df2['Extracted_Second']) / 60).round(2)  # Converts time to a minute decimal

    Groups = df2['Group'].unique().tolist()  # Extracts the number group labels assigned by the plate reader into a list
    Groups.sort()  # Orders the groups in alphabetical order to replace groups with legend labels

    # Changes the plate reader assigned group names with the user assigned group names
    df2["Group"] = df2["Group"].replace(Groups, legend_labels)

    df2 = df2.drop(columns=['Extracted_Minute', 'Extracted_Second'])

    return df2

