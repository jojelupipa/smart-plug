// La velocidad depende del modelo de ESP-01
// siendo habituales 9600 y 115200
const int baudRate = 9600;
 
#include "SoftwareSerial.h"
SoftwareSerial softSerial(2, 3); // RX, TX
 
void setup()
{
   Serial.begin(baudRate);
   softSerial.begin(baudRate);
}
 
void loop()
// enviar los datos de la consola serial al ESP-01, 
// y mostrar lo enviado por el ESP-01 a nuestra consola
{
   if (softSerial.available())
   {
      Serial.print((char)softSerial.read());
   }
   if (Serial.available())
   {
      softSerial.print((char)Serial.read());
   }
}
