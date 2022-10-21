import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def cli_absorbance_plot(df, output_folder, exp_name):
    sns.lineplot(data=df, x="Wavelength (nm)", y="Absorbance", color='red')
    plt.ylim(ymin=0)
    plt.xlim(190, 840)
    plt.title('%s Nano Drop Analysis' % exp_name)
    plt.savefig(os.path.join(output_folder, '%s_NanoDropAnalysis.png' % exp_name))


def absorbance_setup(data_file, **kwargs):
    df = pd.read_csv(data_file, sep="\t", skiprows=2)  # Skips the top two rows in imported tsv file
    return df
