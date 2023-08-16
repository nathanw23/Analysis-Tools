import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def cli_EDIWN_kinetics_plot(df, output_folder, exp_name):
    n_number = df.query('Group == "A" and "Time (min)" == 0').Group.count()  # calculates the replicate number

    ax = sns.lineplot(data=df, x="Time (min)", y="Intensity (A.U.)", hue="Group", ci="sd")  # plots a line graph of the average for each group at each time point

    if n_number == 1:
        ax.set_title(f"{exp_name} Kinetics Scan", wrap=True)
    else:
        ax.set_title(
            f"{exp_name} Kinetics Scan (N={n_number}, Band=Standard Deviation)",wrap=True,)  # adds a title to the graph with the correct n number
    ax.set(xlabel="Time (min)", ylabel="Signal (A.U.)")  # labels the axis
    plt.savefig(os.path.join(output_folder, f"{exp_name}_EDWIN_Kinetics"), dpi=300)  # saves the graph with the correct file name in the same folder as the data


def EDWIN_kinetics_analysis(data_file, **kwargs):
    df = pd.read_excel(
        data_file, skiprows=10
    )  # reads in data and removes logs from the top of the file
    df["Well"] = df["Unnamed: 0"] + df["Unnamed: 1"].astype(str)  # Combines well row and well column columns
    df.drop(["Unnamed: 0", "Unnamed: 1", "Unnamed: 2"], axis=1, inplace=True)  # removes unnecessary columns
    df.rename(columns={"Unnamed: 3": "Group"}, inplace=True)  # renames group column

    df2 = pd.melt(df,id_vars=["Well", "Group"],var_name="Time (min)",value_name="Intensity (A.U.)")  # converts data from wide format to long format for plotting

    return df2
