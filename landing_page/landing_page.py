#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:38:49 2022

@author: nathanwu
"""

import  pyfiglet 
from terminaltables import AsciiTable
import click

@click.command()

def landing_page():
    
    Welcome = pyfiglet.figlet_format("Analysis Tools")
    print(Welcome)
    
    print("A collection of tools to help with data analysis and visualisation.")
    
    table_data = [
        ['Tool', 'Description'],
        ['plot_platekinetics', 'Plots kinetics data collected from the ClarioStar plate reader'],
        ['plot_scan', 'Plots scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['plot_kinetics', 'Plots kinetic scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['plot_3dscan', 'Plots 3D scan data collected from a Cary Eclipse Fluorescence Spectrophotometer'],
        ['plot_videocolour', 'Plots the RGB values for a specified region of a video'],
        ['plot_nanodrop', 'Plots specrea from a NanoDrop 2000c'],
        ['split_video', 'Split a video into individual frames']
    ]
    
    table = AsciiTable(table_data)
    print(table.table)
