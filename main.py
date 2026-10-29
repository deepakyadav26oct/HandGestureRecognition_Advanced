import time
import cv2

from camera import Camera
from hand_detector import HandDetector
from gesture_recognition import get_finger_count, fallback_gesture
from dashboard import draw_dashboard
from history import GestureHistory
from controls import VirtualMouseController, VolumeController


MODES = {ord("1"): "GESTURE", ord("2"): "MOUSE", ord("3"): "VOLUME"}


def main():
    camera = Camera()
    detector = HandDetector(max_hands=1)
    history = GestureHistory()
    mouse = VirtualMouseController()
    volume = VolumeController()

    if not camera.is_opened():
        print("ERROR: Webcam could not be opened.")
        camera.release()
        detector.close()
        return

    mode = "GESTURE"
    last_gesture = None
    last_gesture_time = 0.0
    fps = 0.0
    previous_time = time.time()
    start_time = time.monotonic()
    print("Gesture recognition started: 1=Gesture, 2=Mouse, 3=Volume, H=History, Q=Quit")

    try:
        while True:
            success, frame = camera.read_frame()
            if not success:
                print("Could not read webcam frame.")
                break

            timestamp_ms = int((time.monotonic() - start_time) * 1000)
            frame, hands = detector.find_hands(frame, timestamp_ms)

            gesture = "No hand detected"
            finger_count = None
            hand_label = "Unknown"
            action_message = "Show your hand to begin"

            if hands:
                hand = hands[0]
                landmarks = hand["landmarks"]
                hand_label = hand["label"]
                model_gesture = hand["gesture"]
                confidence = hand["score"]

                # Count is computed independently because the pretrained model
                # classifies gestures but does not return a finger count.
                finger_count = get_finger_count(landmarks, hand_label)

                # Prefer trained-model labels, but use landmark fallback for
                # frames where the model reports None/Unclassified.
                if model_gesture == "Unclassified" or confidence < 0.45:
                    gesture = fallback_gesture(landmarks, hand_label)
                    action_message = f"Landmark fallback; model score {confidence:.0%}"
                else:
                    gesture = model_gesture
                    action_message = f"Model confidence: {confidence:.0%}"

                now = time.time()
                if gesture != last_gesture and now - last_gesture_time > 0.30:
                    history.add(gesture)
                    last_gesture = gesture
                    last_gesture_time = now

                if mode == "MOUSE":
                    action_message = mouse.update(landmarks, frame.shape[1], frame.shape[0])
                elif mode == "VOLUME":
                    action_message = volume.update(landmarks, frame.shape[1], frame.shape[0])

            now = time.time()
            elapsed = now - previous_time
            if elapsed > 0:
                current_fps = 1.0 / elapsed
                fps = current_fps if fps == 0 else 0.85 * fps + 0.15 * current_fps
            previous_time = now

            draw_dashboard(
                frame=frame,
                mode=mode,
                gesture=gesture,
                finger_count=finger_count,
                hand_label=hand_label,
                fps=fps,
                history=history,
                action_message=action_message,
            )
            cv2.imshow("Hand Gesture Recognition - Trained Model", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key in MODES:
                mode = MODES[key]
            elif key == ord("h"):
                print("\\n--- Gesture History ---")
                print(history.summary_text())
                print("-----------------------\\n")
    finally:
        camera.release()
        detector.close()
        cv2.destroyAllWindows()
        mouse.close()
        volume.close()


if __name__ == "__main__":
    main()
