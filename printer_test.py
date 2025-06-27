import serial
import time

# Serielle Verbindung konfigurieren
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
time.sleep(2)  # Verbindung stabilisieren

def send_gcode_wait_ok(command):
    print(f">>> Sende: {command}")
    ser.write((command + '\n').encode())
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print(f"<<< {line}")
        if "busy" in line.lower():
            continue
        if line == "ok":
            break

def get_position():
    ser.write(b"M114\n")
    position_lines = []
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            position_lines.append(line)
            if "ok" in line.lower():
                break
    print("--- Aktuelle Position ---")
    for line in position_lines:
        print(line)

# Initialisierung
send_gcode_wait_ok("G28")
send_gcode_wait_ok("G90")
send_gcode_wait_ok("G1 X75 Y75 Z20")
send_gcode_wait_ok("M400")
send_gcode_wait_ok("G9101")

# Interaktiver Modus
print("\n--- Interaktiver Modus (Relativbewegung) ---")
print("Gib relative Schritte für X Y Z ein (z. B. '10 0 -5') oder 'exit' zum Beenden:")

try:
    while True:
        user_input = input("ΔX ΔY ΔZ > ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        try:
            dx, dy, dz = map(float, user_input.split())
            command = f"G1 X{dx} Y{dy} Z{dz}"
            send_gcode_wait_ok(command)
            send_gcode_wait_ok("M400")
            get_position()
        except ValueError:
            print("Ungültige Eingabe. Bitte drei Zahlen eingeben, z. B. '10 0 -5'.")
except KeyboardInterrupt:
    print("\nBeendet durch Benutzer.")

ser.close()
print("Verbindung geschlossen.")
