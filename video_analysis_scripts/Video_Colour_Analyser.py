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
import os
from tqdm import tqdm
import click
import ramdom
from quote import quote

def TotalFrames(videofile):
    global FramesTotal
    cap = cv2.VideoCapture(videofile)
    FramesTotal = 0
    FramesTotal = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    print(f"The video has {FramesTotal} frames")
    
    
def ClipFirstFrame(videofile):
    while True:
        global Y1,Y2,X1,X2
        vidcap = cv2.VideoCapture(videofile)
        success, image = vidcap.read()
        if success:
            plt.figure()
            plt.imshow(image)
            plt.draw()
            plt.pause(0.001)     
        Y1 = int(input("Enter Y1 Coordinate: "))
        Y2 = int(input("Enter Y2 Coordinate: "))
        X1 = int(input("Enter X1 Coordinate: "))
        X2 = int(input("Enter X2 Coordinate: "))    
        plt.close()   
        clip = image[Y1:Y2, X1:X2, :]
        plt.figure()
        plt.imshow(clip)
        plt.draw()
        plt.pause(0.001)      
        Selection_Check = input("Are you happy with the selected area? (Y/N): ").capitalize()
        if Selection_Check == "Y":
            plt.close()
            break
        elif Selection_Check == "N":
            plt.close()
            print("Please select again!")
        else:
            plt.close()
            print("Sorry, that is an invalid command!")

        
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
        current_frame = frame[Y1:Y2, X1:X2, :]
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

        
    print("Counting Frames...")
    
    TotalFrames(Video_FILE)
    
    ClipFirstFrame(Video_FILE)
    
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
    
    words = {"science", "music", "engineering"}
    choice = random.choice(tuple(words))
    res = quote(choice, limit = 100)
    random_number = random.randint(1,100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")