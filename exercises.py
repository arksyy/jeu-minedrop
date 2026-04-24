"""Detecteurs d'exercices bases sur des regles geometriques + state machines."""
from dataclasses import dataclass
from typing import Optional

from geometry import angle_deg, distance
from pose import Landmarks


@dataclass
class ExerciseState:
    reps: int
    phase: str
    feedback: str


class ExerciseDetector:
    name: str = "exercise"
    instruction: str = ""

    def __init__(self, target_reps: int = 5):
        self.target_reps = target_reps
        self.reps = 0
        self.phase = "ready"
        self.feedback = ""

    def is_done(self) -> bool:
        return self.reps >= self.target_reps

    def reset(self) -> None:
        self.reps = 0
        self.phase = "ready"
        self.feedback = ""

    def update(self, lm: Optional[Landmarks]) -> ExerciseState:
        if lm is None:
            self.feedback = "Place-toi devant la camera"
            return ExerciseState(self.reps, self.phase, self.feedback)
        self._update(lm)
        return ExerciseState(self.reps, self.phase, self.feedback)

    def _update(self, lm: Landmarks) -> None:
        raise NotImplementedError


def _shoulder_width(lm: Landmarks) -> float:
    return distance(lm["left_shoulder"], lm["right_shoulder"])


def _midpoint(a, b):
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


class JumpingJackDetector(ExerciseDetector):
    name = "Jumping Jack"
    instruction = "Fais des jumping jacks"

    def _update(self, lm: Landmarks) -> None:
        sw = _shoulder_width(lm)
        if sw < 1e-3:
            return
        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lw, rw = lm["left_wrist"], lm["right_wrist"]
        la, ra = lm["left_ankle"], lm["right_ankle"]
        lh, rh = lm["left_hip"], lm["right_hip"]

        arms_up = (lw[1] < ls[1] - sw * 0.3) and (rw[1] < rs[1] - sw * 0.3)
        arms_down = (lw[1] > ls[1] + sw * 0.2) and (rw[1] > rs[1] + sw * 0.2)

        ankle_spread = distance(la, ra)
        hip_spread = distance(lh, rh)
        legs_apart = ankle_spread > hip_spread * 1.6
        legs_together = ankle_spread < hip_spread * 1.2

        if self.phase == "ready":
            if arms_down and legs_together:
                self.phase = "down"
                self.feedback = "Saute bras en l'air!"
        elif self.phase == "down":
            if arms_up and legs_apart:
                self.phase = "up"
                self.feedback = "Et on redescend..."
        elif self.phase == "up":
            if arms_down and legs_together:
                self.phase = "down"
                self.reps += 1
                self.feedback = f"Rep #{self.reps}!"


class ShadowboxingDetector(ExerciseDetector):
    name = "Shadowboxing"
    instruction = "Lance des coups de poing (shadowboxing)"

    def __init__(self, target_reps: int = 5):
        super().__init__(target_reps)
        self._arm_state = {"left": "bent", "right": "bent"}

    def _update(self, lm: Landmarks) -> None:
        sw = _shoulder_width(lm)
        if sw < 1e-3:
            return
        sides = [
            ("left", lm["left_shoulder"], lm["left_elbow"], lm["left_wrist"]),
            ("right", lm["right_shoulder"], lm["right_elbow"], lm["right_wrist"]),
        ]
        punched = False
        for side, s, e, w in sides:
            ang = angle_deg(s, e, w)
            cur = self._arm_state[side]
            if cur == "bent" and ang > 155:
                self._arm_state[side] = "extended"
                self.reps += 1
                punched = True
            elif cur == "extended" and ang < 110:
                self._arm_state[side] = "bent"
        if self.phase == "ready":
            self.phase = "active"
            self.feedback = "Mets-toi en garde et cogne!"
        if punched:
            self.feedback = f"Punch! Rep #{self.reps}"


class SixSevenDetector(ExerciseDetector):
    """Le tweak '6-7': les deux mains levees au-dessus des epaules.
    Rep = cycle mains en bas -> mains en l'air -> mains en bas.
    """
    name = "6-7"
    instruction = "Leve les deux mains (6-7!)"

    def _update(self, lm: Landmarks) -> None:
        sw = _shoulder_width(lm)
        if sw < 1e-3:
            return
        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lw, rw = lm["left_wrist"], lm["right_wrist"]

        hands_up = (lw[1] < ls[1] - sw * 0.1) and (rw[1] < rs[1] - sw * 0.1)
        hands_down = (lw[1] > ls[1] + sw * 0.2) and (rw[1] > rs[1] + sw * 0.2)

        if self.phase == "ready":
            if hands_up:
                self.phase = "up"
                self.feedback = "Redescend les mains..."
            elif hands_down:
                self.phase = "down"
                self.feedback = "Leve les mains!"
        elif self.phase == "down":
            if hands_up:
                self.phase = "up"
                self.feedback = "...seveeen!"
        elif self.phase == "up":
            if hands_down:
                self.phase = "down"
                self.reps += 1
                self.feedback = f"6-7 #{self.reps}!"


class PushUpDetector(ExerciseDetector):
    name = "Push-up"
    instruction = "Fais des push-ups (de cote pour que la camera voie)"

    def _update(self, lm: Landmarks) -> None:
        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lh, rh = lm["left_hip"], lm["right_hip"]
        le, lw = lm["left_elbow"], lm["left_wrist"]
        re, rw = lm["right_elbow"], lm["right_wrist"]

        shoulder_mid = _midpoint(ls, rs)
        hip_mid = _midpoint(lh, rh)

        dx = abs(shoulder_mid[0] - hip_mid[0])
        dy = abs(shoulder_mid[1] - hip_mid[1])
        horizontal = dx > dy * 0.8

        if not horizontal:
            self.feedback = "Mets-toi en planche, de cote"
            return

        left_ang = angle_deg(ls, le, lw)
        right_ang = angle_deg(rs, re, rw)
        elbow_ang = min(left_ang, right_ang)

        if self.phase == "ready":
            if elbow_ang > 155:
                self.phase = "up"
                self.feedback = "Descends!"
        elif self.phase == "up":
            if elbow_ang < 100:
                self.phase = "down"
                self.feedback = "Pousse!"
        elif self.phase == "down":
            if elbow_ang > 155:
                self.phase = "up"
                self.reps += 1
                self.feedback = f"Rep #{self.reps}!"
