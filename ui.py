"""Overlay: dessine instructions + compteur de reps par-dessus la frame."""
import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX


def _put_text(frame, text, org, scale=0.7, color=(255, 255, 255), thickness=2):
    cv2.putText(frame, text, org, FONT, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, org, FONT, scale, color, thickness, cv2.LINE_AA)


def draw_overlay(frame,
                 exercise_name: str,
                 instruction: str,
                 reps: int,
                 target: int,
                 phase: str,
                 feedback: str,
                 done: bool = False) -> None:
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 110), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    _put_text(frame, exercise_name, (15, 35), scale=0.9, color=(0, 255, 255))
    _put_text(frame, instruction, (15, 65), scale=0.6, color=(255, 255, 255))
    _put_text(frame, f"Reps: {reps} / {target}", (15, 95),
              scale=0.7, color=(0, 255, 0))

    _put_text(frame, f"[{phase}]", (w - 160, 35), scale=0.7, color=(200, 200, 255))

    if feedback:
        _put_text(frame, feedback, (15, h - 20), scale=0.7, color=(255, 200, 0))

    if done:
        cv2.rectangle(frame, (0, h // 2 - 60), (w, h // 2 + 60), (0, 128, 0), -1)
        _put_text(frame, "Bien joue!", (w // 2 - 110, h // 2 + 10),
                  scale=1.6, color=(255, 255, 255), thickness=3)

    _put_text(frame, "q = quitter | space = passer",
              (w - 320, h - 20), scale=0.5, color=(200, 200, 200), thickness=1)
