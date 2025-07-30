#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// ===== WiFi & MQTT Setup =====
const char* ssid = "infinix ";
const char* password = "12345678";
const char* mqttServer = "broker.emqx.io";
int port = 1883;  // ✅ Perbaikan: gunakan integer, bukan string

WiFiClient espClient;
PubSubClient client(espClient);
char clientId[50];

// ===== Servo Setup =====
const int servoPins[5] = {4, 16, 17, 18, 19}; // Ubah sesuai dengan pin yang kamu gunakan
Servo servos[5];

int angleOpen = 0;     // Jari terbuka
int angleClosed = 90;  // Jari menekuk

void wifiConnect() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Menghubungkan WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi terhubung.");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  String data = "";
  for (int i = 0; i < length; i++) data += (char)message[i];
  
  Serial.println("=========================");
  Serial.print("Topik: ");
  Serial.println(topic);
  Serial.print("Pesan diterima: ");
  Serial.println(data);

  if (data.length() == 5) {
    for (int i = 0; i < 5; i++) {
      int angle = (data.charAt(i) == '1') ? angleOpen : angleClosed;
      servos[i].write(angle);
      Serial.printf("Servo %d -> %d derajat\n", i, angle);
    }
  } else {
    Serial.println("⚠ Format tidak valid, harus 5 digit biner.");
  }
}

void mqttReconnect() {
  while (!client.connected()) {
    Serial.print("Menghubungkan MQTT...");
    long r = random(1000);
    sprintf(clientId, "clientId-%ld", r);
    if (client.connect(clientId)) {
      Serial.println(" MQTT terhubung.");
      client.subscribe("OpenCV-IoT6601");
    } else {
      Serial.print("Gagal, kode: ");
      Serial.print(client.state());
      Serial.println(" coba lagi dalam 5 detik.");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  wifiConnect();
  
  // MQTT setup
  client.setServer(mqttServer, port);
  client.setCallback(callback);

  // Servo attach & posisi awal
  for (int i = 0; i < 5; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(angleClosed);
    delay(200);  // Delay biar gerakan awal terlihat
  }
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    wifiConnect();
  }

  if (!client.connected()) {
    mqttReconnect();
  }
  client.loop();
}
