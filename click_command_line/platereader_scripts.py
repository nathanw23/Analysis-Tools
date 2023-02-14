import click
import os
from shared_functions import generate_quote


@click.command()
@click.option(
    "--data_file",
    required=True,
    help="Data file for analysis. Different conditions must be different groups in the plate layout",
)
@click.option(
    "--format_data",
    is_flag=True,
    default=None,
    help="Set this flag to generate and save formatted data.",
)
def click_multiplex_cleanup(**kwargs):
    from platereader.multiplexing import cleanup_multiplex_data, cli_multiplex_plot

    base_output_folder = os.path.dirname(kwargs["data_file"])
    exp_name = kwargs["data_file"].split(os.sep)[-1].rsplit(".", 1)[0]

    df = cleanup_multiplex_data(**kwargs)

    if kwargs["format_data"]:
        df.to_csv(
            os.path.join(base_output_folder, f"{exp_name}_Formatted_Data.csv"),
            encoding="utf-8",
            index=False,
        )

    cli_multiplex_plot(df, base_output_folder, exp_name)

    generate_quote()


@click.command()
@click.option(
    "--data_file",
    required=True,
    help="Data file for analysis. Different conditions must be different groups in the plate layout.",
)
@click.option(
    "--labels",
    default=None,
    help="Labels for the figure legend separated by commas (no spaces)",
)
@click.option(
    "--format_data",
    is_flag=True,
    default=None,
    help="Set this flag to generate and save formatted data.",
)
def click_interpret_kinetics(**kwargs):
    from platereader.kinetics import interpret_plate_kinetics, cli_lineplot

    if kwargs["labels"] is not None:
        kwargs["labels"] = kwargs["labels"].split(",")

    base_output_folder = os.path.dirname(kwargs["data_file"])
    exp_name = kwargs["data_file"].split(os.sep)[-1].rsplit(".", 1)[0]

    df = interpret_plate_kinetics(**kwargs)

    if kwargs["format_data"]:
        df.to_csv(
            os.path.join(base_output_folder, "%s_Formatted_Data.csv" % exp_name),
            encoding="utf-8",
            index=False,
        )  # Exports the formatted datafram as a CSV file

        summary = df.groupby(["Group", "Converted_Time"])[
            "Signal"
        ].describe()  # Produces data summary for group/timepoint
        summary.to_csv(
            os.path.join(base_output_folder, "%s_Data_Summary.csv" % exp_name),
            encoding="utf-8",
        )  # Exports a data summary to a csv file

    if kwargs["labels"] is None:
        kwargs["labels"] = df["Group"].unique().tolist()

    cli_lineplot(df, base_output_folder, exp_name, kwargs["labels"])

    generate_quote()


@click.command()
@click.option(
    "--data_file",
    required=True,
    help="Data file for analysis. Different conditions must be different groups in the plate layout",
)
@click.option(
    "--format_data",
    is_flag=True,
    default=None,
    help="Set this flag to generate and save formatted data",
)
def click_EDWIN_kinetics(**kwargs):
    from platereader.EDWIN_kinetics import (
        EDWIN_kinetics_analysis,
        cli_EDIWN_kinetics_plot,
    )

    base_output_folder = os.path.dirname(kwargs["data_file"])
    exp_name = kwargs["data_file"].split(os.sep)[-1].rsplit(".", 1)[0]

    df = EDWIN_kinetics_analysis(**kwargs)

    if kwargs["format_data"]:
        df.to_csv(
            os.path.join(base_output_folder, f"{exp_name}_Formatted_Data.csv"),
            encoding="utf-8",
            index=False,
        )

    cli_EDIWN_kinetics_plot(df, base_output_folder, exp_name)

    generate_quote()
