import time
from queue import Queue
import keyboard

start_time = time.perf_counter()

order_q = Queue(maxsize=19)
start_q = Queue(maxsize=19)
stop_q = Queue(maxsize=19)

toggle_var = None


class ButtonManager:
    def __init__(self):
        self.keys = []
        self.pre_space = False
        self.bind_key()

    def on_press_a(self):
        press_time = time.perf_counter() - start_time
        press_time = round(press_time, 2)
        start_q.put(press_time)
        print(press_time)

    def on_press_b(self):
        press_time = time.perf_counter() - start_time
        press_time = round(press_time, 2)
        stop_q.put(press_time)
        print(press_time)

    def on_press_space(self):
        global toggle_var

        self.pre_space = not self.pre_space
        if self.pre_space:
            toggle_var = 'start'
        elif not self.pre_space:
            toggle_var = 'stop'

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)
        keyboard.add_hotkey('space', self.on_press_space)

