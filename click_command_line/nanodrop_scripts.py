import click


@click.command()
@click.option('--data_file', required=True, help='Spectra file from NanoDrop in .TSV format.')
def click_absorbance_plot(**kwargs):
    from nanodrop.nanodrop_analysis import absorbance_plot

    absorbance_plot(**kwargs)
