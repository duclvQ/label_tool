import cv2

video_path = ['data/100/100.mp4']
annotation_path = ['data/100/1.txt']

    # Đọc video

for video, annot in zip(video_path, annotation_path):
    # Đọc file annotation
    capture = cv2.VideoCapture(video)
    with open(annot, 'r') as file:
        annot = file.readlines()
        #start_frame, end_frame, label = annot.strip().split('\t')
    print(annot)
    s = list()
    for a in annot:
        s.append(a.strip().split('\t'))
    # Vòng lặp xử lý các khung hình
    frame_count = 0
    l = None
    while True:
            # Đọc một khung hình từ video
            ret, frame = capture.read()
            
            # Kiểm tra nếu không đọc được khung hình nữa
            if not ret:
                break

            for x in s:
                start, stop, label = x  
                if int(start)<frame_count and frame_count<int(stop):
                     l = label
                     break
                else: l = None
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (250, 50)
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            
            # Hiển thị nhãn của annotation và số khung hình
            cv2.putText(frame, str(l), (250, 70), font,
                                fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            
            # Tăng biến đếm số khung hình
            frame_count += 1

            cv2.waitKey(10)

    # Giải phóng video capture
    capture.release()
