import os

# Setup Virtual Display for Render
if "RENDER" in os.environ:  # Only set in Render environment
    os.system("Xvfb :99 -screen 0 1280x720x16 &")  # Start Xvfb
    os.environ["DISPLAY"] = ":99"  # Set DISPLAY variable

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import logging
import atexit
from flask import Flask, Response, render_template

# Initialize Flask app
app = Flask(__name__)

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Setup Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    logging.error("⚠️ Camera failed to initialize. Check camera permissions!")

# Setup Mediapipe Hand Detector
hand_detector = mp.solutions.hands.Hands(
    static_image_mode=False, 
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
drawing_utils = mp.solutions.drawing_utils

# Get Screen Size
screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0
smooth_factor = 0.3  # Adjust for smooth movement
index_x, index_y = 0, 0  # Initialize variables

def generate_frames():
    global index_x, index_y, prev_x, prev_y

    while True:
        success, frame = cap.read()
        if not success:
            logging.warning("⚠️ Failed to capture video frame.")
            break

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = hand.landmark

                thumb_x, thumb_y, middle_y = 0, 0, 0  # Initialize
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    if id == 8:  # Index Finger
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        index_x = screen_width / frame_width * x
                        index_y = screen_height / frame_height * y

                        # Smooth Movement
                        smooth_x = prev_x * (1 - smooth_factor) + index_x * smooth_factor
                        smooth_y = prev_y * (1 - smooth_factor) + index_y * smooth_factor
                        pyautogui.moveTo(smooth_x, smooth_y)
                        prev_x, prev_y = smooth_x, smooth_y

                    if id == 4:  # Thumb
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width / frame_width * x
                        thumb_y = screen_height / frame_height * y

                    if id == 12:  # Middle Finger
                        middle_y = screen_height / frame_height * y

                # Left Click (Pinch Index + Thumb)
                if abs(index_x - thumb_x) < 40 and abs(index_y - thumb_y) < 40:
                    logging.info("🖱️ Left Click Triggered")
                    pyautogui.click()
                    pyautogui.sleep(0.3)

                # Right Click (Pinch Index + Thumb + Middle)
                if abs(index_x - thumb_x) < 40 and abs(index_y - thumb_y) < 40 and abs(middle_y - index_y) < 40:
                    logging.info("🖱️ Right Click Triggered")
                    pyautogui.rightClick()
                    pyautogui.sleep(0.3)

                # Double Click (Close Fingers Together)
                if abs(index_x - thumb_x) < 30 and abs(index_y - thumb_y) < 30 and abs(middle_y - index_y) < 30:
                    logging.info("🖱️ Double Click Triggered")
                    pyautogui.doubleClick()
                    pyautogui.sleep(0.5)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Release resources on exit
def cleanup():
    cap.release()
    cv2.destroyAllWindows()
    logging.info("📌 Camera & resources released.")

atexit.register(cleanup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use port 10000 or the one set by Render
    app.run(host='0.0.0.0', port=port, debug=True)
