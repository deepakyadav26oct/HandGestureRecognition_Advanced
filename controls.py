import math
import time


class VirtualMouseController:
    """Optional mouse control using index fingertip and pinch-to-click."""

    def __init__(self):
        self.enabled = True
        self.pyautogui = None
        self.screen_w = self.screen_h = None
        self.last_click = 0.0
        self.click_cooldown = 0.7
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.screen_w, self.screen_h = pyautogui.size()
            # Prevent pyautogui's corner fail-safe from being disabled.
            pyautogui.FAILSAFE = True
        except Exception as exc:
            self.enabled = False
            print(f"Virtual mouse unavailable: {exc}")

    def update(self, landmarks, frame_w, frame_h):
        if not self.enabled:
            return "Mouse unavailable: install pyautogui"
        p = landmarks
        index_tip = p[8]
        thumb_tip = p[4]

        # Leave a margin so cursor doesn't jitter at the very edge.
        x = max(0, min(self.screen_w - 1, int(index_tip.x * self.screen_w)))
        y = max(0, min(self.screen_h - 1, int(index_tip.y * self.screen_h)))
        try:
            self.pyautogui.moveTo(x, y, duration=0.02)
            gap = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
            now = time.time()
            if gap < 0.035 and now - self.last_click > self.click_cooldown:
                self.pyautogui.click()
                self.last_click = now
                return "Mouse moved; pinch click"
            return "Move index finger; pinch thumb+index to click"
        except Exception as exc:
            return f"Mouse control error: {exc}"

    def close(self):
        pass



class VolumeController:
    """Control Windows master volume using thumb-index finger distance."""

    def __init__(self):
        self.enabled = False
        self.volume = None
        self.last_set = 0.0
        self.last_level = None

        try:
            from pycaw.pycaw import AudioUtilities

            speakers = AudioUtilities.GetSpeakers()

            # Compatible with newer and older pycaw versions
            if hasattr(speakers, "EndpointVolume"):
                self.volume = speakers.EndpointVolume
            else:
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import IAudioEndpointVolume

                interface = speakers.Activate(
                    IAudioEndpointVolume._iid_,
                    CLSCTX_ALL,
                    None
                )
                self.volume = cast(
                    interface, POINTER(IAudioEndpointVolume)
                )

            # Test that the Windows audio device is accessible
            current = self.volume.GetMasterVolumeLevelScalar()
            print(f"Volume controller ready: {int(current * 100)}%")
            self.enabled = True

        except Exception as exc:
            print(f"Volume initialization failed: {exc}")

    def update(self, landmarks, frame_w, frame_h):
        if not self.enabled:
            return "Volume unavailable - check terminal error"

        thumb = landmarks[4]
        index = landmarks[8]

        # Distance between thumb tip and index fingertip
        gap = math.hypot(
            thumb.x - index.x,
            thumb.y - index.y
        )

        # Convert finger distance into volume percentage
        level = max(
            0.0,
            min(1.0, (gap - 0.025) / (0.22 - 0.025))
        )

        now = time.time()

        # Update only when needed to avoid excessive audio calls
        if (
            self.last_level is None
            or abs(level - self.last_level) >= 0.015
        ) and now - self.last_set >= 0.12:
            try:
                self.volume.SetMasterVolumeLevelScalar(
                    float(level), None
                )
                self.last_level = level
                self.last_set = now
            except Exception as exc:
                return f"Volume error: {exc}"

        return f"Volume control: {int(level * 100)}%"

    def close(self):
        pass

