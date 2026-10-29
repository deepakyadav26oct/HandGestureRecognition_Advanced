import cv2


class Camera:
    """OpenCV webcam wrapper."""

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def is_opened(self):
        return self.cap.isOpened()

    def read_frame(self):
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)
        return success, frame

    def release(self):
        self.cap.release()
