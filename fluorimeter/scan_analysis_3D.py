import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
from tqdm.rich import tqdm
import sys
from shared_functions import csv_read_and_break_filter
import warnings
from tqdm import TqdmExperimentalWarning
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

def get_pivot_tables(df_data):
    pivot_table_dict = {}
    for sample_name in tqdm(df_data["Sample"].unique()):
        unformatted_exem = df_data.loc[df_data["Sample"] == sample_name]
        unformatted_exem = unformatted_exem.drop(["Sample"], axis=1)
        pivot_table_dict[sample_name] = unformatted_exem.pivot_table(index="Emission", columns="Excitation", values="Intensity")
    return pivot_table_dict

def cli_plot_heatmap(
  fdata,
  c_axis,
  base_folder,
  plot_separately,
  **kwargs     
):
    
    all_dicts = get_pivot_tables(fdata)

    if  plot_separately == True:
        for x in all_dicts:
            ax = sns.heatmap(all_dicts[x], cmap='viridis', vmin=0, vmax=c_axis)
            ax.invert_yaxis()
            plt.savefig(
                os.path.join(base_folder, f"{x}_3DScan.png"), dpi=300, bbox_inches="tight"
            )
            plt.figure()
    else:
        temp = 0

        for x in all_dicts:
            temp += all_dicts[x]

        average_data = temp / len(all_dicts)

        ax = sns.heatmap(average_data, cmap='viridis', vmin=0, vmax=c_axis)
        ax.invert_yaxis()
        plt.savefig(
            os.path.join(base_folder, "Average_3DScan.png"), dpi=300, bbox_inches="tight"
        )





def interpret_3d_scan(
    data_file,
    plot_separately,
    save_formatted_data=True,
    **kwargs
):
    
    base_folder = os.path.dirname(data_file)
    exp_name = data_file.split(os.sep)[-1].rsplit(".", 1)[0]

    # Imports the data as a pandas data frame after removing the lof at the bottom of the csv file
    filtered_lines = csv_read_and_break_filter(data_file)
    df = pd.DataFrame(filtered_lines)
    df.dropna(inplace=True)

    df = df.drop(labels=1, axis=0) # Drops non-needed headings

    # Gets headings into list
    headings = df.loc[0, ].values.flatten().tolist()
    headings = headings[0::2] # Removes the gaps
    headings = headings[:-1] # Removes the last value from the list
    headings = ["Emission"] + headings

    # Drops non-needed headings
    df = df.drop(labels=0, axis=0)

    # Selects the first column
    wavelengths = df.iloc[:,0]
    wavelengths = wavelengths.astype(float).round(decimals=2)

    # Selects the data columns
    intensities = df[[k for k in df.columns if k % 2 !=0]]

    data = pd.concat([wavelengths, intensities], axis=1)

    data.columns = headings

    fdata = pd.melt(frame=data, id_vars="Emission", var_name="Excitation", value_name="Intensity")

    fdata[["Sample", "Bin", "Excitation"]] = fdata.Excitation.str.split("_", expand=True)

    fdata = fdata.drop(["Bin"], axis=1)
    fdata = fdata.reindex(columns=["Sample", "Excitation", "Emission", "Intensity"]) # Data now in long format need to split into separate wide dataframe
    fdata = fdata.astype({"Emission": float, "Excitation": float, "Intensity": float})
    
    if save_formatted_data:
        fdata.to_csv(
                os.path.join(base_folder, "%s_Formatted_Data.csv" % exp_name),
                encoding="utf-8",
                index=False,
                header=True,
            )   
    else:
        pass

    return fdata