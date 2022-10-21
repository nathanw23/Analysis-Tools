import pandas as pd
import numpy as np
import seaborn as sns
import os
from shared_functions import generate_quote


def cleanup_multiplex_data(data_file, labels, fluorophores):
    base_folder = os.path.dirname(data_file)  # Sets the base file
    exp_name = data_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit(".", 1)[0]

    df = pd.read_csv(data_file, skiprows=5, header=[0, 1])
    df.drop(columns=df.columns[:2], axis=1, inplace=True)

    df.columns = df.columns.map(" ".join)  # Combines to two headers

    df2 = pd.melt(df, id_vars=df.iloc[:, :1], var_name="Temp", value_name="Signal")
    df2.rename(columns={df2.columns[0]: "Group"}, inplace=True)
    df2[["Wavelength", "Time"]] = df2["Temp"].str.split(")", expand=True)
    df2.drop(["Temp"], axis=1, inplace=True)
    df2['Extracted_Minute'] = df2['Time'].str.split('min').str[0].astype(int)
    df2['Extracted_Second'] = df2['Time'].str.split('min').str[1]
    df2['Extracted_Second'] = df2['Extracted_Second'].str.split('s').str[0]
    df2['Extracted_Second'] = df2['Extracted_Second'].replace(r'^\s*$', np.NaN, regex=True).astype(float)
    df2['Extracted_Second'] = df2['Extracted_Second'].fillna(0)
    df2['Converted_Time'] = (((df2['Extracted_Minute'] * 60) + df2['Extracted_Second']) / 60).round(2)
    df2.drop(["Extracted_Minute", "Extracted_Second", "Time"], axis=1, inplace=True)
    df2["Wavelength"] = df2["Wavelength"].str[11:-2]

    groups = df2["Group"].unique().tolist()
    groups.sort()
    conditions = labels.split(",")
    df2["Group"] = df2["Group"].replace(groups, conditions)

    wavelengths = df2["Wavelength"].unique().tolist()
    fluoros = fluorophores.split(",")
    df2["Fluorophore"] = df2["Wavelength"].replace(wavelengths, fluoros)

    df2.to_csv(os.path.join(base_folder, f"{exp_name}_Formatted_Data.csv"), encoding="utf-8", index=False)

    grid = sns.FacetGrid(df2, col='Group', row='Fluorophore', margin_titles=True)
    grid.map(sns.lineplot, "Converted_Time", "Signal", ci="sd", palette="colorblind")
    grid.savefig(os.path.join(base_folder, f"{exp_name}_MultiplexFacet.pdf"), dpi=300)

    generate_quote()
