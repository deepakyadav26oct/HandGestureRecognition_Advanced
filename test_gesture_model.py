import cv2
import mediapipe as mp
from pathlib import Path
import time

model = Path(__file__).resolve().parent / "gesture_recognizer.task"
print("Python MediaPipe:", mp.__version__)
print("Model path:", model)
print("Model exists:", model.exists(), "size:", model.stat().st_size if model.exists() else 0)

if not model.exists():
    raise SystemExit("ERROR: gesture_recognizer.task must be next to this script.")

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
RunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=str(model)),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
)
recognizer = GestureRecognizer.create_from_options(options)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    recognizer.close()
    raise SystemExit("ERROR: Could not open webcam.")

start = time.monotonic()
last_print = 0
print("Webcam started. Show a hand. Press Q to quit.")
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read webcam frame.")
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp = int((time.monotonic() - start) * 1000)
        result = recognizer.recognize_for_video(image, timestamp)

        label = "No hand detected"
        if result.gestures:
            top = result.gestures[0][0]
            label = f"{top.category_name} ({top.score:.2f})"
        elif result.hand_landmarks:
            label = "Hand found, gesture unclassified"

        cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.putText(frame, "Press Q to quit", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        cv2.imshow("MediaPipe Gesture Model Test", frame)

        now = time.time()
        if now - last_print > 1:
            print(label)
            last_print = now
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    recognizer.close()
    cv2.destroyAllWindows()
