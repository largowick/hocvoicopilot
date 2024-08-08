import os
import cv2
import numpy as np

def detect_faces(image_path):
    # Kiểm tra xem tệp cascade có tồn tại không
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_path):
        raise FileNotFoundError(f"Cascade file not found: {cascade_path}")

    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Kiểm tra xem tệp ảnh có tồn tại không
    image_path = 'media/posts/images/a_Tuân.jpg'

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = cv2.imread(image_path)

    # Kiểm tra xem ảnh có được đọc thành công không
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Kiểm tra xem ảnh có được chuyển đổi sang thang độ xám thành công không
    if gray is None:
        raise ValueError("Failed to convert image to grayscale")

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Kiểm tra xem hàm detectMultiScale có trả về danh sách các gương mặt không
    if len(faces) == 0:
        print("No faces detected")
    else:
        print(f"Detected {len(faces)} face(s)")

    face_list = []
    for (x, y, w, h) in faces:
        face_list.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})
        # Vẽ hình chữ nhật quanh gương mặt
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Hiển thị ảnh với các gương mặt được phát hiện
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return face_list