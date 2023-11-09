import click
import os
from shared_functions import generate_quote


@click.command()
@click.option(
    "--data_file", required=True, help="Spectra file from NanoDrop in .TSV format."
)
@click.option(
    "--format_data",
    is_flag=True,
    default=None,
    help="Set this flag to generate and save formatted data.",
)
def click_absorbance_plot(**kwargs):
    from nanodrop.nanodrop_analysis import cli_absorbance_plot, absorbance_setup

    base_folder = os.path.dirname(
        kwargs["data_file"]
    )  # Sets the base folder to the directory of the inputed data file
    exp_name = kwargs["data_file"].split(os.sep)[-1].rsplit(".", 1)[0]

    df = absorbance_setup(**kwargs)
    cli_absorbance_plot(df, base_folder, exp_name)

    if kwargs["format_data"]:
        df.to_csv(
            os.path.join(base_folder, f"{exp_name}.csv"), encoding="utf-8"
        )  # Saves the tsv file as a csv file for future analysis
    
    generate_quote()
