import serial
import time

arduino = serial.Serial("COM3",115200)

time.sleep(3)

datos = bytearray()

for i in range(64):
    datos.extend([255,0,0])

arduino.write(datos)