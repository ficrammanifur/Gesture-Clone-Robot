# 🤖 Gesture Clone Robot

Proyek ini adalah prototipe **Gesture Clone Robot** yang mampu meniru gerakan tangan manusia secara real-time menggunakan **Mediapipe Hand Tracking** (Python) dan **ESP32** yang menggerakkan 5 buah servo motor.

Dengan sistem ini, pengguna cukup menggerakkan tangan di depan kamera, dan tangan robot akan bergerak mengikuti secara langsung. Proyek ini dapat digunakan sebagai dasar penelitian bidang prostetik, teleoperasi robotik, maupun edukasi mekatronika.

---

## ✨ **Fitur**
- Hand tracking real-time menggunakan **Mediapipe**
- Kendali 5 servo motor untuk meniru pergerakan jari
- Komunikasi Python ↔ ESP32 (WebSocket atau MQTT)
- Sistem berbasis open source dan dapat dikembangkan lebih lanjut

---

## 🧰 **Teknologi yang Digunakan**
- Python
- Mediapipe
- ESP32
- Servo Motor (SG90 / MG90)
- MQTT broker (misalnya broker.emqx.io) atau WebSocket
- Arduino IDE / PlatformIO (untuk programming ESP32)

---

## ⚙️ **Arsitektur Sistem**
1. Kamera menangkap pergerakan tangan
2. Python + Mediapipe memproses data sudut jari
3. Python mengirim data sudut ke ESP32
4. ESP32 mengendalikan 5 servo motor
5. Tangan robot bergerak sesuai tangan pengguna
