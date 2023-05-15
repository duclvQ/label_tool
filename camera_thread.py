import os.path
import time
import cv2
import keyboard
from threading import Thread
from queue import Queue
import pickle
import utils
import mediapipe as mp
import time
mp_hands = mp.solutions.hands 



class CameraThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.name_id = 1
        utils.make_dir(mode='video', name_id=self.name_id)
        self.path = os.path.join('data', str(self.name_id), 'video', str(self.name_id) + '.mp4')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                      (int(self.cap.get(3)), int(self.cap.get(4))))

        self.cam_thread = Thread(target=self.run, daemon=True, name='Cam_Thread')
        self.cam_thread.start()
        self.pose_list = list()
        keyboard.add_hotkey('space', self.toggle)
        self.is_running = False

    def run(self):

        start_time = time.time()
        frame_count = 0
        while True:
            _, frame = self.cap.read()
            annotated_frame = frame.copy()
            window_name = 'Image'
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            annotated_frame = cv2.putText(annotated_frame, str(utils.frame), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)

            annotated_frame = cv2.putText(annotated_frame, str(frame_count), (50, 30), font,
                                fontScale, color, thickness, cv2.LINE_AA)

            
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time
            frame_count+=1

            # Hiển thị FPS trên khung hình
            cv2.putText(annotated_frame, f"FPS: {round(fps, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', annotated_frame)

            if utils.toggle_var == 'start':
                utils.frame += 1
                self.writer.write(frame)
                #self.pose_list.append(self.estimate(frame))

            elif utils.toggle_var == 'stop':
                utils.frame = 0
                self.writer.release()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                print('stop camera')
                self.cap.release()
                self.writer.release()
                cv2.destroyWindow('frame')
                with open('parrot.pkl', 'wb') as f:
                    pickle.dump(self.pose_list, f)
                break

    # Update the name ID when 'space' is pressed
    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            utils.make_dir(mode='video', name_id=self.name_id)
            self.path = os.path.join('data', str(self.name_id), 'video', str(self.name_id) + '.mp4')
            self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                          (int(self.cap.get(3)), int(self.cap.get(4))))
        elif not self.is_running:
            self.name_id += 1
 
    def estimate(self, image):
        
        with mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.3) as hands:
                    # Read an image, flip it around y-axis for correct handedness output (see
                    # above).
            pose = []
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Draw hand world landmarks.
            if not results.multi_hand_world_landmarks:
                return pose
            start = time.time()
            for hand_world_landmarks in results.multi_hand_world_landmarks:
                for hand in hand_world_landmarks.landmark:
                    joint_coor = [hand.x, hand.y,hand.z]
                    pose.append(joint_coor)
            print(time.time() - start)
            return pose
