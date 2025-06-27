import cv2
import numpy as np

def kalibriere_kreuzmarker_live_mit_overlay():
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Fehler: Kamera konnte nicht geöffnet werden.")
        return

    print("Drücke 'c' zur Kalibrierung, 'q' zum Beenden.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Kamerabildes.")
            break

        display_frame = frame.copy()
        cv2.imshow("Livebild", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('c'):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=30, maxLineGap=10)

            if lines is None:
                print("Keine Linien erkannt.")
                continue

            horizontal_lengths = []
            vertical_lengths = []

            for line in lines:
                x1, y1, x2, y2 = line[0]
                dx = x2 - x1
                dy = y2 - y1
                length = np.sqrt(dx**2 + dy**2)
                angle = np.arctan2(dy, dx) * 180 / np.pi

                if abs(angle) < 10:
                    horizontal_lengths.append(length)
                    cv2.line(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Grün für horizontal
                elif abs(angle - 90) < 10 or abs(angle + 90) < 10:
                    vertical_lengths.append(length)
                    cv2.line(display_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blau für vertikal

            if horizontal_lengths and vertical_lengths:
                avg_h = np.mean(horizontal_lengths)
                avg_v = np.mean(vertical_lengths)
                pixel_length = (avg_h + avg_v) / 2
                mm_per_pixel = 20.0 / pixel_length
                print(f"Horizontale Länge: {avg_h:.2f} px, Vertikale Länge: {avg_v:.2f} px")
                print(f"Skalierungsfaktor: {mm_per_pixel:.4f} mm/Pixel")
            else:
                print("Nicht genügend horizontale oder vertikale Linien erkannt.")

            cv2.imshow("Erkannte Linien", display_frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    kalibriere_kreuzmarker_live_mit_overlay()
