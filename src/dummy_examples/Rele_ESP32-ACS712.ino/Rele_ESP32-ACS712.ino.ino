
/*
 Conexión Relé:
// S --> pin 19 (p.ej. vale cualquier pin de entrada/salida para la Señal)
// + --> 3.3V 
// - --> GND

**************************
 Conexión ACS712
// Out --> pin 34 (un pin analógico cualquiera) // Estos pines operan con 3.3V, hay que usar un divisor de tensión
// Vcc --> 5V
// Gnd--> GND
 */
int SAMPLESNUMBER = 100;
float zero= 0.0;
const int S_RELAY_PIN = 19;
const int ANALOG_READ_PIN = 34;
const int BAUD_RATIO = 9600;

void setup() {

  // Configuración puerto serie
  Serial.begin(BAUD_RATIO);
  while (!Serial);


  // Configuración relé 10A
  pinMode(S_RELAY_PIN, OUTPUT);
  digitalWrite(S_RELAY_PIN, LOW);
  delay(500);


  // Configurar cero para sensor ACS712

  uint32_t start= millis();
  zero= 0;
  int period= 1000;
  uint32_t measurements_count;
  measurements_count= 0;
  while (millis() - start < period) {
    zero+= analogRead(ANALOG_READ_PIN);
    measurements_count++;
    //delay(period/2);
  }
  zero/=measurements_count;
Serial.print("Zero: ");
Serial.println(zero);
Serial.print("count:");
Serial.println(measurements_count);
/*
  for (int i= 0; i<SAMPLESNUMBER; i++) {
    zero+=analogRead(ANALOG_READ_PIN);
  }
  zero/=SAMPLESNUMBER;
*/

  digitalWrite(S_RELAY_PIN, HIGH);
}

void printMeasure(String prefix, float value, String postfix)
{
  Serial.print(prefix);
  Serial.print(value, 3); // Segundo argumento formato: precisión en decimales
  Serial.println(postfix);

}



float getCurrentAC(uint16_t frequency= 50) {
  uint32_t period = 1000 / frequency;
  uint32_t t_start = millis();
  // Voltaje de referencia para ESP32(3.3V):
  const float VREF= 3.33;
  // Resolución, discretización en la conversión de una señal analógica a un valor numérico 4096 (0-4095) para ESP32.
  const float AtoDC = 4095.0;
  const float sensitivity = 0.100; // Sensibilidad del sensor ACS712_20A
//  const float zero= 512.0;

  uint32_t Isum = 0, measurements_count = 0;
  int32_t Inow;

for (int i= 0; i<3; i++) {
  t_start = millis();
  while (millis() - t_start < period) {
    Inow = zero - analogRead(ANALOG_READ_PIN);
    Isum += Inow*Inow;
    measurements_count++;
    delay(period/2);
  }
}
Isum/=3;

  float Irms = sqrt(Isum / measurements_count) / (AtoDC) * VREF / sensitivity;
//  Serial.println(Irms);
  return Irms;
}



void loop() {
  
   float current = getCurrentAC();
   float currentRMS = 0.707 * current;
//   float power = 230.0 * currentRMS;
//   float currentRMS = 1.1 * current;
   float power = 230.0 * currentRMS;

 
   printMeasure("Intensidad: ", current, "A ,");
   printMeasure("Irms: ", currentRMS, "A ,");
   printMeasure("Potencia: ", power, "W");

   delay(1000);
}
