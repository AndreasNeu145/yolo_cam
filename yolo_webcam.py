from ultralytics import YOLO
import cv2

# Modell laden (nano-Version, schnell und leicht)
model = YOLO("models/yolov8n.pt")

# Webcam öffnen (Index 0 = Standardkamera)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 5)

if not cap.isOpened():
    print("❌ Fehler beim Öffnen der Kamera")
    exit()

print("✅ Kamera geöffnet. Drücke 'q' zum Beenden.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()

    for box in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, box[:4])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Mittelpunkt als Kreis zeichnen
        cv2.circle(annotated_frame, (cx, cy), 5, (0, 255, 255), -1)

        # Koordinaten als Text anzeigen
        cv2.putText(
            annotated_frame,
            f"({cx}, {cy})",
            (cx + 10, cy - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            2
        )

    cv2.imshow("YOLOv8 Live", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
