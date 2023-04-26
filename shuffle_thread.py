import numpy as np
import cv2
import time
import os
import numbers

from random_video import RandomVideo


VIDEO_PATH = './clipped/'
DEFAULT_DELAY = 0.5


def shuffle_threading():
    global order_q
    playlist = RandomVideo().cls
    print(playlist)

    for video in playlist:
        if isinstance(video, str):
            order_q.put(video)
            time.sleep(DEFAULT_DELAY)
            path = os.path.join(VIDEO_PATH, video+'.mp4')
            cap = cv2.VideoCapture(path)

            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
        elif isinstance(video, numbers.Complex):
            # print(video)
            time.sleep(video)