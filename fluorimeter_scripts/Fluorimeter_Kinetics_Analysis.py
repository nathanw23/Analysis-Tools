
'''
Fluorimeter_Kinetics_Analysis.py

Python script to format and plot fluorimeter scan data 

v1, Nathan Wu, 23-Sep-2021
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import click
from shared_functions import generate_quote


@click.command()
@click.option('--data_file', required=True, help='Data file for analysis.')
 
def fluorimeter_kinetics_analysis(data_file):
   
    base_folder = os.path.dirname(data_file) # Sets the base folder to the directory of the inputed data file
    exp_name = data_file.split(os.sep)[-1] # Extracts the experiment name from the name of the data file
    exp_name = exp_name.rsplit('.', 1)[0] # Removes the file extension from the experiment name
    
    df = pd.read_csv(data_file) # Reads in tge data csv file as a dataframe
    if df.shape[1] %2 != 0: df = df.iloc[: , :-1] # Removes the empty column at the end of the dataframe if dataframe has odd number of columns
    df = df.dropna() # Drops the extra information at the bottom of the data file
    df = df.iloc[1: , :] # Removes the second row from the dataframe

    raw_sample_names = df.columns.to_list() # Extracts column headers to a list
    sample_names = raw_sample_names[::2] # Selects the sample names from the header
    old_names = raw_sample_names[1::2] # Selects the other column headers from the list
    sample_number = len(sample_names) # Gets the number of samples
    
    appended_data1 = [] # Initialises appeneded data list
    appended_data2 = [] # Initialises appeneded data list
    
    for x in sample_names: # Loop to concat the time's to one column
        appended_data1.append(df[x])
        df_concat1 = pd.concat(appended_data1)
        
    for y in old_names: # Loop to concat the signal's to one column
        appended_data2.append(df[y])
        df_concat2 = pd.concat(appended_data2)
        
        
    df_combined = pd.concat([df_concat1,df_concat2], axis=1) # Combines the time and signal columns into one dataframe
    df_combined = df_combined.reset_index(drop=True) # Resets the index
    dataframe_length = len(df_combined.index) # Gets the length of the dataframe
    
    round = dataframe_length / sample_number # Calculates the number of datapoints for each group
    names = sample_names * int(round) # Creates a list of each of the group names for each sample
    sorted_list = sorted(names, key=sample_names.index) # Orders the list in the order they first appeated in the original dataframe
    df_combined['Group'] = sorted_list # Adds a list of groups to the dataframe
    
    df_combined = df_combined.rename(columns={0:'Time (min)', 1:'Intensity (A.U.)'}) # Renames the columns
    
    df_combined = df_combined[['Group', 'Time (min)', 'Intensity (A.U.)']] # Reorders the columns
    
    df_combined['Time (min)'] = pd.to_numeric(df_combined['Time (min)']) # Converts the time column from object type to float
    df_combined['Intensity (A.U.)'] = pd.to_numeric(df_combined['Intensity (A.U.)']) # # Converts the signal column from object type to float

    max_time = df_combined['Time (min)'].max() # Gets the max time for the x-axis limits
    
    df_combined.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False) # Saves the updates dataframe to a csv file
    
    summary = df_combined.groupby(["Group", "Time (min)"])["Intensity (A.U.)"].describe()
    summary.to_csv(os.path.join(base_folder, '%s_Data_Summary.csv' % exp_name), encoding='utf-8')
    
    sns.lineplot(data=df_combined, x="Time (min)", y="Intensity (A.U.)", hue="Group", palette='colorblind') # Plots the data
    
    plt.ylim(ymin=0)
    plt.xlim(xmin=0, xmax=max_time)
    plt.title(f'{exp_name} Kinetics Scan')
    plt.xlabel('Time (min)')
    plt.ylabel('Intensity (A.U.)')

    plt.savefig(os.path.join(base_folder, f'{exp_name}_Kinetics_Scan.png'), dpi=300) # Saves the graph
    #plt.show()   
    
    generate_quote()
