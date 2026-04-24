"""Point d'entree: cycle les 3 exercices en parlant a l'utilisateur."""
import sys
import time

import cv2

from exercises import (
    JumpingJackDetector,
    ShadowboxingDetector,
    PushUpDetector,
    SixSevenDetector,
)
from pose import PoseDetector
from ui import draw_overlay

TARGET_REPS = 5
DONE_HOLD_SEC = 2.0
WINDOW_TITLE = "Veille techno - Coach MediaPipe"


def build_sequence():
    return [
        SixSevenDetector(target_reps=TARGET_REPS),
        JumpingJackDetector(target_reps=TARGET_REPS),
        ShadowboxingDetector(target_reps=TARGET_REPS),
        PushUpDetector(target_reps=TARGET_REPS),
    ]


def main() -> int:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur: impossible d'ouvrir la camera (index 0).", file=sys.stderr)
        return 1

    pose = PoseDetector()
    sequence = build_sequence()
    idx = 0
    done_at = None

    try:
        while idx < len(sequence):
            ok, frame = cap.read()
            if not ok:
                print("Erreur: frame vide.", file=sys.stderr)
                break

            frame = cv2.flip(frame, 1)
            landmarks = pose.process(frame)
            pose.draw(frame)

            current = sequence[idx]
            state = current.update(landmarks)
            done = current.is_done()

            draw_overlay(
                frame,
                exercise_name=current.name,
                instruction=current.instruction,
                reps=state.reps,
                target=current.target_reps,
                phase=state.phase,
                feedback=state.feedback,
                done=done,
            )

            cv2.imshow(WINDOW_TITLE, frame)

            if done:
                if done_at is None:
                    done_at = time.time()
                elif time.time() - done_at >= DONE_HOLD_SEC:
                    idx += 1
                    done_at = None

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            if key == ord(' '):
                idx += 1
                done_at = None

        if idx >= len(sequence):
            for _ in range(60):
                ok, frame = cap.read()
                if not ok:
                    break
                frame = cv2.flip(frame, 1)
                h, w = frame.shape[:2]
                cv2.rectangle(frame, (0, 0), (w, h), (0, 80, 0), -1)
                cv2.putText(frame, "Seance terminee!",
                            (w // 2 - 260, h // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255),
                            4, cv2.LINE_AA)
                cv2.imshow(WINDOW_TITLE, frame)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
    finally:
        pose.close()
        cap.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
