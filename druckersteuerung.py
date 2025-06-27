
import serial
import time

class DruckerSteuerung:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=2):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Verbindung stabilisieren

    def sende_gcode(self, command):
        print(f">>> Sende: {command}")
        self.ser.write((command + '\n').encode())
        while True:
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"<<< {line}")
            if "busy" in line.lower():
                continue
            if line == "ok":
                break

    def warte_auf_bewegungsende(self):
        self.sende_gcode("M400")

    def aktuelle_position(self):
        self.ser.write(b"M114\n")
        position_lines = []
        while True:
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                position_lines.append(line)
                if "ok" in line.lower():
                    break
        print("--- Aktuelle Position ---")
        for line in position_lines:
            print(line)

    def schliessen(self):
        self.ser.close()
