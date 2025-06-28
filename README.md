🤖 Gesture Clone Robot
Proyek ini adalah prototipe Gesture Clone Robot yang mampu meniru gerakan tangan manusia secara real-time menggunakan Mediapipe Hand Tracking (Python) dan ESP32 yang menggerakkan 5 buah servo motor.
Dengan sistem ini, pengguna cukup menggerakkan tangan di depan kamera, dan tangan robot akan bergerak mengikuti secara langsung. Proyek ini dapat digunakan sebagai dasar penelitian bidang prostetik, teleoperasi robotik, maupun edukasi mekatronika.

✨ Fitur

Hand tracking real-time menggunakan Mediapipe.
Kendali 5 servo motor untuk meniru pergerakan jari (ibu jari, telunjuk, jari tengah, manis, kelingking).
Komunikasi Python ↔ ESP32 melalui MQTT.
Sistem berbasis open source dan dapat dikembangkan lebih lanjut.


🧰 Teknologi yang Digunakan

Python: Untuk pemrosesan gambar dan deteksi tangan.
Mediapipe: Untuk hand tracking dan deteksi landmark jari.
ESP32: Mikrokontroler untuk mengendalikan servo motor.
Servo Motor (SG90/MG90): Untuk simulasi gerakan jari.
MQTT Broker (broker.emqx.io): Untuk komunikasi antara Python dan ESP32.
Arduino IDE/PlatformIO: Untuk pemrograman ESP32.
OpenCV: Untuk pengambilan dan pemrosesan gambar dari webcam.


⚙️ Arsitektur Sistem

Kamera menangkap pergerakan tangan.
Python + Mediapipe memproses data status jari (terbuka/tertutup).
Python mengirim data biner (misal: "11001") ke ESP32 via MQTT.
ESP32 mengendalikan 5 servo motor berdasarkan data biner.
Tangan robot bergerak sesuai status jari pengguna.


🔗 Diagram Blok Hardware/Software
+----------------+       +----------------------+       +-----------------+
|  Webcam        |       |  Python + Mediapipe  |       |  ESP32          |
|  (Hand Input)  +-----> |  (Hand Tracking &    +-----> |  (Servo Control) |
|                |       |   MQTT Publisher)    |       |                 |
+----------------+       +----------------------+       +--------+--------+
                                                        |
                                                        |
                        +-------------------------------+-------------------------------+
                        |       |       |       |       |       |       |       |       |
                        v       v       v       v       v       v       v       v       v
                    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
                    | Servo | Servo | Servo | Servo | Servo | Servo | Servo | Servo | Servo |
                    |  1    |  2    |  3    |  4    |  5    |  1    |  2    |  3    |  4    |
                    | (Thumb)| (Index)| (Middle)| (Ring)| (Pinky)| (Thumb)| (Index)| (Middle)| (Ring)|
                    +-------+-------+-------+-------+-------+-------+-------+-------+-------+

Penjelasan:

Webcam: Menangkap gambar tangan pengguna secara real-time.
Python + Mediapipe: Memproses gambar untuk mendeteksi status jari (terbuka/tertutup) dan mengirim data biner melalui MQTT.
ESP32: Menerima data biner via MQTT dan menggerakkan 5 servo motor untuk meniru gerakan jari.


📊 Flowchart Sistem
graph TD
    A[Start] --> B[Capture Hand Video<br>(Webcam)]
    B --> C[Detect Landmarks<br>(Mediapipe)]
    C --> D[Process Finger States<br>(Open/Closed)]
    D --> E[Send Binary Data<br>(MQTT to ESP32)]
    E --> F[Move Servos<br>(ESP32)]
    F --> G{Repeat?}
    G -->|Yes| B
    G -->|No| H[End]

Penjelasan:

Flowchart dibuat lebih sederhana dengan label yang jelas dan deskriptif.
Setiap langkah diberi keterangan singkat untuk memudahkan pemahaman.
Struktur alur menunjukkan proses berulang hingga pengguna menghentikan program.


🚀 Cara Menjalankan

Install dependency Python:
pip install opencv-python mediapipe paho-mqtt


Upload kode ESP32:

Buka file gesture_clone_robot.ino di Arduino IDE atau PlatformIO.
Pastikan library WiFi, PubSubClient, dan ESP32Servo sudah terinstall.
Sesuaikan ssid, password, dan mqttServer di kode Arduino.
Upload kode ke ESP32.


Jalankan program Python:
python main.py


Gerakkan tangan di depan webcam, dan servo akan mengikuti gerakan jari Anda.



🙌 Kontribusi
Pull request dan ide pengembangan sangat diterima! Silakan buka Issue untuk diskusi, saran, atau pelaporan bug.

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
