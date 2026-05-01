import time
import cv2

from pose import PoseDetector
from exercises import SixSeven, JumpingJack, Shadowboxing, PushUp

TARGET_REPS = 5
DONE_HOLD = 2.0  
WINDOW = "Veille techno - Coach MediaPipe"
FONT = cv2.FONT_HERSHEY_SIMPLEX


def put_text(frame, text, pos, scale=0.7, color=(255, 255, 255), thick=2):
    cv2.putText(frame, text, pos, FONT, scale, (0, 0, 0), thick + 2, cv2.LINE_AA)
    cv2.putText(frame, text, pos, FONT, scale, color, thick, cv2.LINE_AA)


def draw_ui(frame, ex, is_done):
    h, w = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 110), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    put_text(frame, ex.name, (15, 35), 0.9, (0, 255, 255))
    put_text(frame, ex.instruction, (15, 65), 0.6)
    put_text(frame, f"Reps: {ex.reps} / {ex.target}", (15, 95), 0.7, (0, 255, 0))
    put_text(frame, f"[{ex.phase}]", (w - 160, 35), 0.7, (200, 200, 255))

    if ex.feedback:
        put_text(frame, ex.feedback, (15, h - 20), 0.7, (255, 200, 0))

    if is_done:
        cv2.rectangle(frame, (0, h // 2 - 60), (w, h // 2 + 60), (0, 128, 0), -1)
        put_text(frame, "Bien joue!", (w // 2 - 110, h // 2 + 10),
                 1.6, (255, 255, 255), 3)

    put_text(frame, "q = quitter | space = passer",
             (w - 320, h - 20), 0.5, (200, 200, 200), 1)


def show_end_screen(cap):
    for _ in range(60):
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, 0), (w, h), (0, 80, 0), -1)
        cv2.putText(frame, "Seance terminee!",
                    (w // 2 - 260, h // 2),
                    FONT, 1.8, (255, 255, 255), 4, cv2.LINE_AA)
        cv2.imshow(WINDOW, frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur: impossible d'ouvrir la camera")
        return

    pose = PoseDetector()
    exercises = [
        SixSeven(TARGET_REPS),
        JumpingJack(TARGET_REPS),
        Shadowboxing(TARGET_REPS),
        PushUp(TARGET_REPS),
    ]

    i = 0
    done_at = None

    try:
        while i < len(exercises):
            ok, frame = cap.read()
            if not ok:
                print("Frame vide, on arrete")
                break

            frame = cv2.flip(frame, 1) 

            lm = pose.process(frame)
            pose.draw(frame)

            ex = exercises[i]
            ex.update(lm)
            is_done = ex.done()

            draw_ui(frame, ex, is_done)
            cv2.imshow(WINDOW, frame)

            if is_done:
                if done_at is None:
                    done_at = time.time()
                elif time.time() - done_at >= DONE_HOLD:
                    i += 1
                    done_at = None

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  
                break
            if key == ord(' '):  
                i += 1
                done_at = None

        if i >= len(exercises):
            show_end_screen(cap)
    finally:
        pose.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
