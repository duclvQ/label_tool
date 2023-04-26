import threading
import time
from queue import Queue

import keyboard

from labelling_thread import labelling_thread


start_time = time.perf_counter()

order_q = Queue(maxsize=19)
start_q = Queue(maxsize=19)
stop_q = Queue(maxsize=19)


class Timer:
    global start_time

    def __init__(self):
        self.bind_key()

    def on_press_a(self):
        global start_q
        press_time = time.perf_counter() - start_time
        start_q.put(press_time)

    def on_press_b(self):
        global stop_q
        press_time = time.perf_counter() - start_time
        stop_q.put(press_time)

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)


if __name__ == '__main__':
    Timer()
    while True:
        print(start_q.get())