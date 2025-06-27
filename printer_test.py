import serial
import time

# Konfiguration der seriellen Verbindung (COM-Port ggf. anpassen)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
time.sleep(2)  # Wartezeit für Verbindungsaufbau

def send_gcode(command):
    ser.write((command + '\n').encode())
    time.sleep(0.5)
    while ser.in_waiting:
        print(ser.readline().decode().strip())

# Initialisierung: Homing aller Achsen
send_gcode("G28")  # Referenzfahrt

# Bewegung innerhalb des 150x150x150 mm Arbeitsraums
bewegungen = [
    "G1 X50 Y50 Z0 F3000",    # Position 1
    "G1 X100 Y50 Z50 F3000",  # Position 2
    "G1 X150 Y150 Z150 F3000" # Position 3
]

for befehl in bewegungen:
    send_gcode(befehl)
    time.sleep(1)

# Verbindung schließen
ser.close()
