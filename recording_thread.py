import threading
import time
from threading import Thread

import cv2
from queue import Queue

import keyboard


class CameraThread:
    def __init__(self, src=0):
        self.name_id = 1
        self.cap = cv2.VideoCapture(src)

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(f'{self.name_id}.mp4', self.fourcc, 20.0, (int(self.cap.get(3)),int(self.cap.get(4))))

        self.is_recording = False
        keyboard.add_hotkey('space', self.toggle)

        self.cam_thread = Thread(target=self.run, daemon=True, name='Cam_Thread')
        self.record_thread = Thread(target=self.record, daemon=True, name='Record_Thread')

        self.cam_thread.start()
        self.record_thread.start()

    def toggle(self):
        print(self.name_id)
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.writer = cv2.VideoWriter(f'{self.name_id}.mp4', self.fourcc, 20.0, (int(self.cap.get(3)),int(self.cap.get(4))))
        elif not self.is_recording:
            self.name_id += 1

    def run(self):
        while True:
            _, self.frame = self.cap.read()
            cv2.imshow('frame', self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('stop')
                self.cap.release()
                cv2.destroyAllWindows()
                # exit(1)
                break

    def record(self):
        while True:
            if self.is_recording:
                # print(self.name_id)
                self.writer.write(self.frame)
            elif not self.is_recording:
                self.writer.release()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.writer.release()
                break
                # exit(1)


if __name__ == '__main__':
    src = './[A4VF][K-ON!][SS2][15][DVD].mp4'
    camera = CameraThread(src)

    while True:
        # running_threads = [t.name for t in threading.enumerate() if t.is_alive()]
        # print(f"Running threads: {running_threads}")q
        if keyboard.is_pressed('q'):
            print('break main thread')
            break
        # time.sleep(2)