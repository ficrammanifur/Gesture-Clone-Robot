import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import time

# MQTT Setup
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "OpenCV-IoT6601"
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam Setup
cap = cv2.VideoCapture(0)

# Landmark ujung jari dan pangkal jari untuk deteksi jari terbuka/tertutup
FINGER_TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
FINGER_PIPS = [3, 6, 10, 14, 18]  # Pangkal jari

def is_finger_open(landmarks, tip_id, pip_id):
    """Cek apakah jari terbuka berdasarkan posisi Y ujung jari vs pangkal"""
    tip_y = landmarks[tip_id].y
    pip_y = landmarks[pip_id].y
    # Untuk ibu jari, cek posisi X karena orientasinya berbeda
    if tip_id == 4:  # Thumb
        tip_x = landmarks[tip_id].x
        pip_x = landmarks[pip_id].x
        return tip_x < pip_x if landmarks[0].x < landmarks[5].x else tip_x > pip_x
    return tip_y < pip_y

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera")
            break

        # Flip dan konversi ke RGB untuk MediaPipe
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Proses deteksi tangan
        results = hands.process(frame_rgb)
        
        # Inisialisasi string biner untuk 5 jari (1: terbuka, 0: tertutup)
        finger_states = ['0'] * 5
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Gambar landmark tangan
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Cek status tiap jari
                for i, (tip, pip) in enumerate(zip(FINGER_TIPS, FINGER_PIPS)):
                    if is_finger_open(hand_landmarks.landmark, tip, pip):
                        finger_states[i] = '1'
                
                # Gabungkan status jari menjadi string biner (misal: "11001")
                binary_string = ''.join(finger_states)
                
                # Kirim ke MQTT
                client.publish(MQTT_TOPIC, binary_string)
                print(f"Mengirim: {binary_string}")
                
                # Tampilkan status jari di frame
                cv2.putText(frame, binary_string, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Tampilkan frame
        cv2.imshow('Hand Gesture Control', frame)
        
        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.1)  # Delay untuk mencegah pengiriman data terlalu cepat

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    # Bersihkan resource
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    client.disconnect()
