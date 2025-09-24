import cv2
import serial
import time
import numpy as np
from ultralytics import YOLO

# --- KONFIGURASI SERIAL ---
PORT = "COM5"
BAUDRATE = 9600

try:
    arduino = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print(f"✅ Terhubung ke Arduino di {PORT}")
except serial.SerialException:
    print(f"❌ Gagal terhubung ke Arduino di {PORT}")
    exit()

# --- LOAD YOLO ---
model = YOLO("yolov8n.pt")
print("✅ Model YOLO berhasil dimuat.")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Tidak bisa membuka kamera.")
    exit()

print("🚀 Mulai deteksi... Tekan CTRL + C untuk berhenti.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, imgsz=384, conf=0.3)
        detected = False
        brightness = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label in ["bottle", "cup"]:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    detected = True

                    # --- CEK WARNA BOTOL ---
                    roi = frame[y1:y2, x1:x2]
                    avg_color = roi.mean(axis=(0, 1))  # BGR
                    avg_b, avg_g, avg_r = avg_color
                    brightness = (avg_r + avg_g + avg_b) / 3  # Rata-rata

                    print(f"🎨 Rata-rata BGR: ({avg_b:.1f}, {avg_g:.1f}, {avg_r:.1f}) | Kecerahan: {brightness:.1f}")
                    break

        if detected:
            if brightness > 80:  # Threshold, 0=gelap, 255=terang
                print("⚪ Botol terlalu terang → Servo TIDAK dibuka.")
            else:
                print("✅ Botol/cup gelap → Mengirim perintah ke Arduino...")
                try:
                    arduino.write(b"TRIGGER\n")
                    time.sleep(1)
                except serial.SerialException:
                    print("❌ Gagal mengirim data ke Arduino.")

except KeyboardInterrupt:
    print("\n🛑 Dihentikan oleh pengguna.")

cap.release()
arduino.close()
print("✅ Kamera dan koneksi Arduino ditutup.")
