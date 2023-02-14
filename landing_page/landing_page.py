import click
from rich.console import Console
from rich import print
from rich.table import Table


@click.command()
def landing_page():
    table = Table(title="Analysis Tools")

    table.add_column("Tool", style="Cyan", no_wrap=True)
    table.add_column("Description", style="green")

    table.add_row(
        "plate_kinetics",
        "Plots kinetics data collected from the ClarioStar plate reader",
    )
    table.add_row(
        "plate_multiplex",
        "Cleans up and plots multiplex kinetics data obtained from a ClarioStar plate reader",
    )
    table.add_row(
        "EDWIN_kinetics", "Plots kinetics data collected from the BMG plate reader"
    )
    table.add_row(
        "fluor_scan",
        "Plots scan data collected from a Cary Eclipse Fluorescence Spectrophotometer",
    )
    table.add_row(
        "fluor_kinetics",
        "Plots kinetic scan data collected from a Cary Eclipse Fluorescence Spectrophotometer",
    )
    table.add_row(
        "fluor_3dscan",
        "Plots 3D scan data collected from a Cary Eclipse Fluorescence Spectrophotometer",
    )
    table.add_row(
        "fluor_multiplex",
        "Plots multiplex kinetics fluorescent data from a Cary Eclipse Fluorescence Spectrophotometer",
    )
    table.add_row("plot_nanodrop", "Plots specrea from a NanoDrop 2000c")
    table.add_row(
        "plot_videocolour", "Plots the RGB values for a specified region of a video"
    )
    table.add_row("split_video", "Split a video into individual frames")

    console = Console()
    console.print(table)
