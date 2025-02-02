import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

# MediaPipe için gerekli ayarlar
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Video dosyasını aç
video_path = "Bad2.mp4"  # Video dosyasının yolu
cap = cv2.VideoCapture(video_path)

# Koordinatları kaydetmek için
x_coords = [[] for _ in range(5)]  # 5 parmak için X koordinatları
y_coords = [[] for _ in range(5)]  # 5 parmak için Y koordinatları
frame_count = 0  # Kare sayacı

while cap.isOpened() and frame_count < 30:  # 30 kareyi işle
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    # OpenCV'deki BGR formatını RGB formatına çevir
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Her parmak için koordinatları sakla
    current_x = [None] * 5
    current_y = [None] * 5

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Parmak uçlarının koordinatlarını al (MediaPipe landmark ids: 4, 8, 12, 16, 20)
            for i, idx in enumerate([4, 8, 12, 16, 20]):
                current_x[i] = hand_landmarks.landmark[idx].x
                current_y[i] = hand_landmarks.landmark[idx].y

    # Eğer koordinat tespit edilemezse None olarak bırak
    for i in range(5):
        x_coords[i].append(current_x[i])
        y_coords[i].append(current_y[i])

# Video işlemini kapat
cap.release()
hands.close()

# Eksik verileri doldurma (Bir önceki ve bir sonraki karelerin ortalamasını al)
def fill_missing_data(coords):
    coords = np.array(coords, dtype=np.float32)
    for i in range(len(coords)):
        if np.isnan(coords[i]):  # Eğer eksik değer varsa
            prev_val = coords[i - 1] if i > 0 and not np.isnan(coords[i - 1]) else None
            next_val = coords[i + 1] if i < len(coords) - 1 and not np.isnan(coords[i + 1]) else None
            if prev_val is not None and next_val is not None:
                coords[i] = (prev_val + next_val) / 2  # Ortalama al
            elif prev_val is not None:
                coords[i] = prev_val  # Sadece önceki varsa onu al
            elif next_val is not None:
                coords[i] = next_val  # Sadece sonraki varsa onu al
    return coords

# Eksik verileri doldur
x_coords = [fill_missing_data(finger_coords) for finger_coords in x_coords]
y_coords = [fill_missing_data(finger_coords) for finger_coords in y_coords]

# Veri boyutlarını kontrol et ve eşitle
max_length = max(len(coords) for coords in x_coords)
for i in range(5):
    # Her bir parmağın koordinat dizisini max_length'e göre uzat
    x_coords[i] = np.pad(x_coords[i], (0, max_length - len(x_coords[i])), constant_values=np.nan)
    y_coords[i] = np.pad(y_coords[i], (0, max_length - len(y_coords[i])), constant_values=np.nan)

# CSV dosyasına yazma işlemi
csv_filename = "C:\\Python\\PythonProject2\\finger_coordinates3.csv"

# Başlıklar (başlık satırı)
headers = ["Frame", "Thumb_X", "Thumb_Y", "Index_X", "Index_Y", "Middle_X", "Middle_Y", "Ring_X", "Ring_Y", "Pinky_X",
           "Pinky_Y"]

# CSV dosyasını aç ve yazmaya başla
try:
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Başlık satırını yaz
        writer.writerow(headers)

        # Verileri yaz
        for frame in range(max_length):
            row = [frame + 1]  # Kare numarasını ekle
            for i in range(5):
                row.append(x_coords[i][frame])  # X koordinatları
                row.append(y_coords[i][frame])  # Y koordinatları
            writer.writerow(row)

    print(f"Veriler {csv_filename} dosyasına kaydedildi.")
except Exception as e:
    print(f"CSV dosyasına yazılırken bir hata oluştu: {e}")

# Grafik çizimi
frames = list(range(1, max_length + 1))  # 1'den max_length'e kadar kareler

# Her parmak için ayrı grafik çiz
for i, finger_name in enumerate(["Thumb", "Index", "Middle", "Ring", "Pinky"]):
    plt.figure()
    plt.plot(frames, x_coords[i], label=f"{finger_name} X")  # Etiket ekle
    plt.plot(frames, y_coords[i], linestyle="dashed", label=f"{finger_name} Y")  # Etiket ekle
    plt.title(f"{finger_name} Coordinates Over Frames")
    plt.xlabel("Frame")
    plt.ylabel("Coordinate")
    plt.legend()  # Etiketleri göstermek için
    plt.show()
