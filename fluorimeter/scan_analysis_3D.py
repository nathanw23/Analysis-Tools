import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from shared_functions import csv_read_and_break_filter


def get_pivot_tables(df_data):
    """
    Extracts a pivot table for each sample in the dataframe (assumes 'Sample' column exists)
    :param df_data: Input combined dataframe
    :return: dictionary of split samples, with one dataframe per entry
    """
    pivot_table_dict = {}
    for sample_name in df_data["Sample"].unique():
        unformatted_exem = df_data.loc[df_data["Sample"] == sample_name]
        unformatted_exem = unformatted_exem.drop(["Sample"], axis=1)
        pivot_table_dict[sample_name] = unformatted_exem.pivot_table(index="Emission", columns="Excitation",
                                                                     values="Intensity")
    return pivot_table_dict


def cli_plot_heatmap(fdata, c_axis, base_folder, plot_separately):
    """
    Plots all provided samples into a heatmap
    :param fdata: Dataframe containing all data (long format)
    :param c_axis: Maximum value for colorbar
    :param base_folder: Output folder to save plots
    :param plot_separately: Set to true to save each sample separately, otherwise all inputs will be averaged
    :return: None
    """
    all_dicts = get_pivot_tables(fdata)

    if plot_separately:
        for x in all_dicts:

            plt.figure()
            ax = sns.heatmap(all_dicts[x], cmap='viridis', vmin=0, vmax=c_axis)
            ax.invert_yaxis()

            plt.title("%s 3D Fluorescence Scan" % x)
            plt.xlabel("Excitation Wavelengths (nm)")
            plt.ylabel("Emission Wavelengths (nm)")

            plt.savefig(
                os.path.join(base_folder, f"{x}_3DScan.png"), dpi=300, bbox_inches="tight"
            )
            plt.close()

    else:
        temp = 0

        for x in all_dicts:
            temp += all_dicts[x]

        average_data = temp / len(all_dicts)

        plt.figure()
        ax = sns.heatmap(average_data, cmap='viridis', vmin=0, vmax=c_axis)
        ax.invert_yaxis()

        plt.title("Averaged 3D Fluorescence Scan")
        plt.xlabel("Excitation Wavelengths (nm)")
        plt.ylabel("Emission Wavelengths (nm)")

        plt.savefig(os.path.join(base_folder, "Average_3DScan.png"), dpi=300, bbox_inches="tight")
        plt.close()


def interpret_3d_scan(data_file, save_formatted_data=True):
    """
    Reads in raw 3D data from fluorimeter, converts into a human-readable format and prepares data for plotting.
    :param data_file: Input datafile path
    :param save_formatted_data: Set to true to save the formatted data as a csv file next to the input file
    :return: Pandas-formatted dataframe
    """
    base_folder = os.path.dirname(data_file)
    exp_name = data_file.split(os.sep)[-1].rsplit(".", 1)[0]

    # Imports the data as a pandas data frame after removing the lof at the bottom of the csv file
    filtered_lines = csv_read_and_break_filter(data_file)
    df = pd.DataFrame(filtered_lines)
    df.dropna(inplace=True)

    df = df.drop(labels=1, axis=0)  # Drops non-needed headings

    # Gets headings into list
    headings = df.iloc[0, ].tolist()
    headings = headings[0::2][:-1]  # Removes the gaps and last value from the list

    # Drops headings from main dataframe after extraction
    df = df.drop(labels=0, axis=0)
    df = df.loc[:, ~(df == "").any()]  # if scan stopped before fully complete, removes any unfinished columns

    # finds out if excitation or emission is in the data headers and extracts relevant information
    if ("_EX_" in headings[0]):  # defines which type of wavelength is in the header/columns
        header_type = "Excitation"
        column_type = "Emission"
        header_sep = "_EX_"
    elif "_EM_" in headings[0]:
        header_type = "Emission"
        column_type = "Excitation"
        header_sep = "_EM_"
    else:
        raise RuntimeError("Something is wrong in the data header - add either emission or excitation data only.")

    headings = [column_type] + headings
    column_wavelengths = df.iloc[:, 0].astype(float).round(decimals=2)

    # Selects the data columns
    intensities = df[[k for k in df.columns if k % 2 != 0]]

    data = pd.concat([column_wavelengths, intensities], axis=1)  # re-attaches the column wavelengths to the data
    data.columns = headings

    fdata = pd.melt(frame=data, id_vars=column_type, var_name=header_type, value_name="Intensity") # converts to long format

    fdata[["Sample", header_type]] = fdata[header_type].str.split(header_sep, expand=True) # extracts additional wavelengths from headers

    fdata = fdata.reindex(columns=["Sample", "Excitation", "Emission",
                                   "Intensity"])  # Data now in long format, need to split into separate standardised wide dataframe
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
