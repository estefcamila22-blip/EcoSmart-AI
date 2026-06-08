#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "192.168.1.100";

WiFiClient espClient;
PubSubClient client(espClient);

// Sensor pins
const int POWER_SENSOR_PIN = 34;  // Analog pin for power sensor
const int TEMP_SENSOR_PIN = 35;   // Temperature sensor
const int OCCUPANCY_PIN = 32;     // PIR occupancy sensor

// Device info
const char* device_id = "esai_sensor_001";
const char* device_name = "Living Room Sensor";
const char* device_type = "energy_monitor";

void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(POWER_SENSOR_PIN, INPUT);
  pinMode(TEMP_SENSOR_PIN, INPUT);
  pinMode(OCCUPANCY_PIN, INPUT);
  
  // Connect to WiFi
  connectToWiFi();
  
  // Setup MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(mqttCallback);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  
  // Read sensors every 5 seconds
  static unsigned long lastRead = 0;
  if (millis() - lastRead > 5000) {
    lastRead = millis();
    readAndPublishData();
  }
}

void connectToWiFi() {
  Serial.println("\nStarting WiFi connection...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect(device_id)) {
      Serial.println("connected");
      // Subscribe to control topics
      client.subscribe("esai/devices/+/control");
      client.subscribe("esai/home/+/automation");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void readAndPublishData() {
  // Read power consumption (raw ADC value converted to watts)
  int rawPower = analogRead(POWER_SENSOR_PIN);
  float voltage = (rawPower / 4095.0) * 3.3;
  float power_w = voltage * 300;  // Convert to watts (calibration factor)
  
  // Read temperature
  int rawTemp = analogRead(TEMP_SENSOR_PIN);
  float temperature = ((rawTemp / 4095.0) * 3.3 - 0.5) * 100;  // TMP36 sensor
  
  // Read occupancy
  bool occupancy = digitalRead(OCCUPANCY_PIN);
  
  // Create JSON payload
  StaticJsonDocument<256> doc;
  doc["device_id"] = device_id;
  doc["device_name"] = device_name;
  doc["timestamp"] = millis() / 1000;
  doc["power_w"] = power_w;
  doc["temperature_c"] = temperature;
  doc["occupancy"] = occupancy ? "occupied" : "empty";
  doc["rssi"] = WiFi.RSSI();
  
  // Publish to MQTT
  String topic = String("esai/devices/") + device_id + "/data";
  char buffer[256];
  serializeJson(doc, buffer);
  client.publish(topic.c_str(), buffer);
  
  Serial.print("Published: ");
  Serial.println(buffer);
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);
  
  // Parse JSON command
  StaticJsonDocument<256> doc;
  deserializeJson(doc, payload, length);
  
  String command = doc["command"];
  Serial.print("Command: ");
  Serial.println(command);
  
  // Execute command
  if (command == "ping") {
    sendPingResponse();
  } else if (command == "restart") {
    Serial.println("Restarting device...");
    delay(1000);
    ESP.restart();
  }
}

void sendPingResponse() {
  StaticJsonDocument<128> response;
  response["device_id"] = device_id;
  response["status"] = "online";
  response["uptime"] = millis() / 1000;
  
  String topic = String("esai/devices/") + device_id + "/response";
  char buffer[256];
  serializeJson(response, buffer);
  client.publish(topic.c_str(), buffer);
}