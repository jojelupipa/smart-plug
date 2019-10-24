import serial, time
arduino = serial.Serial('COM4', 9600)
time.sleep(2)
rawString = arduino.readline()
print(rawString)
arduino.close()

# Recuerda sustituir el puerto serie del código, en el ejemplo "COM4", por el puerto serie en el que tengas conectado Arduino.
