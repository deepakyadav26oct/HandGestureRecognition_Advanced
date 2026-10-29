from collections import Counter, deque
from datetime import datetime


class GestureHistory:
    """Keep a bounded history of detected gesture changes."""

    def __init__(self, max_items=100):
        self.events = deque(maxlen=max_items)
        self.counts = Counter()

    def add(self, gesture):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append((timestamp, gesture))
        self.counts[gesture] += 1

    def total(self):
        return sum(self.counts.values())

    def top_items(self, limit=4):
        return self.counts.most_common(limit)

    def recent(self, limit=5):
        return list(self.events)[-limit:][::-1]

    def summary_text(self):
        if not self.events:
            return "No gestures recorded yet."
        lines = [f"Total gesture changes: {self.total()}"]
        lines += [f"{name}: {count}" for name, count in self.counts.most_common()]
        lines += ["Recent:"] + [f"{stamp} - {gesture}" for stamp, gesture in self.recent(10)]
        return "\n".join(lines)
