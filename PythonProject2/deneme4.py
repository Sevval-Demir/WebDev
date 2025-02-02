
import cv2
import mediapipe as mp
import numpy as np
import sys
import os

# Video dosyası yolu
video_path = "C:\Python\PythonProject2\Bad1.mp4"

# Dosya mevcut mu?
if not os.path.exists(video_path):
    print(f"Error: The video file does not exist at {video_path}")
    sys.exit()

# OpenCV ile video yükleme
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Video file cannot be opened. Check the path!")
    sys.exit()

# MediaPipe el takip modeli
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Çizim için boş bir tuval oluştur
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
canvas = np.zeros((height, width, 3), dtype="uint8")

trajectory_points = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü RGB'ye dönüştür
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # El takibini çalıştır
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # İşaret parmağı uç koordinatları (Landmark 8)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * frame.shape[1])
            y = int(index_finger_tip.y * frame.shape[0])

            # Koordinatları kaydet
            trajectory_points.append((x, y))

            # Çizim
            cv2.circle(canvas, (x, y), 5, (255, 255, 255), -1)

# Video akışını serbest bırak
cap.release()

# Canvas'ı kaydet
output_path = "signature_canvas.png"
cv2.imwrite(output_path, canvas)
print(f"Canvas saved as {output_path}")
