"""Download Google's official pretrained MediaPipe Gesture Recognizer model.

Run:
    python download_gesture_model.py

This downloads gesture_recognizer.task into the current project folder.
"""
from pathlib import Path
from urllib.request import urlretrieve
import sys

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
)
MODEL_PATH = Path(__file__).resolve().parent / "gesture_recognizer.task"

def main():
    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 1_000_000:
        print(f"Model already exists: {MODEL_PATH}")
        print(f"Size: {MODEL_PATH.stat().st_size:,} bytes")
        return
    print("Downloading Google's pretrained gesture recognition model...")
    print("This may take a little while depending on your internet connection.")
    try:
        urlretrieve(MODEL_URL, MODEL_PATH)
    except Exception as exc:
        if MODEL_PATH.exists():
            MODEL_PATH.unlink()
        print(f"Download failed: {exc}")
        print("Open this official model URL in your browser and save it as gesture_recognizer.task:")
        print(MODEL_URL)
        sys.exit(1)
    size = MODEL_PATH.stat().st_size
    if size < 1_000_000:
        MODEL_PATH.unlink(missing_ok=True)
        print("Downloaded file looks too small; download may have failed.")
        sys.exit(1)
    print(f"Done! Model saved to: {MODEL_PATH}")
    print(f"Size: {size:,} bytes")

if __name__ == "__main__":
    main()
