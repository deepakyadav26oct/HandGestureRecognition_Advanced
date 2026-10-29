from pathlib import Path
import cv2
import mediapipe as mp
import math

MODEL_PATH = Path(__file__).resolve().parent / "gesture_recognizer.task"

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
]


class HandDetector:
    """MediaPipe Tasks pretrained gesture recognizer + landmark output."""

    def __init__(self, max_hands=1, detection_confidence=0.55, tracking_confidence=0.55):
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}\n"
                "Put gesture_recognizer.task next to main.py."
            )

        if not hasattr(mp, "tasks"):
            raise RuntimeError(
                "MediaPipe Tasks API is unavailable in this environment. "
                "Use the environment where the diagnostic script worked."
            )

        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        self.mp = mp

    def find_hands(self, frame, timestamp_ms):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rgb)
        result = self.recognizer.recognize_for_video(image, int(timestamp_ms))
        detected = []

        if result.hand_landmarks:
            handedness = result.handedness or []
            gesture_lists = result.gestures or []
            for i, landmarks in enumerate(result.hand_landmarks):
                label = "Unknown"
                if i < len(handedness) and handedness[i]:
                    label = handedness[i][0].category_name or "Unknown"

                gesture = "Unclassified"
                score = 0.0
                if i < len(gesture_lists) and gesture_lists[i]:
                    top = gesture_lists[i][0]
                    raw_name = top.category_name or "None"
                    score = float(top.score)
                    gesture = {
                        "Closed_Fist": "Closed Fist",
                        "Open_Palm": "Open Palm",
                        "Pointing_Up": "Pointing Up",
                        "Thumb_Down": "Thumbs Down",
                        "Thumb_Up": "Thumbs Up",
                        "Victory": "Peace Sign",
                        "ILoveYou": "I Love You",
                        "None": "Unclassified",
                    }.get(raw_name, raw_name.replace("_", " "))

                self._draw_landmarks(frame, landmarks)
                detected.append({
                    "landmarks": landmarks,
                    "label": label,
                    "gesture": gesture,
                    "score": score,
                })
        return frame, detected

    @staticmethod
    def _draw_landmarks(frame, points):
        h, w = frame.shape[:2]
        pixels = [(int(p.x * w), int(p.y * h)) for p in points]
        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, pixels[start], pixels[end], (80, 220, 120), 2)
        for x, y in pixels:
            cv2.circle(frame, (x, y), 4, (0, 220, 255), -1)

    def close(self):
        self.recognizer.close()
