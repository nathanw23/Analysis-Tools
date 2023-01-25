import pandas as pd
import numpy as np
import seaborn as sns
import os


def cli_multiplex_plot(df, output_folder, exp_name):
    grid = sns.FacetGrid(df, col='Group', row='Fluorophore', margin_titles=True)
    grid.map(sns.lineplot, "Converted_Time", "Signal", ci="sd", palette="colorblind")
    grid.savefig(os.path.join(output_folder, f"{exp_name}_MultiplexFacet.pdf"), dpi=300)


def cleanup_multiplex_data(data_file, labels, fluorophores, **kwargs):
    """
    Reads in a platereader multiplexed timeseries file and formats data for plotting.  Assumes data has an additional
    'Group' column for averaging results.
    :param data_file: filepath to input file.
    :param labels: Label to apply to each averaged group (list).
    :param fluorophores: List of fluorophores corresponding to header wavelength columns.
    :return: Clean pandas dataframe.
    """
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

    return df2
