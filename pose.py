"""Wrapper MediaPipe Pose: conversion landmarks -> dict de pixels."""
from typing import Dict, Optional, Tuple

import cv2
import mediapipe as mp

Point = Tuple[int, int]
Landmarks = Dict[str, Point]

_mp_pose = mp.solutions.pose
_mp_drawing = mp.solutions.drawing_utils
_mp_styles = mp.solutions.drawing_styles

LANDMARK_NAMES = {
    "nose": 0,
    "left_shoulder": 11, "right_shoulder": 12,
    "left_elbow": 13, "right_elbow": 14,
    "left_wrist": 15, "right_wrist": 16,
    "left_hip": 23, "right_hip": 24,
    "left_knee": 25, "right_knee": 26,
    "left_ankle": 27, "right_ankle": 28,
}


class PoseDetector:
    def __init__(self,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5,
                 model_complexity: int = 1):
        self._pose = _mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=model_complexity,
            enable_segmentation=False,
        )
        self._last_result = None

    def process(self, frame_bgr) -> Optional[Landmarks]:
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = self._pose.process(rgb)
        self._last_result = result
        if not result.pose_landmarks:
            return None
        lms = result.pose_landmarks.landmark
        out: Landmarks = {}
        for name, idx in LANDMARK_NAMES.items():
            lm = lms[idx]
            out[name] = (int(lm.x * w), int(lm.y * h))
        return out

    def draw(self, frame_bgr) -> None:
        if self._last_result and self._last_result.pose_landmarks:
            _mp_drawing.draw_landmarks(
                frame_bgr,
                self._last_result.pose_landmarks,
                _mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=_mp_styles.get_default_pose_landmarks_style(),
            )

    def close(self) -> None:
        self._pose.close()
