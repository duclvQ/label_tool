import os.path
import cv2
import keyboard
from threading import Thread
import utils
import time


class CameraThread:
    def __init__(self, name, src=0):

        self.cap = cv2.VideoCapture(src)
        print('================== READY ==================')
        self.name_id = name

        utils.make_dir(name=self.name_id)
        self.path = os.path.join('data', self.name_id, f'{self.name_id}_{str(utils.name_id)}' + '.mp4')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                      (int(self.cap.get(3)), int(self.cap.get(4)) - 40))

        self.cam_thread = Thread(target=self.run, daemon=True, name='Cam_Thread')
        self.cam_thread.start()
        keyboard.add_hotkey('space', self.toggle)
        self.is_running = False

    def run(self):

        start_time = time.time()
        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print('[ERROR] Missing frames ...')
                continue
            annotated_frame = frame.copy()

            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            annotated_frame = cv2.putText(annotated_frame, str(utils.frame), (250, 70), font,
                                          fontScale, color, thickness, cv2.LINE_AA)

            height, width, _ = frame[40:, :].shape
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time
            frame_count += 1

            # Hiển thị FPS trên khung hình
            cv2.putText(annotated_frame, f"FPS: {round(fps, 2)}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', annotated_frame)

            if utils.toggle_var == 'start':
                utils.frame += 1
                self.writer.write(frame[40:, :])

            elif utils.toggle_var == 'stop':
                utils.frame = 0
                self.writer.release()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                print('stop camera')
                self.cap.release()
                self.writer.release()
                cv2.destroyWindow('frame')
                break

    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            utils.make_dir(name=self.name_id)
            self.path = os.path.join('data', self.name_id, f'{self.name_id}_{utils.name_id}' + '.mp4')
            self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                          (int(self.cap.get(3)), int(self.cap.get(4)) - 40))
