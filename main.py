import cv2
import serial
import time
from ultralytics import YOLO

# --- KONFIGURASI SERIAL ---
PORT = "COM5"  # Ganti sesuai port Arduino kamu
BAUDRATE = 9600

try:
    arduino = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Tunggu Arduino siap
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

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label in ["bottle", "cup"]:
                    detected = True
                    break  # Langsung keluar jika sudah ada yang terdeteksi

        if detected:
            print("✅ BOTOL / CUP TERDETEKSI! Mengirim perintah ke Arduino...")
            try:
                arduino.write(b"TRIGGER\n")  # Kirim perintah
                time.sleep(1)  # Delay supaya tidak spam perintah
            except serial.SerialException:
                print("❌ Gagal mengirim data ke Arduino.")

except KeyboardInterrupt:
    print("\n🛑 Dihentikan oleh pengguna.")

cap.release()
arduino.close()
print("✅ Kamera dan koneksi Arduino ditutup.")
