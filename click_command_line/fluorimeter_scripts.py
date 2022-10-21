import click


@click.command()
@click.option("--data_file", required=True, help='Specify location of input data file.')
def click_fluorimeter_scan(**kwargs):
    from fluorimeter.standard_scan_analysis import fluorimeter_scan_analysis

    fluorimeter_scan_analysis(**kwargs)


@click.command()
@click.option('--data_file', required=True,
              help='Data file for analysis. Fluorimeter must be set to EXCITATION or EMISSION scan mode')
@click.option('--c_axis', type=click.IntRange(0, 1000), default=400, show_default=True,
              help='Set the maximum value of the colourbar')
@click.option('--plot_separately', is_flag=True, help='Set this flag to plot all samples separately')
def click_3d_scan(**kwargs):
    from fluorimeter.scan_analysis_3D import interpret_3d_scan

    interpret_3d_scan(**kwargs)


@click.command()
@click.option('--data_file', required=True, help='Data file for analysis.')
def click_kinetics_analysis(**kwargs):
    from fluorimeter.kinetics_analysis import fluorimeter_kinetics_analysis

    fluorimeter_kinetics_analysis(**kwargs)
