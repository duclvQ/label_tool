import threading
import time
from queue import Queue
import keyboard

from shuffle_thread import ShuffleThread
from recording_thread import CameraThread
import utils

if __name__ == '__main__':
    utils.ButtonManager()
    ShuffleThread()

    # Đổi "src" thành id của camera (tương tự cv2.VideoCapture(src))
    src = './[A4VF][K-ON!][SS2][15][DVD].mp4'
    CameraThread(src)

    while True:
        time.sleep(.01)
        if keyboard.is_pressed('q'):
            print('break main')
            break

    # Create annotation file
    while not (utils.start_q.empty() or
               utils.start_q.empty() or
               utils.order_q.empty()):
        start, stop, cls = utils.start_q.get(), utils.stop_q.get(), utils.order_q.get()
        print(f'{start:.2f}\t{stop:.2f}\t{cls}')
    else:
        print('Empty queue: '
              + 'Start ' * utils.start_q.empty()
              + 'Stop ' * utils.stop_q.empty()
              + 'Order' * utils.order_q.empty()
              )
