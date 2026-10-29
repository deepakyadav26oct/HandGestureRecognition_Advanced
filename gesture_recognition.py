import math


def _dist(a, b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (getattr(a, "z", 0)-getattr(b, "z", 0))**2)


def get_finger_states(landmarks, hand_label="Unknown"):
    """Return [thumb, index, middle, ring, little] raised-state booleans.

    The four long fingers use tip-vs-PIP y positions, which works best with
    the palm facing the camera and fingers pointing upward. Thumb extension
    uses distances from the palm rather than only comparing x coordinates.
    """
    p = landmarks
    states = []

    # Thumb: compare tip's distance from index MCP to thumb IP's distance.
    # Add a small margin to reduce false positives when the thumb is folded.
    thumb_tip_to_palm = _dist(p[4], p[5])
    thumb_ip_to_palm = _dist(p[3], p[5])
    thumb_extended = thumb_tip_to_palm > thumb_ip_to_palm * 1.18
    states.append(thumb_extended)

    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        states.append(p[tip].y < p[pip].y)

    return states


def get_finger_count(landmarks, hand_label="Unknown"):
    return sum(get_finger_states(landmarks, hand_label))


def fallback_gesture(landmarks, hand_label="Unknown"):
    """Fallback label when the pretrained model returns None/Unclassified."""
    states = get_finger_states(landmarks, hand_label)
    count = sum(states)
    thumb, index, middle, ring, little = states

    if count == 0:
        return "Closed Fist"
    if count == 5:
        return "Open Palm"
    if index and middle and not ring and not little:
        return "Peace Sign"
    if thumb and not index and not middle and not ring and not little:
        return "Thumbs Up"
    if not thumb and index and not middle and not ring and not little:
        return "Pointing Up"
    if count == 1:
        return "One Finger"
    if count == 3:
        return "Three Fingers"
    if count == 4:
        return "Four Fingers"
    return "Unclassified"
