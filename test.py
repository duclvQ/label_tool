import threading
import time

import cv2
import keyboard
from threading import Thread
from queue import Queue


# class TestThread:
#     def __init__(self, button: str):
#         self.button = button
#         self.is_recording = False
#         self.counter = 0
#         self.start_time = time.perf_counter()
#
#         keyboard.add_hotkey(button, self.toggle, trigger_on_release=False)
#         self.thread = Thread(target=self.update)
#         self.thread.start()
#
#     def toggle(self):
#         self.is_recording = not self.is_recording
#
#     def update(self):
#         while True:
#             self.counter += 1
#             print(f'{self.counter}\t{time.perf_counter()-self.start_time}')
#             # print(self.counter*1e-6 - (time.perf_counter()-self.start_time))
#
#
# if __name__ == '__main__':
#     testthread = TestThread('space')
#     while True:
#         if keyboard.is_pressed('q'):
#             break


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter('xyz.mp4', fourcc, 20.0, (1, 1))
