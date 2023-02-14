import pandas as pd
import matplotlib.pyplot as plt
import os


def platereader_spot_bar_plot(data_file, labels, fluorophores, **kwargs):
    """
    Reads in a platereader file with spot data (only one time point) and plots a bar graph with the results.
    The output graph is saved in the same folder as the input.
    :param data_file: Filepath of input file.
    :param labels: List of labels corresponding to each sample in file (in order).
    :param fluorophores: List of fluorophores used (mapping to data columns in order).
    :return: Dataframe with formatted data.
    """

    with open(data_file, "r") as f:
        for index, line in enumerate(f.readlines()):
            if "Well" in line:
                header_row = index
                break

    df = pd.read_csv(data_file, skiprows=header_row, header=[0])
    df.drop(columns=df.columns[-1], axis=1, inplace=True)
    df.rename(
        columns={
            colname: fluoro_name
            for colname, fluoro_name in zip(df.columns[3:], fluorophores)
        },
        inplace=True,
    )
    df["Sample"] = labels
    df.plot(x="Sample", y=["Atto550", "Atto647N"], kind="bar", rot=90)
    plt.ylabel("Intensity (Arbitrary Units)")
    plt.tight_layout()

    file_name = os.path.basename(data_file)
    file_folder = os.path.dirname(data_file)

    plt.savefig(os.path.join(file_folder, "%s_barplot.pdf" % file_name))

    return df
