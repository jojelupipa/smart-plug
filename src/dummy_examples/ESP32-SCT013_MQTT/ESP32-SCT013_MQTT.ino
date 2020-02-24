#include <Arduino.h>
#include "EmonLib.h"
#include "WiFi.h"
#include <driver/adc.h>
// MQTT Client Library
#include <PubSubClient.h>

// The GPIO pin were the CT sensor is connected to (should be an ADC input)
#define ADC_INPUT 34

#define HOME_VOLTAGE 230.0

// Force EmonLib to use 10bit ADC resolution
#define ADC_BITS    10
#define ADC_COUNTS  (1<<ADC_BITS)


EnergyMonitor emon1;

const int N_MEASURES = 6;
// Array to store the readings to print a mean
short measurements[N_MEASURES];
short measureIndex = 0;
unsigned long lastMeasurement = 0;
unsigned long timeFinishedSetup = 0;

//MQTT settings
const char* mqttServer = "192.168.1.10";
const int mqttPort = 1883;
const char* mqttUser = "esp32";
const char* mqttPassword = "esp32tfg";
String clientId = "ESP32Client";
WiFiClient wifiClient;
PubSubClient client(wifiClient);


void setup() {

  pinMode(32, OUTPUT);
  digitalWrite(32, HIGH);
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
  analogReadResolution(10);
  Serial.begin(9600);

  setWifi();
  setMQTTConnection();
  while (!Serial);

  // Initialize emon library (30 = calibration number)
  emon1.current(ADC_INPUT, 0.07);


  timeFinishedSetup = millis();
}


void loop() {
  unsigned long currentMillis = millis();

  // If it's been longer then 1000ms since we took a measurement, take one now!
  if(currentMillis - lastMeasurement > 1000){
    double amps = emon1.calcIrms(1000); // Calculate Irms only
    double watt = amps * HOME_VOLTAGE;

    lastMeasurement = millis();

    // Readings are unstable the first 5 seconds when the device powers on
      // so ignore them until they stabilise.
    if(millis() - timeFinishedSetup >= 10000){
      measurements[measureIndex] = watt;
      measureIndex++;
    }
  }

  // When we have several measurements, print them
  if (measureIndex == N_MEASURES) {
    double mean = 0.0;
    for (int i = 0; i < N_MEASURES; i++) {
      mean += measurements[i];
    }
    mean /= (double)N_MEASURES;
    Serial.println(mean);
    sendInfo(mean);
    measureIndex = 0;
  }

}

void setWifi() {
  WiFi.begin();
  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    Serial.println("Connecting to WiFi...");
  }
 
  Serial.print("Connected to the WiFi network. IP: ");
  Serial.println(WiFi.localIP());
}

void setMQTTConnection() {
  // Set the server IP and port
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.print("Stablishing MQTT connection... ");
    // Attempt to connect
    if (client.connect(clientId.c_str(),mqttUser,mqttPassword)) {
      Serial.println("connected");
      client.publish("/connections/presence/ESP32/", "connected");
      } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      // Wait a seconds before retrying
      delay(1000);  
    }
  }
}

void sendInfo(float consumption){
  if(!client.connected()){
    setMQTTConnection();
  }
  if (client.connect(clientId.c_str(),mqttUser,mqttPassword)) {
      client.publish("/consumption/", String(consumption).c_str());
      Serial.print("Data ");
      Serial.print(consumption);
      Serial.println(" sent");
  } else {
    Serial.println("The client was disconnected unexpectedly. Trying to resend...");
    delay(1000);
    sendInfo(consumption);
  }
}
