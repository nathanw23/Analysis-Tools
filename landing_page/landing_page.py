import pyfiglet
from terminaltables import AsciiTable
import click


@click.command()
def landing_page():
    Welcome = pyfiglet.figlet_format("Analysis Tools")
    print(Welcome)

    print("A collection of tools to help with data analysis and visualisation.")

    table_data = [
        ['Tool', 'Description'],
        ['plate_kinetics', 'Plots kinetics data collected from the ClarioStar plate reader'],
        ['plate_multiplex', 'Cleans up and plots multiplex data obtained from a ClarioStar plate reader'],
        ['EDWIN_kinetics', 'Plots kinetics data collected from the BMG plate reader'],
        ['fluor_scan', 'Plots scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['fluor_kinetics', 'Plots kinetic scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['fluor_3dscan', 'Plots 3D scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['fluor_multiplex', 'Plots multiplex fluorescent data from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['plot_nanodrop', 'Plots specrea from a NanoDrop 2000c'],
        ['plot_videocolour', 'Plots the RGB values for a specified region of a video'],
        ['split_video', 'Split a video into individual frames'],
    ]

    table = AsciiTable(table_data)
    print(table.table)
