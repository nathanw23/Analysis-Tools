import os
import cv2
from tqdm.rich import tqdm
from shared_functions import generate_quote


def video_splitter(video_file):
    base_folder = os.path.dirname(video_file)
    exp_name = video_file.split(os.sep)[-1]
    exp_name = exp_name.rsplit(".", 1)[0]

    capture = cv2.VideoCapture(video_file)

    FramesTotal = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Total Frames: {FramesTotal}")

    FrameRate = capture.get(cv2.CAP_PROP_FPS)

    print(f"Frame Rate: {FrameRate:.2f}")

    frameNr = 1
    pbar = tqdm(total=FramesTotal)

    while True:
        success, frame = capture.read()
        if success:
            cv2.imwrite(os.path.join(base_folder, f"{exp_name}-{frameNr}.jpg"), frame)
        else:
            break
        frameNr = frameNr + 1
        pbar.update(1)

    pbar.close()
    capture.release()
    generate_quote()
