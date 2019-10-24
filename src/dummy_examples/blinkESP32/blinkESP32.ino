void setup() {
pinMode(19,OUTPUT);
digitalWrite(19,LOW);
}

void loop() {
digitalWrite(19,HIGH);
delay(500);
digitalWrite(19,LOW);
delay(500);
}
