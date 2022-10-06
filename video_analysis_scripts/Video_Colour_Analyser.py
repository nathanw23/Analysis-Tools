# -*- coding: utf-8 -*-
"""
Script to plot the colour channels of a selected area in a video. Intended to measure colour changes.

Created on Mon Apr 11 13:36:13 2022

@author: Nathan Wu
"""

import cv2
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os
from tqdm import tqdm
import click
from shared_functions import generate_quote

def TotalFrames(videofile):
    global FramesTotal
    cap = cv2.VideoCapture(videofile)
    FramesTotal = 0
    FramesTotal = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    print(f"The video has {FramesTotal} frames")
    
def onselect_function(eclick, erelease):
    global X1, X2, Y1, Y2
    extent = rect_selector.extents
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])
    X1 = int(extent[0])
    X2 = int(extent[1])
    Y1 = int(extent[2])
    Y2 = int(extent[0])
    return X1, X2, Y1, Y2
        
def process_video(video_filepath, Y1, Y2, X1, X2):
    global FramesTotal,colours,total_length
    colours = []
    cap = cv2.VideoCapture(video_filepath)
    grabbed, frame = cap.read()
    pbar = tqdm(total = FramesTotal, desc="Analysing")
    while grabbed:
        grabbed, frame = cap.read()
        if not grabbed:
            break
        current_frame = frame[X1:X2, Y1:Y2, :]
        avg_color_per_row = np.average(current_frame, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0).tolist()
        colours.append(avg_color)
        pbar.update(1)        
    total_length = len(colours)       
    cap.release()

@click.command()
@click.option("--video_file", required=True, help="Video file for colour analysis.")
def Analyse_Colour(video_file):

    base_folder = os.path.dirname(video_file)
    exp_name = video_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]
    Video_FILE = video_file
    
    TotalFrames(Video_FILE)

    vidcap = cv2.VideoCapture(Video_FILE)
    success, image = vidcap.read()
    if success:
        fig, current_ax = plt.subplots()  
        plt.imshow(image)
        
    while True:
        global rect_selector
        rect_selector = RectangleSelector(current_ax, onselect_function, drawtype='box', button=[1])
        plt.draw()
        plt.pause(0.001)
        input("Press Enter to continue...")
        plt.close()
        break
    
    process_video(Video_FILE, Y1, Y2, X1, X2)
    
    df=pd.DataFrame(colours, columns = ['R', 'G', 'B'])
    df['Frame'] = np.arange(0,total_length)
    df = df[["Frame", "R", "G", "B"]]
    df.to_csv(os.path.join(base_folder, '%s_Channel_Data_(%d,%d_%d,%d).csv' % (exp_name, Y1, Y2, X1, X2)), encoding='utf-8', index=False)
    
    plt.figure()
    sns.lineplot(data=df, x='Frame', y='R', color='red')
    sns.lineplot(data=df, x='Frame', y='G', color='green')
    sns.lineplot(data=df, x='Frame', y='B', color='blue')
    plt.xlim(0,)
    plt.ylim(0,)
    plt.ylabel("Channel Value")
    plt.title('%s_Channel_Values_[%d:%d, %d:%d]' % (exp_name, Y1, Y2, X1, X2), wrap=True)
    plt.savefig(os.path.join(base_folder, '%s_ChannelValues_(%d,%d_%d,%d).png' % (exp_name, Y1, Y2, X1, X2)))
    #plt.show()

    generate_quote()
