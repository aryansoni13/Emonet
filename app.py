from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import base64
import json
import os
from datetime import datetime
from collections import deque

app = Flask(__name__)

class WebEmotionAvatar:
    def __init__(self):
        # Mediapipe setup
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False, 
            max_num_faces=1, 
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.LIPS = self.mp_face_mesh.FACEMESH_LIPS
        self.LEFT_IRIS = [468, 469, 470, 471]
        self.RIGHT_IRIS = [473, 474, 475, 476]
        
        # Emotion settings
        self.emotions = {
            "happy": {"emoji": "😊", "color": "#00FF00", "description": "Joyful and cheerful"},
            "sad": {"emoji": "😢", "color": "#FF0000", "description": "Down and melancholic"},
            "angry": {"emoji": "😠", "color": "#0000FF", "description": "Frustrated and upset"},
            "surprise": {"emoji": "😲", "color": "#00FFFF", "description": "Shocked and amazed"},
            "neutral": {"emoji": "😐", "color": "#FFFFFF", "description": "Calm and composed"},
            "fear": {"emoji": "😨", "color": "#FF8C00", "description": "Scared and anxious"},
            "disgust": {"emoji": "🤢", "color": "#8A2BE2", "description": "Repulsed and disturbed"}
        }
        
        # Tracking
        self.emotion_history = deque(maxlen=30)
        self.current_emotion = "neutral"
        self.emotion_confidence = 0.0

    def distance(self, p1, p2):
        return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

    def get_emotion_features(self, landmarks):
        """Extract enhanced emotion features"""
        top_lip = landmarks[13]
        bottom_lip = landmarks[14]
        left_mouth = landmarks[61]
        right_mouth = landmarks[291]
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        left_eyebrow = landmarks[70]
        right_eyebrow = landmarks[300]
        
        face_width = self.distance(landmarks[234], landmarks[454])
        
        features = {
            'mouth_open': self.distance(top_lip, bottom_lip) / face_width,
            'mouth_stretch': self.distance(left_mouth, right_mouth) / face_width,
            'eye_open': (self.distance(left_eye_top, left_eye_bottom) + 
                        self.distance(right_eye_top, right_eye_bottom)) / (2 * face_width),
            'eyebrow_height': (self.distance(left_eyebrow, left_eye_top) + 
                              self.distance(right_eyebrow, right_eye_top)) / (2 * face_width)
        }
        
        # Sadness detection
        eye_top_avg = (left_eye_top.y + right_eye_top.y) / 2
        eye_bottom_avg = (left_eye_bottom.y + right_eye_bottom.y) / 2
        iris_avg = landmarks[468].y
        eye_center_y = (eye_top_avg + eye_bottom_avg) / 2
        features['sad_offset'] = iris_avg - eye_center_y
        
        return features

    def get_emotion(self, landmarks):
        """Enhanced emotion detection with confidence"""
        features = self.get_emotion_features(landmarks)
        
        emotion_scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        # Emotion detection rules
        if features['mouth_stretch'] > 0.40 and features['mouth_open'] < 0.06:
            emotion_scores['happy'] = min(1.0, features['mouth_stretch'] * 2)
        
        if features['mouth_open'] >= 0.12:
            emotion_scores['surprise'] = min(1.0, features['mouth_open'] * 8)
        
        if 0.06 < features['mouth_open'] < 0.12 and features['eyebrow_height'] > 0.05:
            emotion_scores['fear'] = min(1.0, features['mouth_open'] * 10)
        
        if features['sad_offset'] > 0.01 and features['eye_open'] < 0.04:
            emotion_scores['sad'] = min(1.0, abs(features['sad_offset']) * 50)
        
        if features['mouth_open'] < 0.03 and features['mouth_stretch'] < 0.38:
            emotion_scores['disgust'] = 0.8
        
        if features['eye_open'] > 0.096 and features['mouth_open'] < 0.06:
            emotion_scores['angry'] = 0.7
        
        emotion_scores['neutral'] = 0.5
        
        detected_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[detected_emotion]
        
        return detected_emotion, confidence

    def process_frame(self, frame):
        """Process a single frame and return emotion data"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        
        emotion_data = {
            'emotion': 'neutral',
            'confidence': 0.0,
            'emoji': self.emotions['neutral']['emoji'],
            'color': self.emotions['neutral']['color'],
            'description': self.emotions['neutral']['description'],
            'face_detected': False
        }
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                emotion, confidence = self.get_emotion(face_landmarks.landmark)
                emotion_data.update({
                    'emotion': emotion,
                    'confidence': round(confidence, 2),
                    'emoji': self.emotions[emotion]['emoji'],
                    'color': self.emotions[emotion]['color'],
                    'description': self.emotions[emotion]['description'],
                    'face_detected': True
                })
                
                # Update tracking
                self.current_emotion = emotion
                self.emotion_confidence = confidence
                self.emotion_history.append(emotion)
                break
        
        return emotion_data

# Global instance
avatar = WebEmotionAvatar()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    """API endpoint to process frame data"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Resize frame
        frame = cv2.resize(frame, (320, 240))
        
        # Process frame
        emotion_data = avatar.process_frame(frame)
        
        return jsonify(emotion_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emotion_history')
def get_emotion_history():
    """Get emotion history"""
    history = list(avatar.emotion_history)
    return jsonify({'history': history})

@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    stats = {
        'current_emotion': avatar.current_emotion,
        'confidence': avatar.emotion_confidence,
        'history_length': len(avatar.emotion_history),
        'total_emotions': len(avatar.emotions)
    }
    return jsonify(stats)

@app.route('/health')
def health_check():
    """Health check endpoint for Vercel"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'service': 'Emotion Avatar API'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Get port from environment variable (for Vercel)
    port = int(os.environ.get('PORT', 5000))
    
    print("🌐 Starting Emotion Avatar Web Server...")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("🌍 Deployed on Vercel!")
    
    app.run(debug=False, host='0.0.0.0', port=port) 