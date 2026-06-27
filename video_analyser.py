import cv2
import numpy as np
from collections import deque
from ultralytics import YOLO


class VideoAnalyzer:

    def __init__(self, path):
        self.path = path
        self.model = YOLO("yolov8n.pt")

        self.motion_buf = deque(maxlen=600)
        self.player_buf = deque(maxlen=600)

        self.momentum = []
        self.events = []

        self.last_event_frame = -999
        self.cooldown = 20

    # ---------------- MOTION ENGINE ----------------
    def motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(np.clip(np.std(gray) / 20, 0, 10))

    # ---------------- PLAYER ESTIMATION ----------------
    def players(self, frame):
        res = self.model(frame, verbose=False)[0]

        count = 0
        for b in res.boxes:
            cls = int(b.cls[0])
            if res.names[cls] == "person":
                count += 1

        return count

    # ---------------- TEAM STYLE CLASSIFIER ----------------
    def team_style(self, avg_m, avg_p):

        if avg_m > 7 and avg_p >= 8:
            return "High-press attacking team"
        elif avg_p > 8:
            return "Possession control team"
        elif avg_p < 6:
            return "Defensive low block team"
        elif avg_m > 6:
            return "Fast transition team"

        return "Balanced team"

    # ---------------- EVENT DETECTOR ----------------
    def detect_events(self, frame_id, m, p):

        if frame_id - self.last_event_frame < self.cooldown:
            return []

        event = None

        if m > 8 and p >= 8:
            event = "High press / attacking surge"
        elif m > 7 and p <= 5:
            event = "Counter attacking moment"
        elif m < 2:
            event = "Slow build-up phase"
        elif m > 6 and p <= 3:
            event = "Defensive instability"

        if not event:
            return []

        self.last_event_frame = frame_id

        return [{
            "frame": frame_id,
            "event": event,
            "motion": m,
            "players": p
        }]

    # ---------------- SCOUT REPORT ENGINE ----------------
    def scout_report(self, avg_m, avg_p, events):

        involvement = min(100, len(events) * 2)
        intensity = min(100, avg_m * 12)
        structure = min(100, avg_p * 10)

        rating = round((involvement + intensity + structure) / 3, 1)

        role = "CM"
        if avg_m > 7:
            role = "ATTACKING MID / WINGER"
        elif avg_p < 6:
            role = "DEFENSIVE MID / CB"
        elif avg_m > 6 and avg_p > 7:
            role = "BOX-TO-BOX MID"

        strengths = []
        weaknesses = []
        improvements = []

        if avg_m > 6:
            strengths.append("High involvement in play")
        else:
            weaknesses.append("Low attacking contribution")
            improvements.append("Increase movement and attacking transitions")

        if avg_p > 8:
            strengths.append("Strong positional structure")
        else:
            weaknesses.append("Poor spacing and organisation")
            improvements.append("Improve positioning discipline")

        if len(events) > 40:
            strengths.append("High match impact")
        else:
            improvements.append("Increase off-ball involvement")

        improvements += [
            "Scan before receiving the ball",
            "Improve first-touch under pressure",
            "Work on transition speed",
            "Study elite midfield movement patterns"
        ]

        return {
            "rating": rating,
            "role": role,
            "strengths": strengths[:3],
            "weaknesses": weaknesses[:3],
            "improvements": improvements[:5]
        }

    # ---------------- MAIN ANALYSIS ----------------
    def analyse(self, progress=None, status=None):

        cap = cv2.VideoCapture(self.path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_id = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_id += 1

            if frame_id % 2 != 0:
                continue

            frame = cv2.resize(frame, (320, 180))

            m = self.motion(frame)
            p = self.players(frame)

            self.motion_buf.append(m)
            self.player_buf.append(p)

            # EVENTS
            self.events.extend(self.detect_events(frame_id, m, p))

            # MOMENTUM
            if len(self.motion_buf) > 20:
                self.momentum.append(np.mean(self.motion_buf))

            # UI UPDATES
            if progress:
                progress.progress(frame_id / total)

            if status:
                status.text(f"Analyzing frame {frame_id}/{total}")

        cap.release()

        avg_m = float(np.mean(self.motion_buf))
        avg_p = float(np.mean(self.player_buf))

        pressure = avg_m * avg_p
        chaos = avg_m * (10 - abs(avg_p - 7))

        scout = self.scout_report(avg_m, avg_p, self.events)

        return {
            "frames": frame_id,
            "avg_motion": avg_m,
            "avg_players": avg_p,

            "events": self.events,
            "momentum": self.momentum,

            "pressure_index": round(pressure, 2),
            "chaos_index": round(chaos, 2),

            "tactical_score": round(min(10, avg_m * 2.2 + avg_p * 0.4), 1),

            "team_style": self.team_style(avg_m, avg_p),

            "scout_report": scout
        }