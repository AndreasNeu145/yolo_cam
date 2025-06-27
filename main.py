import cv2
import threading
import serial
import time

# Druckersteuerung als Klasse
class DruckerSteuerung:
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(2)

    def sende_gcode(self, command):
        self.ser.write((command + '\n').encode())
        while True:
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"<<< {line}")
            if "busy" in line.lower():
                continue
            if line == "ok":
                break

    def initialisiere(self):
        self.sende_gcode("G28")

    def setze_startposition(self):
        self.sende_gcode("G90")
        self.sende_gcode("G1 X75 Y75 Z80")
        self.sende_gcode("M400")

    def schalte_relativmodus(self):
        self.sende_gcode("G91")

    def bewege_relativ(self, dx, dy, dz):
        befehl = f"G1 X{dx} Y{dy} Z{dz}"
        self.sende_gcode(befehl)
        self.sende_gcode("M400")

    def position_ausgeben(self):
        self.ser.write(b"M114\n")
        while True:
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"<<< {line}")
            if "ok" in line.lower():
                break

    def schliessen(self):
        self.ser.close()

# Webcam-Anzeige in separatem Fenster
def webcam_anzeige():
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Fehler: Webcam konnte nicht geöffnet werden.")
        return

    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Webcam-Bildes.")
            break

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Webcam-Fenster geschlossen.")
            break

    cap.release()
    cv2.destroyWindow("Webcam")

# Hauptprogramm
def main():
    drucker = DruckerSteuerung('/dev/ttyUSB0')
    drucker.initialisiere()
    drucker.setze_startposition()
    drucker.schalte_relativmodus()

    # Starte Webcam-Anzeige in separatem Thread
    webcam_thread = threading.Thread(target=webcam_anzeige, daemon=True)
    webcam_thread.start()

    print("\n--- Interaktiver Modus (Relativbewegung) ---")
    print("Gib relative Schritte für X Y Z ein (z. B. '10 0 -5') oder 'exit' zum Beenden:")

    try:
        while True:
            user_input = input("ΔX ΔY ΔZ > ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            try:
                dx, dy, dz = map(float, user_input.split())
                drucker.bewege_relativ(dx, dy, dz)
                drucker.position_ausgeben()
            except ValueError:
                print("Ungültige Eingabe. Bitte drei Zahlen eingeben, z. B. '10 0 -5'.")
    except KeyboardInterrupt:
        print("\nBeendet durch Benutzer.")

    drucker.schliessen()
    print("Verbindung geschlossen.")

if __name__ == "__main__":
    main()
