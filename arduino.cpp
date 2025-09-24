#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 5;  // Ganti jika servo dipasang di pin lain

void setup() {
  Serial.begin(9600);
  myServo.attach(SERVO_PIN);
  myServo.write(0);  // Posisi awal servo
  Serial.println("✅ Arduino siap menerima perintah...");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Baca sampai newline
    command.trim();  // Hapus spasi / newline tambahan

    if (command == "TRIGGER") {
      Serial.println("🔓 Perintah diterima: TRIGGER → Buka Servo!");
      
      myServo.write(90);   // Buka servo (ubah sesuai kebutuhan)
      delay(1000);         // Tahan 1 detik
      myServo.write(0);    // Tutup servo kembali
    }
  }
}
