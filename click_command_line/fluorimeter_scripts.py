import click
from shared_functions import generate_quote
import os


@click.command()
@click.option("--data_file", required=True, help='Specify location of input data file.')
@click.option("--format_data", is_flag=True, default=None, help='Set this flag to generate and save formatted data.')
def click_fluorimeter_scan(**kwargs):
    from fluorimeter.standard_scan_analysis import fluorimeter_scan_analysis, cli_plot

    df = fluorimeter_scan_analysis(**kwargs)
    base_output_folder = os.path.dirname(kwargs['data_file'])

    exp_name = kwargs['data_file'].split(os.sep)[-1].rsplit('.', 1)[0]

    cli_plot(df, exp_name, base_output_folder)
    if kwargs['format_data']:
        df.to_csv(os.path.join(base_output_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False)

    generate_quote()


@click.command()
@click.option('--data_file', required=True,
              help='Data file for analysis. Fluorimeter must be set to EXCITATION or EMISSION scan mode')
@click.option('--c_axis', type=click.IntRange(0, 1000), default=400, show_default=True,
              help='Set the maximum value of the colourbar')
@click.option('--plot_separately', is_flag=True, help='Set this flag to plot all samples separately')
@click.option('--preformatted_data', is_flag=True,
              help='Set this flag to read samples from formatted file rather than from raw data.')
def click_3d_scan(**kwargs):
    from fluorimeter.scan_analysis_3D import interpret_3d_scan, cli_plot_heatmap

    base_output_folder = os.path.dirname(kwargs['data_file'])
    exp_name = kwargs['data_file'].split(os.sep)[-1].rsplit('.', 1)[0]

    heatmap_data, wavelengths, sample_names = interpret_3d_scan(**kwargs, save_formatted_data=True)

    print("Plotting Data...")
    if isinstance(heatmap_data, list):
        for heatmap, sample in zip(heatmap_data, sample_names):
            cli_plot_heatmap(heatmap, wavelengths['excitation'], wavelengths['emission'], kwargs['c_axis'],
                             base_output_folder, exp_name, sample_info=sample)
    else:
        cli_plot_heatmap(heatmap_data, wavelengths['excitation'], wavelengths['emission'], kwargs['c_axis'],
                         base_output_folder, exp_name)
    print('Done!')

    generate_quote()


@click.command()
@click.option('--data_file', required=True, help='Data file for analysis.')
@click.option("--format_data", is_flag=True, default=None, help='Set this flag to generate and save formatted data.')
def click_kinetics_analysis(**kwargs):
    from fluorimeter.kinetics_analysis import fluorimeter_kinetics_analysis, cli_kinetics_lineplot

    base_folder = os.path.dirname(kwargs['data_file'])  # Sets the base folder to the directory of the inputed data file
    exp_name = kwargs['data_file'].split(os.sep)[-1].rsplit('.', 1)[0]

    df = fluorimeter_kinetics_analysis(kwargs['data_file'])

    if kwargs['format_data']:
        df.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False)  # Saves the updates dataframe to a csv file
        summary = df.groupby(["Group", "Time (min)"])["Intensity (A.U.)"].describe()
        summary.to_csv(os.path.join(base_folder, '%s_Data_Summary.csv' % exp_name), encoding='utf-8')

    cli_kinetics_lineplot(df, exp_name, base_folder)

    generate_quote()

@click.command()
@click.option("--data_file", required=True, help='Specify location of input data file.')
@click.option("--format_data", is_flag=True, default=None, help='Set this flag to generate and save formatted data.')
def click_multiplex_fluorimeter(**kwargs):
    from fluorimeter.multiplex_analysis import fluorimeter_multiplex_analysis, cli_multiplex_plot

    base_folder = os.path.dirname(kwargs['data_file'])  # Sets the base folder to the directory of the inputed data file
    exp_name = kwargs['data_file'].split(os.sep)[-1].rsplit('.', 1)[0]

    df = fluorimeter_multiplex_analysis(kwargs['data_file'])

    exp_name = kwargs['data_file'].split(os.sep)[-1].rsplit('.', 1)[0]

    cli_multiplex_plot(df, base_folder, exp_name)

    if kwargs['format_data']:
        df.to_csv(os.path.join(base_folder, '%s_Formatted_Data.csv' % exp_name), encoding='utf-8', index=False)

    generate_quote()

