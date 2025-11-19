from fastapi import FastAPI, WebSocket
import cv2
import mediapipe as mp
import asyncio
from datetime import datetime

app = FastAPI()

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1,
    min_detection_confidence=0.5
)

def log_event(event: str):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {event}\n")


@app.get("/")
def home():
    return {"status": "running"}


@app.websocket("/ws/detect")
async def detect(ws: WebSocket):
    await ws.accept()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        await ws.send_json({"event": "camera_error"})
        log_event("camera_error")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            await ws.send_json({"event": "no_frame"})
            log_event("no_frame")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_face_mesh.process(frame_rgb)

        if not results.multi_face_landmarks:
            await ws.send_json({"event": "no_face"})
            log_event("no_face")
        else:
            face = results.multi_face_landmarks[0]
            
            left_eye = face.landmark[33]
            right_eye = face.landmark[263]
            nose = face.landmark[1]

            # Check face direction (looking left/right)
            if nose.x < left_eye.x - 0.02:
                event = "looking_right"
            elif nose.x > right_eye.x + 0.02:
                event = "looking_left"
            else:
                event = "focused"

            await ws.send_json({"event": event})
            log_event(event)

        await asyncio.sleep(0.2)
