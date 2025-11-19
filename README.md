Distraction Detection - MVP Backend



Project Description

This MVP detects distraction from a live camera feed using OpenCV + YOLO.
It sends events such as:

focused

not_focused

distracted

no_face_detected

and also logs them with timestamps.





Tech Stack

FastAPI

WebSockets

OpenCV

YOLO

Python





How to Run
1. Install dependencies
pip install -r requirements.txt

2. Start the server
uvicorn backend.main:app --reload

3. Websocket URL
ws://127.0.0.1:8000/ws/detect





Connect using:

OBS virtual camera

WebSocketKing

Custom frontend

Output

Each frame sends JSON:

{
  "status": "focused",
  "timestamp": "YYYY-MM-DD HH:MM:SS"