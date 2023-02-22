""" Setup script for Analysis_Tools. """

from setuptools import setup, find_packages

setup(
    name="Analysis-Tools",
    author="Nathan Wu, Matthew Aquilina",
    version="0.1.0",
    description="A suite of software tools developed during my PhD",
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        analysis_tools = landing_page.landing_page:landing_page
        fluor_scan = click_command_line.fluorimeter_scripts:click_fluorimeter_scan
        fluor_3dscan = click_command_line.fluorimeter_scripts:click_3d_scan
        fluor_kinetics = click_command_line.fluorimeter_scripts:click_kinetics_analysis
        plate_kinetics = click_command_line.platereader_scripts:click_interpret_kinetics
        plate_multiplex = click_command_line.platereader_scripts:click_multiplex_cleanup
        plot_nanodrop = click_command_line.nanodrop_scripts:click_absorbance_plot
        plot_videocolour = click_command_line.video_analysis_scripts:click_video_colour_analysis
        split_video = click_command_line.video_analysis_scripts:click_video_splitter
        fluor_multiplex = click_command_line.fluorimeter_scripts:click_multiplex_fluorimeter
        BMG_kinetics = click_command_line.platereader_scripts:click_EDWIN_kinetics
    """,
)
