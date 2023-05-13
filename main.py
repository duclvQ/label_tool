import os.path
import threading
import time
import queue
from copy import deepcopy

import keyboard

from shuffle_thread import ShuffleThread
from camera_thread import CameraThread
import utils


def create_annot(path):
    start_ls = []
    stop_ls = []
    order_ls = []

    for i in range(utils.order_q.maxsize):
        print(i)
        try:
            start_ls.append(utils.start_q.queue.popleft())
            stop_ls.append(utils.stop_q.queue.popleft())
            order_ls.append(utils.order_q.queue.popleft())
        except IndexError:
            pass

    with open(path, 'w') as f:
        for start, stop, cls in zip(start_ls, stop_ls, order_ls):
            print(f'{start}\t{stop}\t{cls}')
            f.writelines(f'{start}\t{stop}\t{cls}\n')


if __name__ == '__main__':
    # Đổi "src" thành ID của camera (tương tự cv2.VideoCapture(src))
    src = "rtsp://admin:comvis123@192.168.100.125:554/Streaming/Channels/101/"
    # src = "test_vid.mp4"
    # src = 0
    name_id = 1
    # utils.make_dir(mode='annot', name_id=name_id)
    # path = os.path.join('data', str(name_id), 'annot', str(name_id)+'.txt')

    # Run threads
    utils.ButtonManager()
    ShuffleThread()
    CameraThread(src)

    keyboard.wait('space')

    while True:
        time.sleep(.01)
        try:
            if (len(utils.start_q.queue) == utils.order_q.maxsize and
                len(utils.stop_q.queue) == utils.order_q.maxsize) or \
                    utils.toggle_q.get_nowait() == 'stop':
                print('--- Name ID:', name_id)
                utils.make_dir(mode='annot', name_id=name_id)
                path = os.path.join('data', str(name_id), 'annot', str(name_id)+'.txt')
                create_annot(path)
                name_id += 1

                utils.start_q.queue.clear()
                utils.stop_q.queue.clear()
                utils.order_q.queue.clear()
        except queue.Empty:
            pass

        if keyboard.is_pressed('q'):
            print('[EXIT MAIN]')
            break
