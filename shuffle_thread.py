import threading
from threading import Thread

import keyboard
import cv2
import time
import os
import numbers

from random_video import RandomVideo
import utils


VIDEO_PATH = './clipped/'
DEFAULT_DELAY = 0.5


def shuffle_clips():
    playlist = RandomVideo().cls
    print(playlist)

    for video in playlist:
        print(video)
        if isinstance(video, str):
            # utils.order_q.put(video)
            time.sleep(DEFAULT_DELAY)
            path = os.path.join(VIDEO_PATH, video+'.mp4')
            cap = cv2.VideoCapture(path)

            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Clip', frame)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
                else:
                    cap.release()
                    cv2.destroyWindow('Clip')
                    break
        elif isinstance(video, numbers.Complex):
            # print(video)
            time.sleep(video)


class ShuffleThread:
    def __init__(self):
        self.thread = Thread(target=self.shuffle, daemon=False, name='Shuffle Thread')
        self.thread.start()

    def shuffle(self):
        # if utils.toggle_var is not None:
        #     print(utils.toggle_var)
        while True:
            if utils.toggle_var == 'start' \
                    or __name__ == '__main__':
                shuffle_clips()


if __name__ == '__main__':
    ShuffleThread()
    while True:
        # running_threads = [t.name for t in threading.enumerate() if t.is_alive()]
        # print(f"Running threads: {running_threads}")
        time.sleep(1)
        if keyboard.is_pressed('q'):
            break
