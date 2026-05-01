# Wrapper simple autour de MediaPipe Pose
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

LANDMARKS = {
    "nose": 0,
    "left_shoulder": 11, "right_shoulder": 12,
    "left_elbow": 13, "right_elbow": 14,
    "left_wrist": 15, "right_wrist": 16,
    "left_hip": 23, "right_hip": 24,
    "left_knee": 25, "right_knee": 26,
    "left_ankle": 27, "right_ankle": 28,
}

class PoseDetector:
    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1,
        )
        self.result = None

    def process(self, frame):
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(rgb)

        if not self.result.pose_landmarks:
            return None

        points = {}
        for name, idx in LANDMARKS.items():
            lm = self.result.pose_landmarks.landmark[idx]
            points[name] = (int(lm.x * w), int(lm.y * h))
        return points

    def draw(self, frame):
        if self.result and self.result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                self.result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style(),
            )

    def close(self):
        self.pose.close()
