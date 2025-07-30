import cv2                                      # Library untuk menangani kamera dan visualisasi
import mediapipe as mp                          # Library untuk deteksi tangan (dari Google)
import paho.mqtt.client as mqtt                 # Library untuk komunikasi MQTT
import time                                     # Untuk delay

# MQTT Setup
MQTT_BROKER = "broker.emqx.io"                 # Alamat broker MQTT
MQTT_PORT = 1883                               # Port MQTT standar
MQTT_TOPIC = "OpenCV-IoT6601"                  # Topik MQTT yang akan digunakan
client = mqtt.Client()                         # Inisialisasi client MQTT
client.connect(MQTT_BROKER, MQTT_PORT, 60)     # Sambungkan ke broker

# MediaPipe Setup
mp_hands = mp.solutions.hands                  # Inisialisasi modul hands dari MediaPipe
hands = mp_hands.Hands(                         # Konfigurasi deteksi tangan
    max_num_hands=1,                            # Maksimal 1 tangan
    min_detection_confidence=0.7                # Minimum confidence detection
)
mp_draw = mp.solutions.drawing_utils           # Untuk menggambar titik tangan

# Webcam Setup
cap = cv2.VideoCapture(0)                      # Gunakan kamera default (webcam index 0)

# Landmark ujung jari dan pangkal jari untuk deteksi jari terbuka/tertutup
FINGER_TIPS = [4, 8, 12, 16, 20]               # ID landmark ujung jari: Thumb, Index, Middle, Ring, Pinky
FINGER_PIPS = [3, 6, 10, 14, 18]               # ID landmark pangkal jari (PIP joint)

def is_finger_open(landmarks, tip_id, pip_id):
    """Cek apakah jari terbuka berdasarkan posisi Y ujung jari vs pangkal"""
    tip_y = landmarks[tip_id].y               # Posisi vertikal ujung jari
    pip_y = landmarks[pip_id].y               # Posisi vertikal pangkal jari
    if tip_id == 4:                           # Jika ibu jari (thumb)
        tip_x = landmarks[tip_id].x
        pip_x = landmarks[pip_id].x
        # Deteksi terbuka berdasarkan arah ibu jari relatif ke telapak
        return tip_x < pip_x if landmarks[0].x < landmarks[5].x else tip_x > pip_x
    return tip_y < pip_y                      # Jika ujung lebih atas dari pangkal → terbuka

try:
    while cap.isOpened():                     # Selama kamera aktif
        ret, frame = cap.read()               # Baca frame dari kamera
        if not ret:
            print("Gagal membaca frame dari kamera")
            break

        frame = cv2.flip(frame, 1)                               # Balik horizontal (mirror)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      # Ubah ke format RGB

        results = hands.process(frame_rgb)                      # Proses deteksi tangan

        finger_states = ['0'] * 5                               # Awalnya semua jari dianggap tertutup

        if results.multi_hand_landmarks:                        # Jika tangan terdeteksi
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(                         # Gambar landmark tangan di frame
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Periksa setiap jari apakah terbuka atau tidak
                for i, (tip, pip) in enumerate(zip(FINGER_TIPS, FINGER_PIPS)):
                    if is_finger_open(hand_landmarks.landmark, tip, pip):
                        finger_states[i] = '1'                  # Tandai jari sebagai terbuka

                binary_string = ''.join(finger_states)          # Gabung jadi string biner (misal: 10101)
                client.publish(MQTT_TOPIC, binary_string)       # Kirim ke broker MQTT
                print(f"Mengirim: {binary_string}")             # Log ke terminal

                # Tampilkan status biner di layar
                cv2.putText(frame, binary_string, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

        cv2.imshow('Hand Gesture Control', frame)               # Tampilkan video di window

        if cv2.waitKey(1) & 0xFF == ord('q'):                   # Tekan 'q' untuk keluar
            break

        time.sleep(0.1)                                         # Delay agar tidak kirim data terlalu cepat

except KeyboardInterrupt:
    print("Program dihentikan")                                # Handle CTRL+C dari terminal

finally:
    cap.release()               # Matikan kamera
    cv2.destroyAllWindows()     # Tutup semua window OpenCV
    hands.close()               # Tutup proses MediaPipe
    client.disconnect()         # Putuskan koneksi MQTT
