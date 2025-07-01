# 🤖 Gesture Clone Robot

Proyek ini adalah prototipe **Gesture Clone Robot** yang mampu meniru gerakan tangan manusia secara real-time menggunakan *Mediapipe Hand Tracking* (Python) dan **ESP32** yang menggerakkan 5 buah servo motor.

Pengguna cukup menggerakkan tangan di depan kamera, dan tangan robot akan bergerak mengikuti secara langsung.  
Proyek ini dapat menjadi dasar penelitian bidang prostetik, teleoperasi robotik, maupun edukasi mekatronika.

---

## ✨ Fitur

- ✅ Hand tracking real-time menggunakan Mediapipe.
- ✅ Kendali 5 servo motor untuk meniru pergerakan jari (ibu jari, telunjuk, jari tengah, manis, kelingking).
- ✅ Komunikasi Python ↔ ESP32 melalui MQTT.
- ✅ Sistem berbasis open source dan mudah dikembangkan.

---

## 🧰 Teknologi yang Digunakan

- **Python** – Pemrosesan gambar dan deteksi tangan.
- **Mediapipe** – Deteksi landmark jari.
- **ESP32** – Mikrokontroler untuk mengendalikan servo motor.
- **Servo Motor (SG90/MG90)** – Simulasi gerakan jari.
- **MQTT Broker (broker.emqx.io)** – Komunikasi antara Python & ESP32.
- **Arduino IDE / PlatformIO** – Pemrograman ESP32.
- **OpenCV** – Pengambilan & pemrosesan gambar dari webcam.

---

## ⚙️ Arsitektur Sistem

1️⃣ Kamera menangkap pergerakan tangan pengguna.  
2️⃣ Python + Mediapipe memproses status jari (terbuka/tertutup).  
3️⃣ Python mengirim data biner (contoh: `11001`) ke ESP32 via MQTT.  
4️⃣ ESP32 menerima data dan menggerakkan 5 servo motor.  
5️⃣ Tangan robot bergerak mengikuti status jari pengguna.

---

## 🔗 Diagram Blok Hardware / Software

```text
+----------------+       +----------------------+       +-----------------+
|    Webcam      | ----> | Python + Mediapipe   | ----> |      ESP32      |
| (Hand Input)   |       | (Hand Tracking &     |       |  (Servo Control)|
|                |       |   MQTT Publisher)    |       |                 |
+----------------+       +----------------------+       +--------+--------+
                                                            |
                                                            v
                    +-------+-------+-------+-------+-------+
                    | Servo | Servo | Servo | Servo | Servo |
                    |  1    |  2    |  3    |  4    |  5    |
                    |Thumb  |Index  |Middle | Ring  | Pinky |
                    +-------+-------+-------+-------+-------+
---

Penjelasan:

Webcam: Menangkap gerakan tangan secara real-time.

Python + Mediapipe: Deteksi status jari & kirim data ke ESP32.

ESP32: Menggerakkan servo sesuai status jari.

📊 Flowchart Sistem

graph TD
    A[Start] --> B[Capture Hand Video (Webcam)]
    B --> C[Detect Landmarks (Mediapipe)]
    C --> D[Process Finger States (Open/Closed)]
    D --> E[Send Binary Data (MQTT to ESP32)]
    E --> F[Move Servos (ESP32)]
    F --> G{Repeat?}
    G -- Yes --> B
    G -- No --> H[End]

🚀 Cara Menjalankan
1️⃣ Install dependency Python
pip install opencv-python mediapipe paho-mqtt
2️⃣ Upload kode ke ESP32
Buka file gesture_clone_robot.ino di Arduino IDE atau PlatformIO.

Pastikan library WiFi, PubSubClient, dan ESP32Servo sudah terinstall.

Sesuaikan variabel ssid, password, dan mqttServer sesuai jaringan Anda.

Upload kode ke ESP32.
3️⃣ Jalankan program Python
python main.py
4️⃣ Uji coba
Gerakkan tangan di depan webcam → servo akan mengikuti gerakan jari Anda.

🙌 Kontribusi
Pull request, ide pengembangan, dan diskusi sangat diterima!
Silakan buka Issue untuk pertanyaan, saran, atau pelaporan bug.

📦 Flowchart Sistem (Format JSON)
{
  "flowchart": [
    {"id": "start", "label": "Start", "shape": "circle"},
    {"id": "cam", "label": "Capture Hand Video (Webcam)", "shape": "rectangle"},
    {"id": "detect", "label": "Detect Landmarks (Mediapipe)", "shape": "rectangle"},
    {"id": "process", "label": "Process Finger States (Open/Closed)", "shape": "rectangle"},
    {"id": "send", "label": "Send Binary Data (MQTT to ESP32)", "shape": "rectangle"},
    {"id": "move", "label": "Move Servos (ESP32)", "shape": "rectangle"},
    {"id": "loop", "label": "Repeat?", "shape": "diamond"},
    {"id": "end", "label": "End", "shape": "circle"}
  ],
  "connections": [
    {"from": "start", "to": "cam"},
    {"from": "cam", "to": "detect"},
    {"from": "detect", "to": "process"},
    {"from": "process", "to": "send"},
    {"from": "send", "to": "move"},
    {"from": "move", "to": "loop"},
    {"from": "loop", "to": "cam", "label": "Yes"},
    {"from": "loop", "to": "end", "label": "No"}
  ]
}

⚡ Built with Python, Mediapipe & ESP32
⭐ Star this repo if you like it!
