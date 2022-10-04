"""
PlateReader_Kinetics_Analysis.py

Python script to format and plot plate reader kinetics data.

v1, Nathan Wu, 21-Oct-2021
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
import click 
from shared_functions import generate_quote


@click.command()
@click.option('--data_file', required=True, help='Data file for analysis. Different conditions must be different groups in the plate layout.')
@click.option('--labels', required=True, help='Labels for the figure legend separated by commas (no spaces)')

def interpret_plate_kinetics(data_file, labels):
    
    legend_labels = labels.split(",") #Places the lables provided in a list
    
    base_folder = os.path.dirname(data_file) #Sets the base file
    exp_name = data_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]

    df = pd.read_csv(data_file, skiprows=6) #Reads in the csv file and removes the extra rows
    
    df.drop(['Time'],axis=1,inplace=True) #Removes the unnecesary column
    
    df2=pd.melt(df,id_vars=['Unnamed: 0', 'Unnamed: 2'], var_name='Timepoint', value_name='Signal') #Converts the data from wide format to long format for plotting
    
    df2.rename({'Unnamed: 0': 'Well', 'Unnamed: 2': 'Group'}, axis=1, inplace=True) #Renames the first column to 'Group" to be more descriptive 
    
    df2['Extracted_Minute'] = df2['Timepoint'].str.split('min').str[0].astype(int) #Extracts minute value
    
    df2['Extracted_Second'] = df2['Timepoint'].str.split('min').str[1]
    df2['Extracted_Second'] = df2['Extracted_Second'].str.split('s').str[0]
    df2['Extracted_Second'] = df2['Extracted_Second'].replace(r'^\s*$', np.NaN, regex=True).astype(float)
    df2['Extracted_Second'] = df2['Extracted_Second'].fillna(0) #Code  extracts  the second value and sets NaNs to 0
    
    df2['Converted_Time'] = (((df2['Extracted_Minute'] * 60) + df2['Extracted_Second']) / 60).round(2) #Converts time to a minute decimal
    
    n_number=df2.query('Group == "A" and Converted_Time == 0').Group.count() #Calculates the replicate number
    
    Groups = df2['Group'].unique().tolist() #Extracts the number groups labels assigned by the plate reader into a list
    Groups.sort() #Orders the groups in alphabetical order to replace groups with legend labels
    df2["Group"] = df2["Group"].replace(Groups, legend_labels) #Changes the plate reader assigned group names with the user assigned group names
    
    df2 = df2.drop(columns=['Extracted_Minute', 'Extracted_Second'])
    df2.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False) #Exports the formatted datafram as a CSV file 
    
    summary = df2.groupby(["Group", "Converted_Time"])["Signal"].describe() #Produces data summary for each group and timepoint
    summary.to_csv(os.path.join(base_folder, '%s_Data_Summary.csv' % exp_name), encoding='utf-8') #Exports a data summary to a csv file
    
    max_time = df2['Converted_Time'].max() #To determine the max time for the x axis limit 
    
    sns.color_palette("colorblind")
    
    ax = sns.lineplot(data=df2, x='Converted_Time', y='Signal', hue='Group', ci="sd", palette="colorblind") #Plots a line graph of the average for each group at each time point
    if n_number == 1:
        ax.set_title('%s Kinetics Scan' % (exp_name), wrap=True)
    else:
        ax.set_title('%s Kinetics Scan (N = %s, Band = Standard Deviation)' % (exp_name, n_number), wrap=True) #Adds a title to the graph with the correct n number
    ax.set(xlabel='Time (min)', ylabel='Signal (A.U.)') #Labels the axis
    plt.legend(labels=legend_labels)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    ax.set_xlim(0,max_time)
    
    plt.savefig(os.path.join(base_folder, '%s_Plate_Kinetics' % exp_name), bbox_inches='tight', dpi=300) #Saves the graph with an appropiate file name
    #plt.show()
    
    generate_quote()
