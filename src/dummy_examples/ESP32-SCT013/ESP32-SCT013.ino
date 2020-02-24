#include <Arduino.h>
#include "EmonLib.h"
#include "WiFi.h"
#include <driver/adc.h>

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


void setup() {

  pinMode(32, OUTPUT);
  digitalWrite(32, HIGH);
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
  analogReadResolution(10);
  Serial.begin(9600);
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
    measureIndex = 0;
  }

}
