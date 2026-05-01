import json
import os
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2

from pose import PoseDetector
from exercises import SixSeven, JumpingJack, Shadowboxing, PushUp

TARGET_REPS = 5
DONE_HOLD = 2.0
FONT = cv2.FONT_HERSHEY_SIMPLEX
BACKEND_URL = os.environ.get("MINEDROP_BACKEND", "http://localhost:8000").rstrip("/") + "/motion"
CAM_INDEX = int(os.environ.get("MINEDROP_CAM", "0"))
MJPEG_PORT = int(os.environ.get("MINEDROP_MJPEG_PORT", "8001"))
SESSION_REWARD = 67

_latest_jpeg: bytes | None = None
_jpeg_lock = threading.Lock()

_session_active = False
_session_lock = threading.Lock()


def publish_frame(frame) -> None:
    global _latest_jpeg
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    if not ok:
        return
    with _jpeg_lock:
        _latest_jpeg = buf.tobytes()


def request_start() -> bool:
    global _session_active
    with _session_lock:
        if _session_active:
            return False
        _session_active = True
        return True


def is_session_active() -> bool:
    with _session_lock:
        return _session_active


def end_session() -> None:
    global _session_active
    with _session_lock:
        _session_active = False


def _send_json(handler: BaseHTTPRequestHandler, status: int, body: dict) -> None:
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


class MjpegHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # quiet access log
        return

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/start":
            ok = request_start()
            _send_json(self, 200 if ok else 409, {"ok": ok, "active": is_session_active()})
            return
        if path == "/reset":
            end_session()
            _send_json(self, 200, {"ok": True, "active": False})
            return
        if path == "/status":
            _send_json(self, 200, {"active": is_session_active()})
            return
        if path != "/video":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, private")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.end_headers()
        try:
            while True:
                with _jpeg_lock:
                    data = _latest_jpeg
                if data is None:
                    time.sleep(0.05)
                    continue
                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(data)}\r\n\r\n".encode())
                self.wfile.write(data)
                self.wfile.write(b"\r\n")
                time.sleep(1 / 30)
        except (BrokenPipeError, ConnectionResetError):
            pass


def start_mjpeg_server(port: int = MJPEG_PORT) -> None:
    server = ThreadingHTTPServer(("0.0.0.0", port), MjpegHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Coach pret sur http://localhost:{port}  (video=/video, start=/start)")


def _post_motion(payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BACKEND_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=1).close()
    except (urllib.error.URLError, TimeoutError, OSError):
        pass


def notify_session_complete():
    payload = {"event": "session_complete", "tokens": SESSION_REWARD}
    threading.Thread(target=_post_motion, args=(payload,), daemon=True).start()


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


def draw_idle_ui(frame):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 110), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    put_text(frame, "En attente...", (15, 45), 1.0, (0, 255, 255))
    put_text(frame, "Demarre une seance depuis la page Tokens", (15, 85), 0.6)


def fresh_exercises():
    return [
        SixSeven(TARGET_REPS),
        JumpingJack(TARGET_REPS),
        Shadowboxing(TARGET_REPS),
        PushUp(TARGET_REPS),
    ]


def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print(f"Erreur: impossible d'ouvrir la camera (index={CAM_INDEX})")
        return

    start_mjpeg_server()
    pose = PoseDetector()
    exercises = fresh_exercises()

    i = 0
    done_at = None
    empty_streak = 0
    MAX_EMPTY_STREAK = 60
    was_active = False

    try:
        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                empty_streak += 1
                if empty_streak >= MAX_EMPTY_STREAK:
                    print("Camera ne renvoie plus de frames, on arrete")
                    break
                time.sleep(0.01)
                continue
            empty_streak = 0

            frame = cv2.flip(frame, 1)
            lm = pose.process(frame)
            pose.draw(frame)

            active = is_session_active()
            if active and not was_active:
                exercises = fresh_exercises()
                i = 0
                done_at = None
            was_active = active

            if active and i < len(exercises):
                ex = exercises[i]
                ex.update(lm)
                is_done = ex.done()
                draw_ui(frame, ex, is_done)

                if is_done:
                    if done_at is None:
                        done_at = time.time()
                    elif time.time() - done_at >= DONE_HOLD:
                        i += 1
                        done_at = None
            else:
                draw_idle_ui(frame)

            if active and i >= len(exercises):
                notify_session_complete()
                end_session()
                exercises = fresh_exercises()
                i = 0
                done_at = None
                was_active = False

            publish_frame(frame)
    except KeyboardInterrupt:
        pass
    finally:
        pose.close()
        cap.release()


if __name__ == "__main__":
    main()
