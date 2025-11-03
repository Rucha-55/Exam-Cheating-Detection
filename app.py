"""
Exam Cheating Detection System - Flask Backend
Uses computer vision to detect cheating indicators in real-time
"""

from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import torch
import mediapipe as mp
from threading import Lock
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

# Global variables for video streaming
camera_lock = Lock()
current_frame = None
detection_results = {
    'cheating_score': 0,
    'indicators': [],
    'timestamp': None,
    'warning_level': 'safe'
}

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection
mp_hands = mp.solutions.hands

# Load your trained model (replace with your actual model path)
try:
    model = torch.load('cheating_model_best.pt', map_location=torch.device('cpu'))
    model.eval()
    MODEL_LOADED = True
except:
    MODEL_LOADED = False
    print("Warning: Model not loaded. Using detection fallback.")


def generate_frames():
    """Generate frames from webcam for streaming"""
    global current_frame, detection_results
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True
    ) as pose, mp_face_detection.FaceDetection() as face_detection, \
        mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1
        ) as hands:
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Convert to RGB for MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Pose detection
            pose_results = pose.process(frame_rgb)
            
            # Face detection
            face_results = face_detection.process(frame_rgb)
            
            # Hand detection
            hand_results = hands.process(frame_rgb)
            
            # Analyze for cheating indicators
            cheating_score, indicators = analyze_cheating_indicators(
                frame, pose_results, face_results, hand_results, h, w
            )
            
            # Determine warning level
            if cheating_score > 0.7:
                warning_level = 'critical'
                color = (0, 0, 255)  # Red
            elif cheating_score > 0.4:
                warning_level = 'warning'
                color = (0, 165, 255)  # Orange
            else:
                warning_level = 'safe'
                color = (0, 255, 0)  # Green
            
            # Draw indicators on frame
            frame = draw_indicators(frame, pose_results, face_results, hand_results, color, h, w)
            
            # Add score overlay
            cv2.rectangle(frame, (10, 10), (300, 80), (0, 0, 0), -1)
            cv2.putText(frame, f'Cheating Score: {cheating_score:.2f}', (20, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f'Status: {warning_level.upper()}', (20, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Update global results
            detection_results = {
                'cheating_score': float(cheating_score),
                'indicators': indicators,
                'timestamp': datetime.now().isoformat(),
                'warning_level': warning_level
            }
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()


def analyze_cheating_indicators(frame, pose_results, face_results, hand_results, h, w):
    """
    Analyze various indicators of cheating
    Returns: (cheating_score: float 0-1, indicators: list)
    """
    indicators = []
    cheating_score = 0.0
    
    # 1. Head posture analysis
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        
        # Get head keypoints
        head_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x
        head_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
        head_conf = landmarks[mp_pose.PoseLandmark.NOSE.value].visibility
        
        # Check if head is tilted/looking away
        left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE.value]
        right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value]
        
        eye_angle = abs(left_eye.y - right_eye.y)
        if eye_angle > 0.05:  # Tilted head
            indicators.append("Head tilt detected")
            cheating_score += 0.15
        
        # Check if looking down/away
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        if nose.y > 0.6:  # Looking down significantly
            indicators.append("Looking down/away")
            cheating_score += 0.20
        
        # 2. Posture analysis
        shoulder_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        shoulder_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        shoulder_diff = abs(shoulder_left.y - shoulder_right.y)
        if shoulder_diff > 0.1:  # Hunched/leaning
            indicators.append("Abnormal posture")
            cheating_score += 0.15
        
        # 3. Hand visibility and position
        if hand_results.multi_hand_landmarks:
            num_hands = len(hand_results.multi_hand_landmarks)
            if num_hands > 0:
                indicators.append(f"Hands visible ({num_hands})")
                cheating_score += 0.10 * num_hands
    
    # 4. Face detection - multiple faces in frame
    if face_results.detections:
        num_faces = len(face_results.detections)
        if num_faces > 1:
            indicators.append(f"Multiple people detected ({num_faces})")
            cheating_score += 0.25
    
    # Normalize score to 0-1
    cheating_score = min(cheating_score, 1.0)
    
    return cheating_score, indicators


def draw_indicators(frame, pose_results, face_results, hand_results, color, h, w):
    """Draw detected landmarks and indicators on frame"""
    
    # Draw pose landmarks
    if pose_results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )
    
    # Draw hand landmarks
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style()
            )
    
    # Draw face detections
    if face_results.detections:
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            x_min = int(bboxC.xmin * w)
            y_min = int(bboxC.ymin * h)
            width = int(bboxC.width * w)
            height = int(bboxC.height * h)
            
            cv2.rectangle(frame, (x_min, y_min), (x_min + width, y_min + height), color, 2)
    
    return frame


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/camera')
def camera():
    """Camera detection page"""
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming endpoint"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/get_results')
def get_results():
    """Get current detection results"""
    return jsonify(detection_results)


@app.route('/api/results', methods=['POST'])
def save_results():
    """Save detection results"""
    data = request.get_json()
    
    # Save to results file
    with open('detection_results.json', 'a') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f)
        f.write('\n')
    
    return jsonify({'status': 'saved'})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': MODEL_LOADED,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
