import cv2
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm.rich import tqdm
from shared_functions import generate_quote


def TotalFrames(videofile):
    global FramesTotal
    cap = cv2.VideoCapture(videofile)
    FramesTotal = 0
    FramesTotal = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    print(f"The video has {FramesTotal} frames")


def process_video(video_filepath, Y1, Y2, X1, X2):
    global FramesTotal, colours, total_length
    colours = []
    cap = cv2.VideoCapture(video_filepath)
    grabbed, frame = cap.read()
    pbar = tqdm(total=FramesTotal, desc="Analysing")
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


def colour_analysis(video_file):
    base_folder = os.path.dirname(video_file)
    exp_name = video_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit('.', 1)[0]
    Video_FILE = video_file

    print("Counting Frames...")

    TotalFrames(Video_FILE)

    vidcap = cv2.VideoCapture(Video_FILE)
    success, image = vidcap.read()
    r = cv2.selectROI("Select the area", image)
    Y1 = int(r[1])
    Y2 = int(r[1] + r[3])
    X1 = int(r[0])
    X2 = int(r[0] + r[2])
    cv2.destroyAllWindows()

    process_video(Video_FILE, Y1, Y2, X1, X2)

    df = pd.DataFrame(colours, columns=['Red', 'Green', 'Blue'])
    df['Frame'] = np.arange(0, total_length)
    df = df[["Frame", "Red", "Green", "Blue"]]

    df = pd.melt(df, id_vars=['Frame'], var_name='Channel', value_name='Signal')

    df.to_csv(os.path.join(base_folder, '%s_Channel_Data_(%d,%d_%d,%d).csv' % (exp_name, Y1, Y2, X1, X2)), encoding='utf-8', index=False)

    grid = sns.FacetGrid(df, row='Channel', margin_titles=True)
    grid.map(sns.lineplot, "Frame", "Signal", ci="sd", palette="colorblind")
    plt.savefig(os.path.join(base_folder, '%s_ChannelValues_(%d,%d_%d,%d).png' % (exp_name, Y1, Y2, X1, X2)))

    generate_quote()
