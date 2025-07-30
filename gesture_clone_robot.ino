#include <WiFi.h>              // Library untuk koneksi WiFi
#include <PubSubClient.h>      // Library untuk koneksi MQTT
#include <ESP32Servo.h>        // Library untuk mengontrol servo di ESP32

// ===== WiFi & MQTT Setup =====
const char* ssid = "=MASUKAN USERNAME WIFI";        // SSID WiFi yang digunakan
const char* password = "MASUKAN PASS WIFI";         // Password WiFi
const char* mqttServer = "broker.emqx.io";          // Alamat broker MQTT
int port = 1883;                                    // Port MQTT (default 1883)

WiFiClient espClient;            // Objek koneksi WiFi
PubSubClient client(espClient);  // Objek MQTT client menggunakan WiFi
char clientId[50];               // Buffer untuk ID unik client MQTT

// ===== Servo Setup =====
const int servoPins[5] = {4, 16, 17, 18, 19}; // Pin GPIO yang terhubung ke servo
Servo servos[5];                             // Array objek servo

int angleOpen = 0;     // Derajat posisi servo saat jari terbuka
int angleClosed = 90;  // Derajat posisi servo saat jari tertutup

void wifiConnect() {
  WiFi.mode(WIFI_STA);                     // Atur mode WiFi sebagai Station
  WiFi.begin(ssid, password);              // Mulai koneksi WiFi
  Serial.print("Menghubungkan WiFi");
  while (WiFi.status() != WL_CONNECTED) {  // Tunggu sampai terhubung
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi terhubung.");     // Tampilkan status terhubung
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());          // Cetak alamat IP ESP32
}

void callback(char* topic, byte* message, unsigned int length) {
  String data = "";                          // Variabel untuk menyimpan pesan
  for (int i = 0; i < length; i++) data += (char)message[i]; // Konversi byte ke string

  Serial.println("=========================");
  Serial.print("Topik: ");
  Serial.println(topic);                    // Tampilkan topik pesan
  Serial.print("Pesan diterima: ");
  Serial.println(data);                     // Tampilkan isi pesan

  if (data.length() == 5) {                 // Cek apakah data berisi 5 karakter
    for (int i = 0; i < 5; i++) {
      int angle = (data.charAt(i) == '1') ? angleOpen : angleClosed; // '1' buka, selain itu tutup
      servos[i].write(angle);              // Atur sudut servo sesuai data
      Serial.printf("Servo %d -> %d derajat\n", i, angle); // Cetak info servo
    }
  } else {
    Serial.println("⚠ Format tidak valid, harus 5 digit biner."); // Validasi format pesan
  }
}

void mqttReconnect() {
  while (!client.connected()) {                      // Coba sambung ke MQTT selama belum terhubung
    Serial.print("Menghubungkan MQTT...");
    long r = random(1000);                           // Buat ID client acak
    sprintf(clientId, "clientId-%ld", r);
    if (client.connect(clientId)) {                  // Coba koneksi MQTT
      Serial.println(" MQTT terhubung.");
      client.subscribe("OpenCV-IoT6601");            // Langganan ke topik MQTT
    } else {
      Serial.print("Gagal, kode: ");
      Serial.print(client.state());                  // Tampilkan error code
      Serial.println(" coba lagi dalam 5 detik.");
      delay(5000);                                   // Tunggu sebelum mencoba lagi
    }
  }
}

void setup() {
  Serial.begin(115200);                 // Mulai Serial monitor
  wifiConnect();                        // Hubungkan ke WiFi

  client.setServer(mqttServer, port);   // Atur server MQTT
  client.setCallback(callback);         // Atur fungsi callback untuk pesan masuk

  // Inisialisasi servo dan atur posisi awal ke menekuk
  for (int i = 0; i < 5; i++) {
    servos[i].attach(servoPins[i]);     // Sambungkan objek servo ke pin GPIO
    servos[i].write(angleClosed);       // Atur posisi awal menekuk
    delay(200);                         // Delay agar gerakan terlihat jelas
  }
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {  // Jika WiFi terputus, sambungkan ulang
    wifiConnect();
  }

  if (!client.connected()) {            // Jika MQTT terputus, sambungkan ulang
    mqttReconnect();
  }
  client.loop();                        // Proses loop MQTT untuk menerima pesan
}
