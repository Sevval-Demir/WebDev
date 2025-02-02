import cv2

# Video dosyasının yolu
video_path = 'Bad2.mp4'

# Video dosyasını aç
cap = cv2.VideoCapture(video_path)

# Video başarıyla açıldıysa
if cap.isOpened():
    # Video özelliklerini al (frame sayısı)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Toplam Frame Sayısı: {total_frames}")
else:
    print("Videoyu açmada bir hata oluştu.")

# Video dosyasını kapat
cap.release()
