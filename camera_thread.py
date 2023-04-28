import os.path
import time
import cv2
import keyboard
from threading import Thread
from queue import Queue

import utils


class CameraThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)

        self.name_id = 1
        utils.make_dir(mode='video', name_id=self.name_id)
        self.path = os.path.join('data', str(self.name_id), 'video', str(self.name_id) + '.mp4')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.path, self.fourcc, 30.0,
                                      (int(self.cap.get(3)), int(self.cap.get(4))))

        self.cam_thread = Thread(target=self.run, daemon=True, name='Cam_Thread')
        self.cam_thread.start()

        keyboard.add_hotkey('space', self.toggle)
        self.is_running = False

    def run(self):
        while True:
            _, frame = self.cap.read()
            cv2.imshow('frame', frame)

            if utils.toggle_var == 'start':
                self.writer.write(frame)

            elif utils.toggle_var == 'stop':
                self.writer.release()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                print('stop camera')
                self.cap.release()
                self.writer.release()
                cv2.destroyWindow('frame')
                break

    # Update the name ID when 'space' is pressed
    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            utils.make_dir(mode='video', name_id=self.name_id)
            self.path = os.path.join('data', str(self.name_id), 'video', str(self.name_id) + '.mp4')
            self.writer = cv2.VideoWriter(self.path, self.fourcc, 30.0,
                                          (int(self.cap.get(3)), int(self.cap.get(4))))
        elif not self.is_running:
            self.name_id += 1


if __name__ == '__main__':
    src = 'test_vid.mp4'
    camera = CameraThread(src)

    while True:
        # running_threads = [t.name for t in threading.enumerate() if t.is_alive()]
        # print(f"Running threads: {running_threads}")
        if keyboard.is_pressed('q'):
            print('break main thread')
            break
        # time.sleep(2)
