
/*
 Conexión Relé:
// S --> pin 9
// + --> 3.3V
// - --> GND

**************************
 Conexión ACS712
// Out --> A0
// Vcc --> 5V
// Gnd--> GND
 */
int SAMPLESNUMBER = 100;
float zero= 0.0;

void setup() {

  // Configuración relé 10A
  pinMode(9, OUTPUT);
  digitalWrite(9, LOW);
  delay(500);

  
  // Configurar cero para sensor ACS712
  for (int i= 0; i<SAMPLESNUMBER; i++) {
    zero+=analogRead(A0);
  }
  zero/=SAMPLESNUMBER;

  // Configuración puerto serie
  Serial.begin(9600);

  digitalWrite(9, HIGH);
}

void printMeasure(String prefix, float value, String postfix)
{
  Serial.print(prefix);
  Serial.print(value, 3);
  Serial.println(postfix);

}



float getCurrentAC(uint16_t frequency= 50) {
  uint32_t period = 1000000 / frequency;
  uint32_t t_start = micros();
  const float VREF= 5.0;
  const float sensitivity = 0.100;
//  const float zero= 512.0;

  uint32_t Isum = 0, measurements_count = 0;
  int32_t Inow;

  while (micros() - t_start < period) {
    Inow = zero - analogRead(A0);
    Isum += Inow*Inow;
    measurements_count++;
  }

  float Irms = sqrt(Isum / measurements_count) / 1023.0 * VREF / sensitivity;
  return Irms;
}



void loop() {
  
   float current = getCurrentAC();
//   float currentRMS = 0.707 * current;
//   float power = 230.0 * currentRMS;
   float currentRMS = 1.1 * current;
   float power = 230.0 * currentRMS;
 
   printMeasure("Intensidad: ", current, "A ,");
   printMeasure("Irms: ", currentRMS, "A ,");
   printMeasure("Potencia: ", power, "W");

   delay(1000);
}
