import os.path

import cv2

VIDEO_PATH = './clipped/'
with open('./Classes.txt', 'r') as f:
    cls = f.read().split()
    print(cls)
for video in cls:
    print(video)
    path = os.path.join(VIDEO_PATH, video+'.mp4')
    # print(path)
    cap = cv2.VideoCapture(path)

    while cap.isOpened():
        # print('hello')
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            cap.release()
            cv2.destroyAllWindows()
