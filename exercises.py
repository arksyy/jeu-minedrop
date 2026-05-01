import math



def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_deg(a, b, c):
    ax, ay = a[0] - b[0], a[1] - b[1]
    cx, cy = c[0] - b[0], c[1] - b[1]
    dot = ax * cx + ay * cy
    mag = math.hypot(ax, ay) * math.hypot(cx, cy)
    if mag == 0:
        return 0
    cos_t = max(-1, min(1, dot / mag))
    return math.degrees(math.acos(cos_t))



class Exercise:
    name = ""
    instruction = ""

    def __init__(self, target=5):
        self.target = target
        self.reps = 0
        self.phase = "ready"
        self.feedback = ""

    def done(self):
        return self.reps >= self.target



class JumpingJack(Exercise):
    name = "Jumping Jack"
    instruction = "Fais des jumping jacks"

    def update(self, lm):
        if lm is None:
            self.feedback = "Place-toi devant la camera"
            return

        sw = distance(lm["left_shoulder"], lm["right_shoulder"])
        if sw < 1:
            return

        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lw, rw = lm["left_wrist"], lm["right_wrist"]
        la, ra = lm["left_ankle"], lm["right_ankle"]
        lh, rh = lm["left_hip"], lm["right_hip"]

        
        arms_up = lw[1] < ls[1] - sw * 0.3 and rw[1] < rs[1] - sw * 0.3
        arms_down = lw[1] > ls[1] + sw * 0.2 and rw[1] > rs[1] + sw * 0.2

        
        ankle_gap = distance(la, ra)
        hip_gap = distance(lh, rh)
        legs_apart = ankle_gap > hip_gap * 1.6
        legs_together = ankle_gap < hip_gap * 1.2

        if self.phase == "ready" and arms_down and legs_together:
            self.phase = "down"
            self.feedback = "Saute bras en l'air!"
        elif self.phase == "down" and arms_up and legs_apart:
            self.phase = "up"
            self.feedback = "Et on redescend..."
        elif self.phase == "up" and arms_down and legs_together:
            self.phase = "down"
            self.reps += 1
            self.feedback = f"Rep #{self.reps}!"


class Shadowboxing(Exercise):
    name = "Shadowboxing"
    instruction = "Lance des coups de poing"

    def __init__(self, target=5):
        super().__init__(target)
        self.left_arm = "bent"
        self.right_arm = "bent"

    def update(self, lm):
        if lm is None:
            self.feedback = "Place-toi devant la camera"
            return

        if self.phase == "ready":
            self.phase = "active"
            self.feedback = "Mets-toi en garde et cogne!"

        ang_l = angle_deg(lm["left_shoulder"], lm["left_elbow"], lm["left_wrist"])
        if self.left_arm == "bent" and ang_l > 155:
            self.left_arm = "extended"
            self.reps += 1
            self.feedback = f"Punch! Rep #{self.reps}"
        elif self.left_arm == "extended" and ang_l < 110:
            self.left_arm = "bent"

        # Bras droit
        ang_r = angle_deg(lm["right_shoulder"], lm["right_elbow"], lm["right_wrist"])
        if self.right_arm == "bent" and ang_r > 155:
            self.right_arm = "extended"
            self.reps += 1
            self.feedback = f"Punch! Rep #{self.reps}"
        elif self.right_arm == "extended" and ang_r < 110:
            self.right_arm = "bent"


class SixSeven(Exercise):
    name = "6-7"
    instruction = "Leve les deux mains (6-7!)"

    def update(self, lm):
        if lm is None:
            self.feedback = "Place-toi devant la camera"
            return

        sw = distance(lm["left_shoulder"], lm["right_shoulder"])
        if sw < 1:
            return

        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lw, rw = lm["left_wrist"], lm["right_wrist"]

        hands_up = lw[1] < ls[1] - sw * 0.1 and rw[1] < rs[1] - sw * 0.1
        hands_down = lw[1] > ls[1] + sw * 0.2 and rw[1] > rs[1] + sw * 0.2

        if self.phase == "ready":
            if hands_up:
                self.phase = "up"
                self.feedback = "Redescend les mains..."
            elif hands_down:
                self.phase = "down"
                self.feedback = "Leve les mains!"
        elif self.phase == "down" and hands_up:
            self.phase = "up"
            self.feedback = "...seveeen!"
        elif self.phase == "up" and hands_down:
            self.phase = "down"
            self.reps += 1
            self.feedback = f"6-7 #{self.reps}!"


class PushUp(Exercise):
    name = "Push-up"
    instruction = "Fais des push-ups (de cote pour la camera)"

    def update(self, lm):
        if lm is None:
            self.feedback = "Place-toi devant la camera"
            return

        ls, rs = lm["left_shoulder"], lm["right_shoulder"]
        lh, rh = lm["left_hip"], lm["right_hip"]

        sx = (ls[0] + rs[0]) / 2
        sy = (ls[1] + rs[1]) / 2
        hx = (lh[0] + rh[0]) / 2
        hy = (lh[1] + rh[1]) / 2
        if abs(sx - hx) <= abs(sy - hy) * 0.8:
            self.feedback = "Mets-toi en planche, de cote"
            return

        ang_l = angle_deg(ls, lm["left_elbow"], lm["left_wrist"])
        ang_r = angle_deg(rs, lm["right_elbow"], lm["right_wrist"])
        elbow = min(ang_l, ang_r)

        if self.phase == "ready" and elbow > 155:
            self.phase = "up"
            self.feedback = "Descends!"
        elif self.phase == "up" and elbow < 100:
            self.phase = "down"
            self.feedback = "Pousse!"
        elif self.phase == "down" and elbow > 155:
            self.phase = "up"
            self.reps += 1
            self.feedback = f"Rep #{self.reps}!"
