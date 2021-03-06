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
const int IRMS_SAMPLES = 1000;
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
String publishTopic = "/data/consumption/";
String receiverTopic = "/control/toggle/";
String plugID = "enchufe001";

//Wifi Settings
const char* ssid = "replaceWithSSID";
const char* password =  "replaceWithPassword";
WiFiClient wifiClient;
PubSubClient client(wifiClient);
String relayStatus = "HIGH";


void setup() {
  publishTopic = publishTopic + plugID;
  receiverTopic = receiverTopic + plugID;
  pinMode(32, OUTPUT);
  digitalWrite(32, HIGH);
  relayStatus = "HIGH";
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
  analogReadResolution(10);
  Serial.begin(9600);

  setWifi();
  setMQTTConnection();
  while (!Serial);

  // Initialize emon library (0.07 = calibration number)
  emon1.current(ADC_INPUT, 0.07);


  timeFinishedSetup = millis();
}


void loop() {
  unsigned long currentMillis = millis();

  // If it's been longer then 1000ms since we took a measurement, take one now!
  if(currentMillis - lastMeasurement > 1000){
    double amps = emon1.calcIrms(IRMS_SAMPLES); // Calculate Irms only
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
  client.loop();
}


// Start up wifi, if it's first time, must use Wifi.begin(ssid, password) to connect. You can use Wifi.begin() afterwards
// to avoid exposing your password in your code


void setWifi() {
  WiFi.begin(); // Asume you already connected it, otherwise you'll have to use Wifi.begin(<ssid>,<password>)
  //Wifi.begin(ssid, password)
  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    Serial.println("Connecting to WiFi...");
  }
 
  Serial.print("Connected to the WiFi network. IP: ");
  Serial.println(WiFi.localIP());
}


// Connects to the server


void setMQTTConnection() {
  // Set the server IP and port
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.print("Stablishing MQTT connection... ");
    // Attempt to connect
    if (client.connect(clientId.c_str(),mqttUser,mqttPassword)) {
      Serial.println("connected");
      String connectionMessage = String("/connections/presence/ESP32/");
      connectionMessage += plugID;
      client.publish( connectionMessage.c_str(), "connected");
      if(client.subscribe(receiverTopic.c_str()) && client.subscribe("/control/toggle/general")) {
        String suscribedMessage = String("esp32 subbed to /control/toggle/general and ");
        suscribedMessage += receiverTopic;
        client.publish("/connections/presence/ESP32/", suscribedMessage.c_str());
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      // Wait a second before retrying
      delay(1000);  
    }
  }
}


// Tries to connect and send the read data


void sendInfo(float consumption) {
  if(!client.connected()){
    setMQTTConnection();
  }
  if (client.connect(clientId.c_str(),mqttUser,mqttPassword)) {
      client.publish(publishTopic.c_str(), String(consumption).c_str());
      Serial.print("Data ");
      Serial.print(consumption);
      Serial.println(" sent");
  } else {
    Serial.println("The client was disconnected unexpectedly. Trying to resend...");
    delay(1000);
    sendInfo(consumption);
  }
}


// Callback function to manage the relay's status


void callback(char* topic, byte *payload, unsigned int length) {
  Serial.println("-------new message from broker-----");
  Serial.print("channel:");
  Serial.println(topic);
  Serial.print("data:");  
  Serial.write(payload, length);
  Serial.println();

  // Smart Switch is only subbed to /control/toggle/<plugID> and /control/toggle/general (general toggle) so it will change relay's status when any message is received
  toggleRelay();
}


// Toggles the Relay status


void toggleRelay() {
  if (relayStatus == "HIGH"){
      digitalWrite(32, LOW);
      relayStatus = "LOW";  
  } else if (relayStatus == "LOW") {
      digitalWrite(32, HIGH);
      relayStatus = "HIGH";
  }
}
