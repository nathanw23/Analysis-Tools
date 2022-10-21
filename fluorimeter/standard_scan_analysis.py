import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def cli_plot(df, exp_name, output_folder):
    sns.lineplot(data=df, x="Wavelength (nm)", y="Intensity (A.U.)", hue="Sample")
    plt.ylim(ymin=0)
    plt.title('%s Fluorescence Scan' % exp_name)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (AU)')

    plt.savefig(os.path.join(output_folder, f'{exp_name} Fluorescence_Scan.png'), dpi=300)


def fluorimeter_scan_analysis(data_file, **kwargs):

    df = pd.read_csv(data_file)
    if df.shape[1] % 2 != 0:
        df = df.iloc[:, :-1]
    df = df.dropna()

    raw_sample_names = df.columns.to_list()
    sample_names = raw_sample_names[::2]
    old_names = raw_sample_names[1::2]

    df2 = df.drop([0, 0])
    df2 = pd.melt(df2, id_vars=raw_sample_names[0], value_vars=raw_sample_names[1::2], var_name='Sample',
                  value_name='Intensity (A.U.)')
    df2 = df2.rename(columns={sample_names[0]: "Wavelength (nm)"})
    df2 = df2[["Sample", "Wavelength (nm)", "Intensity (A.U.)"]]
    df2['Sample'] = df2['Sample'].replace(old_names, sample_names)
    df2[["Wavelength (nm)", "Intensity (A.U.)"]] = df2[["Wavelength (nm)", "Intensity (A.U.)"]].apply(pd.to_numeric)

    return df2
