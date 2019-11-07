
/*
 Conexión Relé:
// S --> pin 19 (p.ej. vale cualquier pin de entrada/salida)
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

  // Configuración relé 10A
  pinMode(S_RELAY_PIN, OUTPUT);
  digitalWrite(S_RELAY_PIN, LOW);
  delay(500);

  
  // Configurar cero para sensor ACS712
  for (int i= 0; i<SAMPLESNUMBER; i++) {
    zero+=analogRead(ANALOG_READ_PIN);
  }
  zero/=SAMPLESNUMBER;

  // Configuración puerto serie
  Serial.begin(BAUD_RATIO);

  digitalWrite(S_RELAY_PIN, HIGH);
}

void printMeasure(String prefix, float value, String postfix)
{
  Serial.print(prefix);
  Serial.print(value, 3); // Segundo argumento formato: precisión en decimales
  Serial.println(postfix);

}



float getCurrentAC(uint16_t frequency= 50) {
  uint32_t period = 1000000 / frequency;
  uint32_t t_start = micros();
  // Voltaje de referencia para Arduino(5V):
  const float VREF= 3.33;
  // Resolución, discretización en la conversión de una señal analógica a un valor numérico 1024 (0-1023) para arduino.
  const float AtoDC = 4095.0;
  const float sensitivity = 0.100;
//  const float zero= 512.0;

  uint32_t Isum = 0, measurements_count = 0;
  int32_t Inow;

  while (micros() - t_start < period) {
    Inow = zero - analogRead(ANALOG_READ_PIN);
    Isum += Inow*Inow;
    measurements_count++;
  }

  float Irms = sqrt(Isum / measurements_count) / AtoDC * VREF / sensitivity;
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
