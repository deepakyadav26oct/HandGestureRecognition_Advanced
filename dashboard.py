import cv2


def draw_dashboard(frame, mode, gesture, finger_count, hand_label, fps, history, action_message):
    """Draw a compact status dashboard on the webcam frame."""
    h, w = frame.shape[:2]
    panel_w = min(470, w - 20)
    panel_h = min(245, h - 20)
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (18, 25, 35), -1)
    cv2.addWeighted(overlay, 0.82, frame, 0.18, 0, frame)

    lines = [
        ("HAND GESTURE RECOGNITION", (0, 255, 160), 0.68),
        (f"Mode: {mode}     Hand: {hand_label}", (245, 245, 245), 0.55),
        (f"Gesture: {gesture}", (0, 220, 255), 0.62),
        (f"Finger count: {finger_count if finger_count is not None else '-'}", (245, 245, 245), 0.55),
        (f"FPS: {fps:.1f}     Gesture changes: {history.total()}", (200, 220, 255), 0.5),
        (f"Action: {action_message[:42]}", (220, 240, 220), 0.46),
        ("1 Gesture  |  2 Mouse  |  3 Volume  |  H History  |  Q Quit", (230, 230, 230), 0.43),
    ]

    y = 38
    for i, (text, color, scale) in enumerate(lines):
        cv2.putText(frame, text, (22, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2 if i == 0 else 1, cv2.LINE_AA)
        y += 31 if i == 0 else 29

    # Recent gesture list is useful for the demo.
    recent = history.recent(3)
    start_y = min(panel_h + 32, h - 65)
    cv2.putText(frame, "Recent:", (20, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 160), 1)
    for idx, (stamp, name) in enumerate(recent):
        y = start_y + 22 + idx * 20
        if y < h - 8:
            cv2.putText(frame, f"{stamp}  {name}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.43, (245, 245, 245), 1)
