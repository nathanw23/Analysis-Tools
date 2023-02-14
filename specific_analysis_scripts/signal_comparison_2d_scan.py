from fluorimeter.standard_scan_analysis import fluorimeter_scan_analysis
import os
import numpy as np

folder = "../scratch_data/"

region_of_interest = (570, 590)
volume_dropdown = 5

files = [
    "1000V_medium_emission_scan_3_100_em_10.csv",
    "1000V_medium_emission_scan.csv",
    "1000V_medium_emission_scan_3_100_try_2.csv",
    "1000V_medium_emission_scan_4_block_6.csv",
]
sample_combos = [
    ("PC 100ul (10nM)", "PC 7mm 25ul (10nM)"),
    ("PC 100ul (10nM)", "PC 25ul (50nM)"),
    ("PC 100ul (10nM)", "PC 7mm 25ul (10nM)"),
    ("PC 100ul (10nM)", "PC 7mm 25ul (50nM)"),
]
relative_concentrations = [(1, 1), (1, 5), (1, 1), (1, 5)]

for pos_index in range(len(files)):
    df, metadata = fluorimeter_scan_analysis(os.path.join(folder, files[pos_index]))
    sample_1, sample_2 = (
        sample_combos[pos_index][0],
        sample_combos[pos_index][1],
    )
    s1 = df.loc[
        (df["Sample"] == sample_1)
        & (df["Wavelength (nm)"] < region_of_interest[1])
        & (df["Wavelength (nm)"] > region_of_interest[0])
    ]
    s1 = np.array(s1["Intensity (A.U.)"])
    s2 = df.loc[
        (df["Sample"] == sample_2)
        & (df["Wavelength (nm)"] < region_of_interest[1])
        & (df["Wavelength (nm)"] > region_of_interest[0])
    ]
    s2 = np.array(s2["Intensity (A.U.)"])

    signal_gain = np.average(s2 / s1)
    rel_conc = (
        relative_concentrations[pos_index][1] / relative_concentrations[pos_index][0]
    )

    print(
        "Analysis of signal change between samples %s and %s, from file %s:"
        % (sample_1, sample_2, files[pos_index])
    )
    print(
        "Across emission region of interest (%s), average signal gain/drop is %s for black cuvettes (%s times less volume),"
        " with a relative increase in concentration of %s"
        % (region_of_interest, signal_gain, volume_dropdown, rel_conc)
    )
    print(
        "I.e. black cuvette improved signal by a factor of %s."
        % ((signal_gain * volume_dropdown) / rel_conc)
    )
    print("------")
