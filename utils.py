import os
import time
from queue import Queue
import keyboard

MAXSIZE = 19
start_time = time.perf_counter()

order_q = Queue(maxsize=MAXSIZE)
start_q = Queue(maxsize=MAXSIZE)
stop_q = Queue(maxsize=MAXSIZE)
#toggle_q = Queue(maxsize=1)

toggle_var = None

frame = 0


class ButtonManager:
    def __init__(self):
        self.keys = []
        self.pre_space = False
        self.bind_key()

    def on_press_a(self):
        if not start_q.full():
            press_time = time.perf_counter() - start_time
            press_time = round(press_time, 2)
            start_q.put(frame)
        

    def on_press_b(self):
        if not stop_q.full():
            press_time = time.perf_counter() - start_time
            press_time = round(press_time, 2)
            # stop_q.put(press_time)
            # print(press_time)
            stop_q.put(frame)
       

    def on_press_space(self):
        global toggle_var, toggle_q, start_time
        self.pre_space = not self.pre_space
        print('space')
        if self.pre_space:
            toggle_var = 'start'
            #toggle_q.put('start')

            # Restart timer
            start_time = time.perf_counter()

        elif not self.pre_space:
            print(frame)
            toggle_var = 'stop'
            #toggle_q.put('stop')

        print('-'*20)

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)
        keyboard.add_hotkey('space', self.on_press_space)


def make_dir(mode, name_id):
    _dir = os.path.join('data', str(name_id), mode)
    if not os.path.exists(_dir):
        os.makedirs(_dir)

