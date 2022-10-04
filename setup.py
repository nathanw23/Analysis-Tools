""" Setup script for Analysis_Tools. """

from setuptools import setup, find_packages

setup(
    name="Analysis-Tools",
    author="Nathan Wu, Matthew Aquilina",
    version='0.1.0',
    description="A suite of software tools developed during my PhD",
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        plot_scan = fluorimeter_scripts.Fluorimeter_Scan_Analysis:fluorimeter_scan_analysis
        plot_3dscan = fluorimeter_scripts.Fluorimeter_3DScan_Analysis:interpret_3d_scan
        plot_kinetics = fluorimeter_scripts.Fluorimeter_Kinetics_Analysis:fluorimeter_kinetics_analysis
        plot_platekinetics = platereader_scripts.PlateReader_Kinetics:interpret_plate_kinetics
        plot_videocolour = video_analysis_scripts.Video_Colour_Analyser:Analyse_Colour
        analysis_tools = landing_page.landing_page:landing_page
        plot_nanodrop = nanodrop_scripts.NanoDrop_Analysis:Plot_NanoDrop
        split_video = video_analysis_scripts.split_video:video_splitter
    '''
)

