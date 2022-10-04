# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 20:41:17 2022

@author: s1893121
"""

import click
import os
import cv2
from tqdm import tqdm
import random
from quote import quote


@click.command()
@click.option("--video_file", required=True, help="Video file to be split into frames.")

def video_splitter(video_file): 
    
    base_folder = os.path.dirname(video_file)
    exp_name = video_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]

    capture = cv2.VideoCapture(video_file)

    FramesTotal = 0
    FramesTotal = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f'Total Frames: {FramesTotal}')

    FrameRate = capture.get(cv2.CAP_PROP_FPS)

    print(f'Frame Rate: {FrameRate:.2f}')
 
    frameNr = 1
    pbar = tqdm(total=FramesTotal)
 
    while (True):
        success, frame = capture.read()
        if success:
            cv2.imwrite(os.path.join(base_folder, f'{exp_name}-{frameNr}.jpg'), frame)
        else:
            break
        frameNr = frameNr + 1
        pbar.update(1)
 
    pbar.close()
    capture.release()
    
    words = {"science", "music", "engineering"}
    choice = random.choice(tuple(words))
    res = quote(choice, limit = 100)
    random_number = random.randint(1,100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")